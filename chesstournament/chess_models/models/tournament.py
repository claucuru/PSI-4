from django.db import models
from django.contrib.auth import get_user_model
from .player import Player
from .referee import Referee
from .constants import (
    TournamentBoardType, TournamentSpeed, TournamentType,
    RankingSystem, Scores
)

User = get_user_model()


class RankingSystemClass(models.Model):
    """Modelo que representa un sistema de ranking.
    Atributos:
        value (str): Valor del sistema de ranking.
    """
    value = models.CharField(
        max_length=2,
        choices=RankingSystem.choices,
        primary_key=True
    )

    def __str__(self):
        return self.value

    @classmethod
    def getRanking(cls):
        return cls.objects.all()


class Tournament(models.Model):
    """Modelo que representa un torneo de ajedrez."""
    name = models.CharField(max_length=128, unique=True)
    administrativeUser = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True
    )
    players = models.ManyToManyField(Player, blank=True)
    referee = models.ForeignKey(
        Referee, on_delete=models.CASCADE, null=True, blank=True
    )
    start_date = models.DateTimeField(auto_now=True)
    end_date = models.DateField(null=True, blank=True)
    max_update_time = models.IntegerField(default=43200)
    only_administrative = models.BooleanField(default=False)
    tournament_type = models.CharField(
        max_length=2,
        choices=TournamentType.choices,
        default=TournamentType.ROUNDROBIN
    )
    tournament_speed = models.CharField(
        max_length=2,
        choices=TournamentSpeed.choices,
        default=TournamentSpeed.CLASSICAL
    )
    board_type = models.CharField(
        max_length=3,
        choices=TournamentBoardType.choices,
        default=TournamentBoardType.LICHESS
    )
    win_points = models.FloatField(default=1.0)
    draw_points = models.FloatField(default=0.5)
    lose_points = models.FloatField(default=0.0)
    timeControl = models.CharField(max_length=32, default='15+0')
    number_of_rounds_for_swiss = models.IntegerField(default=0)
    rankingList = models.ManyToManyField(RankingSystemClass, blank=True)

    def __str__(self):
        return self.name

    def getPlayers(self, sorted=False):
        if not sorted:
            return list(self.players.all())

        if (
            self.tournament_speed == TournamentSpeed.RAPID and
            self.board_type == TournamentBoardType.LICHESS
        ):
            return list(self.players.order_by("lichess_rating_rapid"))
        elif (
            self.tournament_speed == TournamentSpeed.BLITZ and
            self.board_type == TournamentBoardType.LICHESS
        ):
            return list(self.players.order_by("lichess_rating_blitz"))
        elif (
            self.tournament_speed == TournamentSpeed.BULLET and
            self.board_type == TournamentBoardType.LICHESS
        ):
            return list(self.players.order_by("lichess_rating_bullet"))
        elif (
            self.tournament_speed == TournamentSpeed.CLASSICAL and
            self.board_type == TournamentBoardType.LICHESS
        ):
            return list(self.players.order_by("lichess_rating_classical"))
        else:
            return list(self.players.all())

    def getPlayersCount(self):
        return self.players.count()

    def cleanRankingList(self):
        self.rankingList.clear()

    def addToRankingList(self, ranking_value):
        ranking_obj, _ = RankingSystemClass.objects.get_or_create(
            value=ranking_value
        )
        self.rankingList.add(ranking_obj)

    def removeFromRankingList(self, ranking_value):
        try:
            ranking_obj = RankingSystemClass.objects.get(value=ranking_value)
            self.rankingList.remove(ranking_obj)
            return True
        except RankingSystemClass.DoesNotExist:
            return False

    def getRoundCount(self):
        from .round import Round
        return Round.objects.filter(tournament=self).count()

    def get_number_of_rounds_with_games(self):
        from .round import Round
        from .game import Game

        rounds_with_games = 0
        tournament_rounds = Round.objects.filter(tournament=self)

        for tournament_round in tournament_rounds:
            if Game.objects.filter(round=tournament_round).exists():
                rounds_with_games += 1

        return rounds_with_games

    def get_latest_round_with_games(self):
        from .round import Round
        from .game import Game

        tournament_rounds = Round.objects.filter(
            tournament=self
        ).order_by('-start_date')

        for tournament_round in tournament_rounds:
            if Game.objects.filter(round=tournament_round).exists():
                return tournament_round

        return None

    def getGames(self):
        from .game import Game
        return Game.objects.filter(round__tournament=self)


