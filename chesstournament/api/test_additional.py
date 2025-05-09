from django.test import TestCase, tag
from django.contrib.auth.models import User
from chess_models.models.constants import TournamentBoardType, TournamentSpeed
from chess_models.models.tournament import RankingSystemClass
from rest_framework import status
from rest_framework.test import APIClient
from chess_models.models import Tournament, Player, Game, Round
from unittest.mock import patch


print("Los errores mostrados en la consola son errores provocados"
      "para probar toda la funcionalidad.")
print("=" * 80)


class TournamentViewSetTests(TestCase):

    """Pruebas exhaustivas para TournamentViewSet."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='admin',
            password='password')
        self.client.force_authenticate(user=self.user)

        # Crear datos de prueba
        self.tournament = Tournament.objects.create(
            name="Test Tournament",
            administrativeUser=self.user
        )
        self.player1 = Player.objects.create(lichess_username="player1")
        self.player2 = Player.objects.create(lichess_username="player2")

    @tag("continua")
    def test_list_tournaments_unauthenticated(self):
        """Prueba listar torneos sin autenticación (permisos abiertos)."""
        self.client.logout()
        response = self.client.get('/api/v1/tournaments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("continua")
    def test_retrieve_tournament_unauthenticated(self):
        """Prueba obtener detalles de torneo sin autenticación."""
        self.client.logout()
        response = self.client.get(
            f'/api/v1/tournaments/{self.tournament.id}/'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("continua")
    def test_create_tournament_authenticated(self):
        """Prueba crear torneo con usuario autenticado."""
        data = {
            "name": "New Tournament",
            "players": "player1\nplayer2",
            "administrativeUser": self.user.id
        }
        response = self.client.post(
            '/api/v1/tournaments/', data, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['player_ids']), 2)

    @tag("continua")
    def test_create_tournament_malformed_player_data(self):
        """Prueba crear torneo con datos de jugadores mal formados."""
        data = {
            "name": "Malformed Player Tournament",
            "players": ('lichess_username\nLichessUsername1\n'
                        'LichessUsername2',
                        )
        }
        response = self.client.post(
            '/api/v1/tournaments/',
            data,
            format='json')
        # Debería crear el torneo pero no procesar jugadores
        self.assertEqual(len(response.data['player_ids']), 0)

    @tag("continua")
    def test_create_tournament_malformed_player_data2(self):
        """Prueba crear torneo con datos de jugadores mal formados."""
        data = {
            "name": "Malformed Player Tournament",
            "players": 'lichess_username\nLichessUsername1\nLichessUsername2',
        }
        response = self.client.post(
            '/api/v1/tournament_create/',
            data,
            format='json')
        # Debería crear el torneo pero no procesar jugadores
        self.assertEqual(len(response.data['player_ids']), 0)

    @tag("continua")
    def test_update_tournament(self):
        """Prueba actualizar un torneo existente."""
        data = {"name": "Updated Tournament Name"}
        response = self.client.patch(
            f'/api/v1/tournaments/{self.tournament.id}/', data, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Tournament Name")

    @tag("continua")
    def test_delete_tournament(self):
        """Prueba eliminar un torneo."""
        response = self.client.delete(
            f'/api/v1/tournaments/{self.tournament.id}/'
            )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @tag("continua")
    def test_add_players_to_tournament_with_invalid_data(self):
        """Prueba agregar jugadores a un torneo con datos inválidos."""
        data = {"players": "invalid_player"}
        response = self.client.post('/api/v1/tournaments/',
                                    data,
                                    format='json'
                                    )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("continua")
    def test_create_invalid_tournament(self):
        """Prueba crear un torneo con datos inválidos."""
        data = {
            "name": "",
            "players": "player1\nplayer2",
            "administrativeUser": self.user.id,
            "email": "invalid_email"  # Email inválido
        }
        response = self.client.post(
            '/api/v1/tournaments/',
            data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("continua")
    def test_ranking_system_class_str(self):
        """Prueba la representación en string de la clase"""
        ranking = RankingSystemClass.objects.create(value='EL')
        self.assertEqual(str(ranking), 'EL')

    @tag("continua")
    def test_get_ranking_method(self):
        """Prueba obtener el método de ranking."""
        RankingSystemClass.objects.create(value='EL')
        ranking = RankingSystemClass.getRanking()
        self.assertEqual(ranking.count(), 1)

    @tag("continua")
    def test_tournament_str(self):
        """Prueba la representación en string de un torneo."""
        self.assertEqual(str(self.tournament), "Test Tournament")

    @tag("continua")
    def test_get_players_sorted(self):
        """Prueba obtener los jugadores ordenados."""

        self.tournament.players.add(self.player1, self.player2)

        self.player1.lichess_rating_rapid = 1600
        self.player2.lichess_rating_rapid = 1500
        self.player1.save()
        self.player2.save()

        self.tournament.tournament_speed = TournamentSpeed.RAPID
        self.tournament.board_type = TournamentBoardType.LICHESS
        self.tournament.save()

        sorted_players = self.tournament.getPlayers(sorted=True)
        self.assertEqual(len(sorted_players), 2)
        self.assertEqual(sorted_players[0], self.player1)

    @tag("continua")
    def test_clean_ranking_list(self):
        """Prueba eliminar los jugadores."""
        self.tournament.addToRankingList('EL')
        self.assertEqual(self.tournament.rankingList.count(), 1)
        self.tournament.cleanRankingList()
        self.assertEqual(self.tournament.rankingList.count(), 0)

    @tag("continua")
    def test_add_remove_ranking_list(self):
        """Prueba agregar y eliminar jugadores de la lista de ranking."""
        self.tournament.addToRankingList('EL')
        self.assertEqual(self.tournament.rankingList.count(), 1)
        self.tournament.removeFromRankingList('EL')
        self.assertEqual(self.tournament.rankingList.count(), 0)

        result = self.tournament.removeFromRankingList('kajsd')
        self.assertEqual(result, False)

    @tag("continua")
    def test_get_ranking_from_unexistings_tournament(self):
        """Prueba obtener el ranking de un torneo inexistente."""
        response = self.client.get('/api/v1/get_ranking/9999999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("continua")
    def bad_request_creating_tournament(self):
        response = self.client.post(
            '/api/v1/tournament_create/',
            {},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("continua")
    def test_create_tournament(self):
        """Prueba crear un torneo."""
        data = {
            "name": "New Tournament",
            "administrativeUser": self.user.id,
            "players": "lichess_username\nrmarabini\n"
        }
        response = self.client.post(
            '/api/v1/tournament_create/',
            data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "New Tournament")
        self.assertEqual(len(response.data['player_ids']), 1)


class PlayerViewSetTests(TestCase):

    """Pruebas exhaustivas para PlayerViewSet."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='admin',
            password='password')
        self.client.force_authenticate(user=self.user)

        self.player = Player.objects.create(lichess_username="testplayer")

    @tag("continua")
    def test_list_players(self):
        """Prueba listar todos los jugadores."""
        response = self.client.get('/api/v1/players/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    @tag("continua")
    def test_retrieve_player(self):
        """Prueba obtener detalles de un jugador."""
        response = self.client.get(f'/api/v1/players/{self.player.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['lichess_username'], "testplayer")

    @tag("continua")
    def test_delete_player(self):
        """Prueba eliminar un jugador."""
        response = self.client.delete(f'/api/v1/players/{self.player.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class GameViewSetTests(TestCase):
    """Pruebas exhaustivas para GameViewSet."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='admin',
            password='password')
        self.client.force_authenticate(user=self.user)

        self.tournament = Tournament.objects.create(
            name="Test Tournament",
            administrativeUser=self.user
        )
        self.player1 = Player.objects.create(lichess_username="player1")
        self.player2 = Player.objects.create(lichess_username="player2")
        self.round = Round.objects.create(
            tournament=self.tournament,
            name="Round 1"
        )
        self.game = Game.objects.create(
            round=self.round,
            white=self.player1,
            black=self.player2
        )

    @tag("continua")
    def test_list_games(self):
        """Prueba listar todas las partidas."""
        response = self.client.get('/api/v1/games/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("continua")
    def test_create_game_authenticated(self):
        """Prueba crear partida con usuario autenticado."""
        data = {
            "round": self.round.id,
            "white": self.player1.id,
            "black": self.player2.id
        }
        response = self.client.post('/api/v1/games/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @tag("continua")
    def test_delete_game_authenticated(self):
        """Prueba eliminar partida con usuario autenticado."""
        response = self.client.delete(f'/api/v1/games/{self.game.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @tag("continua")
    def test_create_game_unauthenticated(self):
        """Prueba intentar crear partida sin autenticación."""
        # Desautenticamos al cliente
        self.client.force_authenticate(user=None)

        data = {
            "round": self.round.id,
            "white": self.player1.id,
            "black": self.player2.id
        }
        response = self.client.post('/api/v1/games/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @tag("continua")
    def test_delete_game_unauthenticated(self):
        """Prueba intentar eliminar partida sin autenticación."""
        # Desautenticamos al cliente
        self.client.force_authenticate(user=None)

        response = self.client.delete(f'/api/v1/games/{self.game.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @tag("continua")
    def test_update_game_authenticated(self):
        """Prueba actualizar partida con usuario autenticado."""
        data = {
            "result": "w"  # Blancas ganan
        }
        response = self.client.patch(
            f'/api/v1/games/{self.game.id}/',
            data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar que la partida se marcó como finalizada
        # tras actualizar el resultado
        updated_game = Game.objects.get(id=self.game.id)
        self.assertTrue(updated_game.finished)

    @tag("continua")
    def test_update_finished_game_unauthenticated(self):
        """Prueba intentar actualizar partida finalizada sin autenticación."""
        # Marcamos el juego como finalizado
        self.game.finished = True
        self.game.save()

        # Desautenticamos al cliente
        self.client.force_authenticate(user=None)

        data = {
            "result": "b"  # Cambiamos el resultado
        }
        response = self.client.patch(
            f'/api/v1/games/{self.game.id}/',
            data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag("continua")
    def test_update_unfinished_game_unauthenticated(self):
        """Prueba actualizar partida no finalizada sin autenticación."""
        # Aseguramos que el juego no está finalizado
        self.game.finished = False
        self.game.save()

        # Desautenticamos al cliente
        self.client.force_authenticate(user=None)

        data = {
            "result": "=",  # Blancas ganan
        }
        response = self.client.patch(
            f'/api/v1/games/{self.game.id}/',
            data,
            format='json'
            )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar que la actualización funcionó
        updated_game = Game.objects.get(id=self.game.id)
        self.assertEqual(updated_game.result, "=")  # Resultado actualizado

    @tag("continua")
    def create_game_unauthenticated(self):
        """Prueba crear partida sin autenticación."""
        # Desautenticamos al cliente
        self.client.force_authenticate(user=None)

        data = {
            "round": self.round.id,
            "white": self.player1.id,
            "black": self.player2.id
        }
        response = self.client.post('/api/v1/games/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @tag("continua")
    def test_detail_game(self):
        """Prueba obtener detalle de una partida."""
        response = self.client.get(f'/api/v1/games/{self.game.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.game.id)


class RoundViewSetTests(TestCase):
    """Pruebas exhaustivas para RoundViewSet."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='admin',
            password='password')
        self.client.force_authenticate(user=self.user)

        self.tournament = Tournament.objects.create(
            name="Test Tournament",
            administrativeUser=self.user
        )
        self.round = Round.objects.create(
            tournament=self.tournament,
            name="Round 1"
        )

    @tag("continua")
    def test_list_rounds(self):
        """Prueba listar todas las rondas."""
        response = self.client.get('/api/v1/rounds/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("continua")
    def test_retrieve_round(self):
        """Prueba obtener detalles de una ronda."""
        response = self.client.get(f'/api/v1/rounds/{self.round.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("continua")
    def test_delete_round(self):
        """Prueba eliminar una ronda."""
        response = self.client.delete(f'/api/v1/rounds/{self.round.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @tag("continua")
    def create_round_with_invalid_data(self):
        """Prueba crear ronda con datos inválidos."""
        data = {
            "name": ""
        }
        response = self.client.post('/api/v1/rounds/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateRoundAPIViewTests(TestCase):
    """Pruebas exhaustivas para CreateRoundAPIView."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='admin',
            password='password')
        self.client.force_authenticate(user=self.user)

        self.tournament = Tournament.objects.create(
            name="Test Tournament",
            administrativeUser=self.user
        )
        self.player1 = Player.objects.create(lichess_username="player1")
        self.player2 = Player.objects.create(lichess_username="player2")
        self.tournament.players.add(self.player1, self.player2)

    @tag("continua")
    def test_create_round_invalid_tournament_id(self):
        """Prueba crear ronda con ID de torneo inválido."""
        data = {"tournament_id": "id-invalido"}
        response = self.client.post(
            '/api/v1/create_round/',
            data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['result'])

    @tag("continua")
    def test_create_round_tournament_not_found(self):
        """Prueba crear ronda con torneo inexistente."""
        data = {"tournament_id": 999999}
        response = self.client.post(
            '/api/v1/create_round/',
            data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['result'])

    @tag("continua")
    def test_create_round_no_players_in_tournament(self):
        """Prueba crear ronda sin jugadores en el torneo."""
        empty_tournament = Tournament.objects.create(
            name="Empty Tournament",
            administrativeUser=self.user
        )
        data = {"tournament_id": empty_tournament.id}
        response = self.client.post(
            '/api/v1/create_round/',
            data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['result'])


class SearchTournamentsAPIViewTests(TestCase):
    """Pruebas exhaustivas para SearchTournamentsAPIView."""

    def setUp(self):
        self.client = APIClient()
        self.tournament1 = Tournament.objects.create(name="Chess Championship")
        self.tournament2 = Tournament.objects.create(name="Amateur Tournament")

    @tag("continua")
    def test_search_tournaments_valid(self):
        """Prueba buscar torneos con cadena válida."""
        data = {"search_string": "Chess"}
        response = self.client.post(
            '/api/v1/searchTournaments/',
            data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    @tag("continua")
    def test_search_tournaments_no_search_string(self):
        """Prueba buscar torneos sin cadena de búsqueda."""
        data = {}
        response = self.client.post(
            '/api/v1/searchTournaments/',
            data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['result'])


class TournamentCreateAPIViewTests(TestCase):
    """Pruebas exhaustivas para TournamentCreateAPIView."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='admin',
            password='password'
            )
        self.client.force_authenticate(user=self.user)

    @tag("continua")
    def test_create_tournament_unauthenticated(self):
        """Prueba crear torneo sin autenticación (debe fallar)."""
        self.client.logout()
        data = {"name": "New Tournament"}
        response = self.client.post(
            '/api/v1/tournament_create/',
            data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @tag("continua")
    def test_create_tournament(self):
        """Prueba crear torneo con datos válidos."""
        data = {
            "name": "New Tournament",
            "administrativeUser": self.user.id
        }
        response = self.client.post(
            '/api/v1/tournament_create/',
            data,
            format='json'
            )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetPlayersTests(TestCase):
    """Pruebas exhaustivas para GetPlayers."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='admin',
            password='password'
            )
        self.tournament = Tournament.objects.create(
            name="Test Tournament",
            administrativeUser=self.user
        )
        self.player1 = Player.objects.create(lichess_username="player1")
        self.player2 = Player.objects.create(lichess_username="player2")
        self.tournament.players.add(self.player1, self.player2)

    @tag("continua")
    def test_get_players_tournament_not_found(self):
        """Prueba obtener jugadores de torneo inexistente."""
        response = self.client.get('/api/v1/get_players/999999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data['result'])


class CustomUserViewSetTests(TestCase):
    """Pruebas exhaustivas para CustomUserViewSet."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='admin',
            password='password'
            )
        self.client.force_authenticate(user=self.user)

    @tag("continua")
    def test_user_create_disabled(self):
        """Prueba que la creación de usuarios está deshabilitada."""
        data = {
            "username": "newuser",
            "password": "newpassword"
        }
        response = self.client.post(
            '/api/v1/users/',
            data,
            format='json'
            )
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED
                         )

    @tag("continua")
    def test_user_list(self):
        """Prueba listar usuarios."""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("continua")
    def test_user_retrieve(self):
        """Prueba obtener detalles de usuario."""
        response = self.client.get(f'/api/v1/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateOTBGameAPIViewTests(TestCase):
    """Pruebas exhaustivas para UpdateOTBGameAPIView."""

    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='admin',
            password='password'
            )

        # Crear un torneo
        self.tournament = Tournament.objects.create(
            name="Test Tournament",
            administrativeUser=self.user
        )

        # Crear jugadores
        self.white_player = Player.objects.create(
            lichess_username="white_player",
            name="White Player",
            email="white@example.com"
        )
        self.black_player = Player.objects.create(
            lichess_username="black_player",
            name="Black Player",
            email="black@example.com"
        )

        # Crear una ronda
        self.round = Round.objects.create(
            tournament=self.tournament,
            name="Round 1"
        )

        # Crear una partida
        self.game = Game.objects.create(
            round=self.round,
            white=self.white_player,
            black=self.black_player,
            finished=False
        )

    @tag("continua")
    def test_update_otb_game_success_white_player(self):
        """Prueba actualizar partida OTB correctamente como jugador blanco."""
        data = {
            "game_id": self.game.id,
            "otb_result": "w",
            "name": "White Player",
            "email": "white@example.com"
        }
        response = self.client.post(
            '/api/v1/update_otb_game/',
            data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['result'])

        # Verificar que el juego se ha actualizado
        self.game.refresh_from_db()
        self.assertEqual(self.game.result, "w")
        self.assertTrue(self.game.finished)

    @tag("continua")
    def test_update_otb_game_success_black_player(self):
        """Prueba actualizar partida OTB correctamente como jugador negro."""
        data = {
            "game_id": self.game.id,
            "otb_result": "b",
            "name": "Black Player",
            "email": "black@example.com"
        }
        response = self.client.post(
            '/api/v1/update_otb_game/',
            data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['result'])

        # Verificar que el juego se ha actualizado
        self.game.refresh_from_db()
        self.assertEqual(self.game.result, "b")
        self.assertTrue(self.game.finished)

    @tag("continua")
    def test_update_otb_game_missing_game_id(self):
        """Prueba actualizar partida OTB sin proporcionar game_id."""
        data = {
            "otb_result": "1-0",
            "name": "White Player",
            "email": "white@example.com"
        }
        response = self.client.post(
            '/api/v1/update_otb_game/',
            data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['result'])
        self.assertEqual(response.data['message'], "Game ID is required")

    @tag("continua")
    def test_update_otb_game_invalid_game_id(self):
        """Prueba actualizar partida OTB con game_id inválido."""
        data = {
            "game_id": 999999,  # ID inexistente
            "otb_result": "1-0",
            "name": "White Player",
            "email": "white@example.com"
        }
        response = self.client.post(
            '/api/v1/update_otb_game/',
            data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data['result'])
        self.assertEqual(response.data['message'], "Game not found")

    @tag("continua")
    def test_update_otb_game_missing_result(self):
        """Prueba actualizar partida OTB sin proporcionar resultado."""
        data = {
            "game_id": self.game.id,
            "name": "White Player",
            "email": "white@example.com"
        }
        response = self.client.post(
            '/api/v1/update_otb_game/',
            data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['result'])
        self.assertEqual(response.data['message'], "OTB Result is required")

    @tag("continua")
    def test_update_otb_game_already_finished(self):
        """Prueba actualizar partida OTB que ya está finalizada."""
        # Primero finalizamos el juego
        self.game.finished = True
        self.game.result = "b"
        self.game.save()

        data = {
            "game_id": self.game.id,
            "otb_result": "w",
            "name": "White Player",
            "email": "white@example.com"
        }
        response = self.client.post(
            '/api/v1/update_otb_game/',
            data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['result'])
        self.assertEqual(response.data['message'], "Game is already finished")

        # Verificar que el resultado no ha cambiado
        self.game.refresh_from_db()
        self.assertEqual(self.game.result, "b")

    @tag("continua")
    def test_update_otb_game_staff_can_update_finished(self):
        """Prueba que un staff puede actualizar una partida finalizada."""
        # Primero finalizamos el juego
        self.game.finished = True
        self.game.result = "w"
        self.game.save()

        # Autenticamos como staff
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)

        data = {
            "game_id": self.game.id,
            "otb_result": "b"
        }
        response = self.client.post(
            '/api/v1/update_otb_game/',
            data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['result'])

        # Verificar que el resultado ha cambiado
        self.game.refresh_from_db()
        self.assertEqual(self.game.result, "b")

    @tag("continua")
    def test_update_otb_game_invalid_player_credentials(self):
        """Prueba actualizar partida OTB con
        credenciales de jugador inválidas."""
        data = {
            "game_id": self.game.id,
            "otb_result": "1-0",
            "name": "Invalid Player",
            "email": "invalid@example.com"
        }
        response = self.client.post(
            '/api/v1/update_otb_game/',
            data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['result'])
        self.assertEqual(response.data['message'],
                         "Player credentials do not match game participants")

        # Verificar que el juego no se ha actualizado
        self.game.refresh_from_db()
        self.assertEqual(self.game.result, '*')
        self.assertFalse(self.game.finished)

    @tag("continua")
    def test_update_otb_game_exception_handling(self):
        """Prueba el manejo de excepciones al actualizar partida OTB."""
        # Crear un mock para simular una excepción al guardar
        with patch('chess_models.models.game.Game.save') as mock_save:
            mock_save.side_effect = Exception("Test exception")

            data = {
                "game_id": self.game.id,
                "otb_result": "1-0",
                "name": "White Player",
                "email": "white@example.com"
            }

            response = self.client.post(
                '/api/v1/update_otb_game/',
                data,
                format='json'
                )

            self.assertEqual(response.status_code,
                             status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.assertFalse(response.data['result'])
            self.assertTrue(
                "Error: Test exception" in response.data['message']
                )


class AdminUpdateGameAPIViewTests(TestCase):
    """Pruebas exhaustivas para AdminUpdateGameAPIView."""

    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username='admin',
            password='password')
        self.other_user = User.objects.create_user(
            username='other',
            password='password')

        # Crear un torneo con admin_user como administrativo
        self.tournament = Tournament.objects.create(
            name="Test Tournament",
            administrativeUser=self.admin_user
        )

        # Crear jugadores
        self.white_player = Player.objects.create(
            lichess_username="white_player"
            )
        self.black_player = Player.objects.create(
            lichess_username="black_player"
            )

        # Crear una ronda
        self.round = Round.objects.create(
            tournament=self.tournament,
            name="Round 1"
        )

        # Crear una partida
        self.game = Game.objects.create(
            round=self.round,
            white=self.white_player,
            black=self.black_player,
            finished=False
        )

        # Autenticar como admin_user por defecto
        self.client.force_authenticate(user=self.admin_user)

    @tag("continua")
    def test_admin_update_game_success_with_otb_result(self):
        """Prueba actualizar partida como
        administrador usando otb_result."""
        data = {
            "game_id": self.game.id,
            "otb_result": "d"
        }
        response = self.client.post(
            '/api/v1/admin_update_game/',
            data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['result'])

        # Verificar que el juego se ha actualizado
        self.game.refresh_from_db()
        self.assertEqual(self.game.result, "d")
        self.assertTrue(self.game.finished)

    @tag("continua")
    def test_admin_update_game_success_with_serializer(self):
        """Prueba actualizar partida como
        administrador usando el serializer."""
        data = {
            "game_id": self.game.id,
        }
        response = self.client.post(
            '/api/v1/admin_update_game/',
            data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['result'])

        # Verificar que el juego se ha actualizado
        self.game.refresh_from_db()
        self.assertEqual(self.game.result, '*')

    @tag("continua")
    def test_admin_update_game_missing_game_id(self):
        """Prueba actualizar partida como
        administrador sin proporcionar game_id."""
        data = {
            "otb_result": "1-0"
        }
        response = self.client.post(
            '/api/v1/admin_update_game/',
            data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['result'])
        self.assertEqual(response.data['message'], "Game ID is required")

    @tag("continua")
    def test_admin_update_game_invalid_game_id(self):
        """Prueba actualizar partida como
        administrador con game_id inválido."""
        data = {
            "game_id": 999999,  # ID inexistente
            "otb_result": "1-0"
        }
        response = self.client.post(
            '/api/v1/admin_update_game/',
            data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data['result'])
        self.assertEqual(response.data['message'], "Game not found")

    @tag("continua")
    def test_admin_update_game_not_tournament_admin(self):
        """Prueba actualizar partida como usuario que
        no es el administrador del torneo."""
        # Autenticar como otro usuario
        self.client.force_authenticate(user=self.other_user)

        data = {
            "game_id": self.game.id,
            "otb_result": "1-0"
        }
        response = self.client.post(
            '/api/v1/admin_update_game/',
            data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.data['result'])
        self.assertEqual(response.data['message'],
                         "Only the user that create "
                         "the tournament can update it")

        # Verificar que el juego no se ha actualizado
        self.game.refresh_from_db()
        self.assertEqual(self.game.result, '*')
        self.assertFalse(self.game.finished)

    @tag("continua")
    def test_admin_update_game_unauthenticated(self):
        """Prueba actualizar partida como
        administrador sin autenticación."""
        # Eliminar autenticación
        self.client.force_authenticate(user=None)

        data = {
            "game_id": self.game.id,
            "otb_result": "1-0"
        }
        response = self.client.post(
            '/api/v1/admin_update_game/',
            data,
            format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    @tag("continua")
    def test_admin_update_game_serializer_validation_error(self):
        """Prueba actualizar partida con
        datos inválidos para el serializer."""
        # Suponiendo que el campo 'result' tiene validación
        # (por ejemplo, solo puede ser '1-0', '0-1', '1/2-1/2')
        data = {
            "game_id": self.game.id,
            "result": "invalid-result"  # Formato inválido
        }

        with patch('api.serializers.GameSerializer.is_valid') as mock_is_valid:
            from rest_framework.exceptions import ValidationError
            mock_is_valid.side_effect = ValidationError(
                {"result": ["Invalid result format"]}
                )

            response = self.client.post(
                '/api/v1/admin_update_game/', data, format='json'
                )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertFalse(response.data['result'])


class UpdateLichessGameAPIViewTests(TestCase):
    """Pruebas exhaustivas para UpdateLichessGameAPIView."""

    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='admin',
            password='password'
            )

        # Crear un torneo
        self.tournament = Tournament.objects.create(
            name="Test Tournament",
            administrativeUser=self.user
        )

        # Crear jugadores
        self.white_player = Player.objects.create(
            lichess_username="white_player"
            )
        self.black_player = Player.objects.create(
            lichess_username="black_player"
                                                  )

        # Crear una ronda
        self.round = Round.objects.create(
            tournament=self.tournament,
            name="Round 1"
        )

        # Crear una partida
        self.game = Game.objects.create(
            round=self.round,
            white=self.white_player,
            black=self.black_player,
            finished=False
        )

    @tag("continua")
    def test_update_lichess_game_missing_game_id(self):
        """Prueba actualizar partida
        Lichess sin proporcionar game_id."""
        data = {
            "lichess_game_id": "abcdef123456"
        }
        response = self.client.post(
            '/api/v1/update_lichess_game/',
            data,
            format='json'
            )
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST
                         )
        self.assertFalse(response.data['result'])
        self.assertEqual(response.data['message'], "Game ID is required")

    @tag("continua")
    def test_update_lichess_game_missing_lichess_game_id(self):
        """Prueba actualizar partida Lichess
        sin proporcionar lichess_game_id."""
        data = {
            "game_id": self.game.id
        }
        response = self.client.post(
            '/api/v1/update_lichess_game/',
            data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['result'])
        self.assertEqual(response.data['message'],
                         "Lichess game ID is required"
                         )

    @tag("continua")
    def test_update_lichess_game_invalid_game_id(self):
        """Prueba actualizar partida Lichess con game_id inválido."""
        data = {
            "game_id": 999999,  # ID inexistente
            "lichess_game_id": "abcdef123456"
        }
        response = self.client.post(
            '/api/v1/update_lichess_game/',
            data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data['result'])
        self.assertEqual(response.data['message'], "Game not found")

    @tag("continua")
    def test_update_lichess_game_lichess_api_error(self):
        """Prueba manejo de error de la API de Lichess."""
        data = {
            "game_id": self.game.id,
            "lichess_game_id": "abcdef123456"
        }

        # Mock para simular error de la API de Lichess
        with patch(
            'chess_models.models.game.Game.get_lichess_game_result'
        ) as mock_lichess:
            from chess_models.models.player import LichessAPIError
            mock_lichess.side_effect = LichessAPIError(
                "Lichess API error message"
                )

            response = self.client.post(
                '/api/v1/update_lichess_game/',
                data,
                format='json'
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertFalse(response.data['result'])
            self.assertEqual(
                response.data['message'],
                "Lichess API error message")

    @tag("continua")
    def test_update_lichess_game_request_exception(self):
        """Prueba manejo de excepción en request a Lichess."""
        data = {
            "game_id": self.game.id,
            "lichess_game_id": "abcdef123456"
        }

        # Mock para simular error de requests
        with patch(
            'chess_models.models.game.Game.get_lichess_game_result'
        ) as mock_lichess:
            from requests.exceptions import RequestException
            mock_lichess.side_effect = RequestException("Connection error")

            response = self.client.post(
                '/api/v1/update_lichess_game/',
                data,
                format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertFalse(response.data['result'])
            self.assertEqual(
                response.data['message'],
                "Failed to fetch data for game abcdef123456 from Lichess")


class GetRoundTest(TestCase):
    """Pruebas exhaustivas para GetRoundResults."""

    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='admin',
            password='password')
        self.client.force_authenticate(user=self.user)

        self.tournament = Tournament.objects.create(
            name="Test Tournament",
            administrativeUser=self.user
        )
        self.round = Round.objects.create(
            tournament=self.tournament,
            name="Round 1"
        )
        self.player1 = Player.objects.create(lichess_username="player1")
        self.player2 = Player.objects.create(lichess_username="player2")
        self.tournament.players.add(self.player1, self.player2)
        self.game = Game.objects.create(
            round=self.round,
            white=self.player1,
            black=self.player2,
            finished=False
        )

    @tag("continua")
    def test_get_round_results_success(self):
        """Prueba obtener resultados de una ronda."""
        response = self.client.get(
            f'/api/v1/get_round_results/{self.tournament.id}/'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("continua")
    def test_get_round_results_invalid_tournament_id(self):
        """Prueba obtener resultados de ronda con ID de torneo inválido."""
        response = self.client.get('/api/v1/get_round_results/999999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data['result'])
        self.assertEqual(response.data['message'], "Tournament not found")

    @tag("continua")
    def test_get_round_invalid_request(self):
        """Prueba obtener resultados de ronda con solicitud inválida."""
        response = self.client.get('/api/v1/get_round_results/7877/')
        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data['result'])

    @tag("continua")
    def test_different_types_of_tournament(self):
        """Prueba obtener resultados de ronda
        con diferentes tipos de torneo."""
        # Crear un torneo con un sistema de puntuación diferente
        tournament = Tournament.objects.create(
            name="Swiss Tournament",
            administrativeUser=self.user,
            tournament_speed='RA',
        )

        round = Round.objects.create(
            tournament=tournament,
            name="Round 1"
        )

        player3 = Player.objects.create(lichess_username="player3")
        player4 = Player.objects.create(lichess_username="player4")
        tournament.players.add(player3, player4)

        game = Game.objects.create(
            round=round,
            white=player3,
            black=player4,
            finished=False
        )

        response = self.client.get(
            f'/api/v1/get_round_results/{tournament.id}/'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        game.white = None
        game.save()

        response = self.client.get(
            f'/api/v1/get_round_results/{tournament.id}/'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        game.white = player3
        game.save()

        tournament.tournament_speed = 'BL'
        tournament.save()

        response = self.client.get(
            f'/api/v1/get_round_results/{tournament.id}/'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        game.white = None
        game.save()

        response = self.client.get(
            f'/api/v1/get_round_results/{tournament.id}/'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        tournament.tournament_speed = 'CL'
        tournament.save()

        response = self.client.get(
            f'/api/v1/get_round_results/{tournament.id}/'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        game.white = player3
        game.save()

        response = self.client.get(
            f'/api/v1/get_round_results/{tournament.id}/'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag("continua")
    def test_general_exception_handling(self):
        """Prueba el manejo de excepciones generales en la vista."""
        # Usar mock para forzar una excepción
        # cuando se llama a Round.objects.filter()
        with patch('chess_models.models.Round.objects.filter') as mock_filter:
            # Configurar el mock para que lance una excepción
            mock_filter.side_effect = Exception("Error de prueba forzado")

            # Hacer la solicitud a la API
            response = self.client.get(
                f'/api/v1/get_round_results/{self.tournament.id}/'
                )

            # Verificar que se maneje la excepción correctamente
            self.assertEqual(response.status_code,
                             status.HTTP_400_BAD_REQUEST)
            self.assertFalse(response.data['result'])
            self.assertEqual(response.data['message'],
                             "Error de prueba forzado")
