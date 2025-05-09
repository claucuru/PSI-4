from unittest.mock import patch
from django.test import TestCase, tag
from django.utils import timezone
from chess_models.models import (
    Player, Tournament, Round, Game, TournamentType, Scores,
    TournamentBoardType, TournamentSpeed, RankingSystem, RankingSystemClass,
    LichessAPIError
)
from chess_models.models.game import create_rounds
from chess_models.models.tournament import getScores, getBlackWins, getRanking


class GameModelAdditionalTest(TestCase):
    def setUp(self):
        self.tournament = Tournament.objects.create(
            name='tournament_test',
            tournament_type=TournamentType.ROUNDROBIN
        )

        # Crear jugadores
        self.players = []
        for i in range(4):
            player = Player.objects.create(
                name=f'Player {i}',
                email=f'player{i}@example.com',
                lichess_username=f'player{i}'
            )
            self.tournament.players.add(player)
            self.players.append(player)

        # Crear una ronda
        self.round = Round.objects.create(
            name='Round 1',
            tournament=self.tournament
        )

        print("Setup completado.")
        print(f"Jugadores creados: {[player.name for player in self.players]}")
        print(f"Torneo creado: {self.tournament.name}")
        print(f"Ronda creada: {self.round.__str__()}")

    @tag('continua')
    def test_create_rounds_invalid_tournament_type(self):
        """Test create_rounds with invalid tournament type."""
        tournament = Tournament.objects.create(
            name='tournament_swiss',
            tournament_type='SW'
        )

        # Añadir jugadores
        for player in self.players:
            tournament.players.add(player)

        # Llamar a create_rounds
        rounds = create_rounds(tournament)

        # Verificar que no se crearon rondas
        self.assertEqual(len(rounds), 0)

    @tag('continua')
    def test_create_rounds_odd_number_of_players(self):
        """Test create_rounds with odd number of players."""
        tournament = Tournament.objects.create(
            name='tournament_odd',
            tournament_type=TournamentType.ROUNDROBIN
        )

        # Añadir 3 jugadores (número impar)
        for i in range(3):
            tournament.players.add(self.players[i])

        # Llamar a create_rounds
        rounds = create_rounds(tournament)

        # Verificar que no se crearon rondas
        self.assertEqual(len(rounds), 0)

    @tag('continua')
    def test_create_rounds_with_swiss_byes(self):
        """Test create_rounds with swiss byes parameter."""
        tournament = Tournament.objects.create(
            name='tournament_with_byes',
            tournament_type=TournamentType.ROUNDROBIN
        )

        # Añadir jugadores
        for player in self.players:
            tournament.players.add(player)

        # Llamar a create_rounds con el parámetro swissByes
        swiss_byes = [1, 2]  # Algunos valores de ejemplo
        rounds = create_rounds(tournament, swissByes=swiss_byes)

        # Verificar que las rondas se crearon exitosamente
        self.assertEqual(len(rounds), 3)