def getScores(tournament):
    from .game import Game
    from .round import Round

    PLAIN_SCORE = RankingSystem.PLAIN_SCORE.value
    results = {}

    players = tournament.getPlayers()
    for player in players:
        results[player] = {PLAIN_SCORE: 0.0}

    tournament_rounds = Round.objects.filter(tournament=tournament)

    for tournament_round in tournament_rounds:
        games = Game.objects.filter(round=tournament_round)
        for game in games:
            if game.result == 'W':
                if game.white in results:
                    results[game.white][PLAIN_SCORE] += tournament.win_points
                if game.black in results:
                    results[game.black][PLAIN_SCORE] += tournament.lose_points
            elif game.result == 'B':
                if game.white in results:
                    results[game.white][PLAIN_SCORE] += tournament.lose_points
                if game.black in results:
                    results[game.black][PLAIN_SCORE] += tournament.win_points
            elif game.result == 'D':
                if game.white in results:
                    results[game.white][PLAIN_SCORE] += tournament.draw_points
                if game.black in results:
                    results[game.black][PLAIN_SCORE] += tournament.draw_points
            elif game.result == Scores.FORFEITWIN.value:
                if game.white in results:
                    results[game.white][PLAIN_SCORE] += tournament.win_points
            elif game.result == Scores.BYE_Z.value:
                if game.white in results:
                    results[game.white][PLAIN_SCORE] += tournament.lose_points
            elif game.result == Scores.BYE_H.value:
                if game.white in results:
                    results[game.white][PLAIN_SCORE] += tournament.draw_points
            elif game.result == Scores.BYE_F.value:
                if game.white in results:
                    results[game.white][PLAIN_SCORE] += tournament.win_points
            elif game.result == Scores.BYE_U.value:
                if game.white in results:
                    results[game.white][PLAIN_SCORE] += tournament.win_points

    return results


def getBlackWins(tournament, results):
    from .game import Game
    from .round import Round

    WINS = RankingSystem.WINS.value
    BLACKTIMES = RankingSystem.BLACKTIMES.value

    players = tournament.getPlayers()
    for player in players:
        results[player][WINS] = 0
        results[player][BLACKTIMES] = 0

    tournament_rounds = Round.objects.filter(tournament=tournament)

    for tournament_round in tournament_rounds:
        games = Game.objects.filter(round=tournament_round)

        for game in games:
            if game.result not in [
                Scores.FORFEITWIN.value, Scores.FORFEITLOSS.value,
                Scores.BYE_F.value, Scores.BYE_H.value,
                Scores.BYE_U.value, Scores.BYE_Z.value
            ]:
                if game.black in results:
                    results[game.black][BLACKTIMES] += 1

                if game.result == 'W':
                    if game.white in results:
                        results[game.white][WINS] += 1
                if game.result == 'B':
                    if game.black in results:
                        results[game.black][WINS] += 1

    return results

def getRanking(tournament):
    from .game import Game
    from .round import Round
    
    # Obtener las puntuaciones y victorias con negras
    results = getScores(tournament)
    results = getBlackWins(tournament, results)
    
    # Verificar si el torneo tiene juegos - REVISAMOS ESTA PARTE
    tournament_has_games = False
    games_count = Game.objects.filter(round__tournament=tournament).count()
    tournament_has_games = games_count > 0
    
    # Si no hay juegos, retornar un ranking inicial
    if not tournament_has_games:
        players = tournament.players.all()
        ranked_results = {}
        for rank, player in enumerate(players, 1):
            ranked_results[player] = {
                'rank': rank,
                RankingSystem.PLAIN_SCORE.value: 0.0,
                RankingSystem.WINS.value: 0,
                RankingSystem.BLACKTIMES.value: 0
            }
        return ranked_results
    
    # Manejar el caso cuando rankingList está vacío
    try:
        ranking_criteria = list(
            tournament.rankingList.values_list('value', flat=True)
        )
        # Si la lista está vacía, usar criterios predeterminados
        if not ranking_criteria:
            ranking_criteria = [
                RankingSystem.PLAIN_SCORE.value,
                RankingSystem.WINS.value,
                RankingSystem.BLACKTIMES.value
            ]
    except Exception as e:
        # En caso de error (tabla no existe, error de relación, etc.)
        print(f"Error al obtener rankingList: {e}")
        # Usar criterios predeterminados
        ranking_criteria = [
            RankingSystem.PLAIN_SCORE.value,
            RankingSystem.WINS.value,
            RankingSystem.BLACKTIMES.value
        ]
    
    # Asegurar que PLAIN_SCORE esté en los criterios
    if RankingSystem.PLAIN_SCORE.value not in ranking_criteria:
        ranking_criteria.insert(0, RankingSystem.PLAIN_SCORE.value)
    
    players = tournament.getPlayers(sorted=False)
    
    def sort_key(player):
        # Asegurarse de que el jugador existe en los resultados
        if player not in results:
            return tuple(0 for _ in ranking_criteria)
        
        return tuple(-results[player].get(criterion, 0)
                 for criterion in ranking_criteria)
    
    sorted_players = sorted(players, key=sort_key)
    
    ranked_results = {}
    current_rank = 1
    for player in sorted_players:
        # Verificar si el jugador existe en los resultados
        if player in results:
            player_results = {
                'rank': current_rank,
                RankingSystem.PLAIN_SCORE.value: results[player].get(
                    RankingSystem.PLAIN_SCORE.value, 0
                ),
                RankingSystem.WINS.value: results[player].get(
                    RankingSystem.WINS.value, 0
                ),
                RankingSystem.BLACKTIMES.value: results[player].get(
                    RankingSystem.BLACKTIMES.value, 0
                )
            }
                    
            ranked_results[player] = player_results
        else:
            # Manejar el caso donde el jugador no tiene resultados
            ranked_results[player] = {
                'rank': current_rank,
                RankingSystem.PLAIN_SCORE.value: 0,
                RankingSystem.WINS.value: 0,
                RankingSystem.BLACKTIMES.value: 0
            }
            
        current_rank += 1

    
    return ranked_results