class TournamentModelAdditionalTest(TestCase):
    def setUp(self):
        self.tournament = Tournament.objects.create(
            name='tournament_test',
            tournament_type=TournamentType.ROUNDROBIN,
            tournament_speed=TournamentSpeed.RAPID,
            board_type=TournamentBoardType.LICHESS
        )

        # Crear jugadores con diferentes ratings
        self.players = []
        for i in range(4):
            player = Player.objects.create(
                name=f'Player {i}',
                email=f'player{i}@example.com',
                lichess_username=f'player{i}',
                lichess_rating_rapid=1500 + i * 100,
                lichess_rating_blitz=1400 + i * 100,
                lichess_rating_bullet=1300 + i * 100,
                lichess_rating_classical=1600 + i * 100
            )
            self.tournament.players.add(player)
            self.players.append(player)

        # Crear sistemas de ranking
        RankingSystemClass.objects.get_or_create(
            value=RankingSystem.PLAIN_SCORE.value)
        RankingSystemClass.objects.get_or_create(
            value=RankingSystem.WINS.value)
        RankingSystemClass.objects.get_or_create(
            value=RankingSystem.BLACKTIMES.value)

    @tag('continua')
    def test_get_players_count(self):
        """Test getPlayersCount method."""
        count = self.tournament.getPlayersCount()
        self.assertEqual(count, 4)

    @tag('continua')
    def test_clean_ranking_list(self):
        """Test cleanRankingList method."""
        self.tournament.addToRankingList(RankingSystem.PLAIN_SCORE.value)
        self.tournament.addToRankingList(RankingSystem.WINS.value)

        # Verificar que se añadieron los sistemas de ranking
        self.assertEqual(self.tournament.rankingList.count(), 2)

        # Limpiar la lista de ranking
        self.tournament.cleanRankingList()

        # Verificar que la lista de ranking está vacía
        self.assertEqual(self.tournament.rankingList.count(), 0)

    @tag('continua')
    def test_add_to_ranking_list_existing(self):
        """Test addToRankingList with existing ranking system."""
        self.tournament.addToRankingList(RankingSystem.PLAIN_SCORE.value)

        # Verificar que se añadió
        self.assertEqual(self.tournament.rankingList.count(), 1)

        # Añadir el mismo sistema de ranking de nuevo
        self.tournament.addToRankingList(RankingSystem.PLAIN_SCORE.value)

        # Verificar que no se añadió de nuevo
        self.assertEqual(self.tournament.rankingList.count(), 1)

    @tag('continua')
    def test_remove_from_ranking_list_exists(self):
        """Test removeFromRankingList with existing ranking system."""
        self.tournament.addToRankingList(RankingSystem.PLAIN_SCORE.value)

        # Verificar que se añadió
        self.assertEqual(self.tournament.rankingList.count(), 1)

        # Eliminar el sistema de ranking
        result = self.tournament.removeFromRankingList(
            RankingSystem.PLAIN_SCORE.value)

        # Verificar que se eliminó
        self.assertTrue(result)
        self.assertEqual(self.tournament.rankingList.count(), 0)

    @tag('continua')
    def test_remove_from_ranking_list_not_exists(self):
        """Prueba removeFromRankingList
        con un sistema de ranking no existente"""
        # Intentar eliminar un sistema de ranking que no existe
        result = self.tournament.removeFromRankingList('XY')

        # Verificar que devuelve False
        self.assertFalse(result)

    @tag('continua')
    def test_get_round_count(self):
        """Test getRoundCount method."""
        Round.objects.create(name='Round 1', tournament=self.tournament)
        Round.objects.create(name='Round 2', tournament=self.tournament)

        # Verificar conteo
        self.assertEqual(self.tournament.getRoundCount(), 2)

    @tag('continua')
    def test_get_number_of_rounds_with_games(self):
        """Prueba el método get_number_of_rounds_with_games"""
        # Crear rondas
        round1 = Round.objects.create(name='Round 1',
                                      tournament=self.tournament)
        round2 = Round.objects.create(name='Round 2',
                                      tournament=self.tournament)

        # Crear juegos solo en rondas 1 y 2
        Game.objects.create(white=self.players[0], black=self.players[1],
                            round=round1)
        Game.objects.create(white=self.players[2], black=self.players[3],
                            round=round2)

        # Verificar conteo
        self.assertEqual(self.tournament.get_number_of_rounds_with_games(), 2)

    @tag('continua')
    def test_get_latest_round_with_games(self):
        """Prueba el método get_latest_round_with_games"""
        # Crear rondas
        round1 = Round.objects.create(
            name='Round 1',
            tournament=self.tournament,
            start_date=timezone.now()
        )

        # Esperar un momento para asegurar timestamps diferentes
        import time
        time.sleep(0.1)

        round2 = Round.objects.create(
            name='Round 2',
            tournament=self.tournament,
            start_date=timezone.now()
        )

        # Crear juego en la ronda 1
        Game.objects.create(white=self.players[0], black=self.players[1],
                            round=round1)

        # Verificar que la última ronda con juegos es la ronda 1
        latest_round = self.tournament.get_latest_round_with_games()
        self.assertEqual(latest_round, round1)

        # Añadir juego a la ronda 2
        Game.objects.create(white=self.players[2], black=self.players[3],
                            round=round2)

        # Verificar que la última ronda con juegos es ahora la ronda 2
        latest_round = self.tournament.get_latest_round_with_games()
        self.assertEqual(latest_round, round2)

    @tag('continua')
    def test_get_latest_round_with_games_no_games(self):
        """Test get_latest_round_with_games with no games."""
        Round.objects.create(name='Round 1', tournament=self.tournament)
        Round.objects.create(name='Round 2', tournament=self.tournament)

        # Verificar que devuelve None
        latest_round = self.tournament.get_latest_round_with_games()
        self.assertIsNone(latest_round)

    @tag('continua')
    def test_get_games(self):
        """Prueba el método getGames"""
        # Crear rondas
        round1 = Round.objects.create(name='Round 1',
                                      tournament=self.tournament)
        round2 = Round.objects.create(name='Round 2',
                                      tournament=self.tournament)

        # Crear juegos
        game1 = Game.objects.create(white=self.players[0],
                                    black=self.players[1], round=round1)
        game2 = Game.objects.create(white=self.players[2],
                                    black=self.players[3], round=round1)
        game3 = Game.objects.create(white=self.players[0],
                                    black=self.players[2], round=round2)

        # Verificar que se devuelven todos los juegos
        games = self.tournament.getGames()
        self.assertEqual(games.count(), 3)
        self.assertIn(game1, games)
        self.assertIn(game2, games)
        self.assertIn(game3, games)

    @tag('continua')
    def test_get_lichess_game_result(self):
        """Prueba el método get_lichess_game_result
          con todos los resultados posibles"""
        # Crear una ronda para los juegos
        round1 = Round.objects.create(name='Round 1',
                                      tournament=self.tournament)

        # Mock de la respuesta de la API de Lichess
        def mock_lichess_response(game_id, winner=None, status=None):
            """Simula diferentes respuestas de la API de Lichess"""
            base_response = {
                'players': {
                    'white': {'userId':
                              self.players[0].lichess_username.lower()},
                    'black': {'userId':
                              self.players[1].lichess_username.lower()}
                }
            }

            if winner:
                base_response['winner'] = winner
            if status:
                base_response['status'] = status

            return base_response

        # Caso 1: Blancas ganan
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_lichess_response(
                'test1', winner='white')

            game_white_win = Game.objects.create(
                white=self.players[0],
                black=self.players[1],
                round=round1
            )
            result = game_white_win.get_lichess_game_result('test1')[0]
            self.assertEqual(result, 'W')  # 'w' representa victoria de blancas

        # Caso 2: Negras ganan
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_lichess_response(
                'test2', winner='black')

            game_black_win = Game.objects.create(
                white=self.players[0],
                black=self.players[1],
                round=round1
            )
            result = game_black_win.get_lichess_game_result('test2')[0]
            self.assertEqual(result, 'B')  # 'b' representa victoria de negras

        # Caso 3: Empate
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_lichess_response(
                'test3', status='draw')

            game_draw = Game.objects.create(
                white=self.players[0],
                black=self.players[1],
                round=round1
            )
            result = game_draw.get_lichess_game_result('test3')[0]
            self.assertEqual(result, 'D')  # '=' representa empate

        # Caso 4: Resultado no disponible (partida en progreso)
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {'players': {
                'white': {'userId': self.players[0].lichess_username.lower()},
                'black': {'userId': self.players[1].lichess_username.lower()}
            }}  # Sin winner ni status de finalización

            game_no_result = Game.objects.create(
                white=self.players[0],
                black=self.players[1],
                round=round1
            )
            result = game_no_result.get_lichess_game_result('test4')[0]
            self.assertEqual(result, '*')

        # Caso 5: Error en la API
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 404

            game_error = Game.objects.create(
                white=self.players[0],
                black=self.players[1],
                round=round1
            )
            with self.assertRaises(LichessAPIError):
                game_error.get_lichess_game_result('test5')

    @tag('continua')
    def test_ranking_system_class_methods(self):
        """Prueba los métodos getPlayers y getRanking de RankingSystemClass"""
        ranking_systems = RankingSystemClass.getRanking()
        self.assertEqual(ranking_systems.count(), 3)

        # Verificar que los sistemas de ranking esperados están presentes
        system_values = [system.value for system in ranking_systems]
        self.assertIn(RankingSystem.PLAIN_SCORE.value, system_values)
        self.assertIn(RankingSystem.WINS.value, system_values)
        self.assertIn(RankingSystem.BLACKTIMES.value, system_values)

        # Probar getPlayers con diferentes configuraciones de torneo
        # Caso 1: Torneo rápido en Lichess
        self.tournament.tournament_speed = TournamentSpeed.RAPID
        self.tournament.board_type = TournamentBoardType.LICHESS
        self.tournament.save()

        players_sorted = self.tournament.getPlayers(sorted=True)
        self.assertEqual(len(players_sorted), 4)
        ratings = [p.lichess_rating_rapid for p in players_sorted]
        self.assertEqual(ratings, sorted(ratings))

        # Caso 2: Torneo blitz en Lichess
        self.tournament.tournament_speed = TournamentSpeed.BLITZ
        self.tournament.save()

        players_sorted = self.tournament.getPlayers(sorted=True)
        ratings = [p.lichess_rating_blitz for p in players_sorted]
        self.assertEqual(ratings, sorted(ratings))

        # Caso 3: Torneo bullet en Lichess
        self.tournament.tournament_speed = TournamentSpeed.BULLET
        self.tournament.save()

        players_sorted = self.tournament.getPlayers(sorted=True)
        ratings = [p.lichess_rating_bullet for p in players_sorted]
        self.assertEqual(ratings, sorted(ratings))

        # Caso 4: Torneo clásico en Lichess
        self.tournament.tournament_speed = TournamentSpeed.CLASSICAL
        self.tournament.save()

        players_sorted = self.tournament.getPlayers(sorted=True)
        ratings = [p.lichess_rating_classical for p in players_sorted]
        self.assertEqual(ratings, sorted(ratings))
        self.tournament.board_type = 'OTH'  # Otro tipo de tablero
        self.tournament.save()

        players_sorted = self.tournament.getPlayers(sorted=True)
        players_unsorted = self.tournament.getPlayers(sorted=False)
        self.assertEqual(list(players_sorted), list(players_unsorted))


class ScoreCalculationTest(TestCase):
    def setUp(self):
        self.tournament = Tournament.objects.create(
            name='tournament_test',
            tournament_type=TournamentType.ROUNDROBIN,
            win_points=1.0,
            draw_points=0.5,
            lose_points=0.0
        )

        # Crear jugadores
        self.players = []
        for i in range(4):
            player = Player.objects.create(
                name=f'Player {i}',
                email=f'player{i}@example.com',
                lichess_username=f'player{i}'
            )
            self.tournament.players.add(player)
            self.players.append(player)

        # Crear una ronda
        self.round = Round.objects.create(
            name='Round 1',
            tournament=self.tournament
        )


    @tag('continua')
    def test_get_scores_forfeit_win(self):
        """Prueba getScores con resultado de victoria por incomparecencia"""
        # Crear juego con resultado de victoria por incomparecencia
        Game.objects.create(
            white=self.players[0],
            black=self.players[1],
            round=self.round,
            result=Scores.FORFEITWIN.value  # Victoria por incomparecencia
        )

        # Calcular puntuaciones
        scores = getScores(self.tournament)

        # Verificar puntuaciones
        self.assertEqual(scores[self.players[0]][
            RankingSystem.PLAIN_SCORE.value], 1.0)  # Victoria
        self.assertEqual(scores[self.players[1]][
            RankingSystem.PLAIN_SCORE.value], 0.0)  # Sin puntos

    @tag('continua')
    def test_get_scores_bye_z(self):
        """Prueba getScores con resultado BYE_Z"""
        # Crear juego con resultado BYE_Z (bye con cero puntos)
        Game.objects.create(
            white=self.players[0],
            black=None,  # Sin oponente
            round=self.round,
            result=Scores.BYE_Z.value
        )

        # Calcular puntuaciones
        scores = getScores(self.tournament)

        # Verificar puntuaciones
        self.assertEqual(scores[self.players[0]][
            RankingSystem.PLAIN_SCORE.value], 0.0)  # Cero puntos

    @tag('continua')
    def test_get_scores_bye_h(self):
        """Prueba getScores con resultado BYE_H"""
        # Crear juego con resultado BYE_H (bye con medio punto)
        Game.objects.create(
            white=self.players[0],
            black=None,  # Sin oponente
            round=self.round,
            result=Scores.BYE_H.value
        )

        # Calcular puntuaciones
        scores = getScores(self.tournament)

        # Verificar puntuaciones
        self.assertEqual(scores[self.players[0]][
            RankingSystem.PLAIN_SCORE.value], 0.5)  # Medio punto

    @tag('continua')
    def test_get_scores_bye_f(self):
        """Prueba getScores con resultado BYE_F"""
        # Crear juego con resultado BYE_F (bye con punto completo)
        Game.objects.create(
            white=self.players[0],
            black=None,  # Sin oponente
            round=self.round,
            result=Scores.BYE_F.value
        )

        # Calcular puntuaciones
        scores = getScores(self.tournament)

        # Verificar puntuaciones
        self.assertEqual(scores[self.players[0]][
            RankingSystem.PLAIN_SCORE.value], 1.0)  # Punto completo

    @tag('continua')
    def test_get_scores_bye_u(self):
        """Prueba getScores con resultado BYE_U"""
        # Crear juego con resultado BYE_U (bye con punto completo)
        Game.objects.create(
            white=self.players[0],
            black=None,  # Sin oponente
            round=self.round,
            result=Scores.BYE_U.value
        )

        # Calcular puntuaciones
        scores = getScores(self.tournament)

        # Verificar puntuaciones
        self.assertEqual(scores[self.players[0]][
            RankingSystem.PLAIN_SCORE.value], 1.0)  # Punto completo


    @tag('continua')
    def test_get_ranking_with_no_games(self):
        """Test getRanking when tournament has no games."""
        ranking = getRanking(self.tournament)

        # Verificar que los jugadores tienen rangos y puntuaciones iniciales
        for rank, player in enumerate(self.players, 1):
            self.assertIn(player, ranking)
            self.assertEqual(ranking[player]['rank'], rank)
            self.assertEqual(ranking[player][RankingSystem.PLAIN_SCORE.value],
                             0.0)
            self.assertEqual(ranking[player][RankingSystem.WINS.value], 0)
            self.assertEqual(ranking[player][RankingSystem.BLACKTIMES.value],
                             0)


class TestPlayerInvalid(TestCase):
    def setUp(self):
        self.player = Player(
            name='Invalid Player',
            email='invalid_email',
            fide_id='12345678900',
        )

    @tag('continua')
    def test_check_lichess_user_exists_invalid(self):
        """Prueba la verificación de existencia
        de usuario Lichess con datos inválidos"""
        exists = self.player.check_lichess_user_exists()
        self.assertFalse(exists)

    @tag('continua')
    def test_get_lichess_user_ratings_invalid(self):
        """Prueba la obtención de ratings de Lichess con datos inválidos"""
        self.player.get_lichess_user_ratings()  # Debería lanzar una excepción
        self.assertEqual(self.player.lichess_rating_bullet, 0)
        self.assertEqual(self.player.lichess_rating_blitz, 0)
        self.assertEqual(self.player.lichess_rating_rapid, 0)
        self.assertEqual(self.player.lichess_rating_classical, 0)
