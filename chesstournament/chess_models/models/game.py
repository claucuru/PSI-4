from django.db import models
from django.utils import timezone
import requests

from .player import Player, LichessAPIError
from .round import Round
from .constants import Scores


class Game(models.Model):
    """
    Modelo que representa una partida de ajedrez jugada dentro de un torneo.
    Almacena información sobre los jugadores, el resultado, la ronda a la que
    pertenece, y fechas relevantes.

    Atributos:
        white (Player): Jugador que juega con las piezas blancas.
        black (Player): Jugador que juega con las piezas negras.
        finished (bool): Indica si la partida ha terminado o no.
        round (Round): Ronda a la que pertenece la partida.
        start_date (datetime): Fecha y hora de inicio de la partida.
        update_date (datetime): Fecha y hora de última actualización
        de la partida.
        result (str): Resultado de la partida, representado por un carácter.
        rankingOrder (int): Orden de clasificación del juego en la ronda.
    """
    white = models.ForeignKey(
        Player, on_delete=models.CASCADE,
        related_name='white_player',
        null=True,
        blank=True
    )
    black = models.ForeignKey(
        Player, on_delete=models.CASCADE,
        related_name='black_player',
        null=True,
        blank=True
    )
    finished = models.BooleanField(default=False)
    round = models.ForeignKey(
        Round, on_delete=models.CASCADE,
    )
    start_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    result = models.CharField(
        max_length=1, default=Scores.NOAVAILABLE,
        choices=Scores.choices,
    )
    rankingOrder = models.IntegerField(default=0)

    def __str__(self):
        """Representación en cadena de la partida."""
        white = self.white
        black = self.black
        white_str = f"{str(white)}({white.id})" if white else "No player"
        black_str = f"{str(black)}({black.id})" if black else "No player"
        return f"{white_str} vs {black_str} = {self.get_result_display()}"

    def get_lichess_game_result(self, game_id):
        """
        Accede a la API de Lichess para obtener el resultado de una partida.
        Args:
        game_id (str): Identificador de la partida en Lichess
        Returns:
        tuple: (resultado, jugador_blanco, jugador_negro)
        donde resultado es un string con el valor de Scores
        Raises:
        Exception: Si hay un error al acceder a la API
        """
        url = f"https://lichess.org/api/game/{game_id}"
        response = requests.get(url)
        if response.status_code != 200:
            raise LichessAPIError("Failed to fetch data for game")
        data = response.json()
        # Obtenemos los nombres de usuario de los jugadores
        white_username = data.get('players', {}).get('white', {}).get('userId')
        black_username = data.get('players', {}).get('black', {}).get('userId')

        # Verificar si los jugadores coinciden con los esperados
        if (self.white.lichess_username.lower() != white_username.lower() or
                self.black.lichess_username.lower() != black_username.lower()):
            raise LichessAPIError(
                "Players for game " + game_id +
                " are different"
            )

        # Determinamos el resultado según el ganador o si fue un empate
        winner = data.get('winner')
        if winner == 'white':
            result = 'w'  # Cambiado de Scores.WHITE a 'w'
        elif winner == 'black':
            result = 'b'  # Cambiado de Scores.BLACK a 'b'
        elif data.get('status') == 'draw' or data.get('status') == 'stalemate':
            result = '='  # Cambiado de Scores.DRAW a 'd'
        else:
            result = '*'  # Cambiado de Scores.NOAVAILABLE a '*'

        return result, white_username, black_username


def create_rounds(tournament, swissByes=None):
    """
    Crea y almacena en la base de datos todas las
    rondas y partidas para un torneo.
    Implementa el Sistema Berger (Round Robin) para emparejar jugadores.
    Esta versión solo maneja un número par de jugadores.

    Args:
        tournament: Instancia del modelo Tournament para el que se crearán
                   las rondas
        swissByes: Parámetro opcional para torneos de tipo Swiss
                  (no usado en esta implementación)

    Returns:
        list: Lista de rondas creadas
    """
    if swissByes is None:
        swissByes = []

    # Obtenemos los jugadores del torneo
    players = list(tournament.players.all())
    num_players = len(players)

    # Verificamos que sea un torneo Round Robin y
    # que tenga un número par de jugadores
    if tournament.tournament_type != 'SR' or num_players % 2 != 0:
        print(
            f"Error: El torneo debe ser Round Robin y tener un número par de "
            f"jugadores. Tipo actual: {tournament.tournament_type}, "
            f"Jugadores: {num_players}"
        )
        return []

    # Para simplificar, trabajamos con índices (1 a num_players)
    player_indices = list(range(1, num_players + 1))

    # Generamos todos los emparejamientos siguiendo el algoritmo Berger
    all_pairings = []

    # Primera ronda: emparejar primero con último, segundo con penúltimo, etc.
    first_round = []
    for i in range(num_players // 2):
        pairing = [player_indices[i], player_indices[num_players - 1 - i]]
        first_round.append(pairing)
    all_pairings.append(first_round)

    # Generamos el resto de rondas
    for r in range(1, num_players - 1):
        prev_round = all_pairings[r - 1]
        new_round = []

        # Primera pareja: último número de ronda anterior con el número mayor
        highest_num = num_players
        last_num_in_prev = prev_round[-1][1]

        if r % 2 == 1:
            # Para la segunda ronda, es [mayor, último]
            new_round.append([highest_num, last_num_in_prev])
        else:
            # Para las rondas subsiguientes (a partir de la tercera),
            # el orden del primer emparejamiento se invierte
            new_round.append([last_num_in_prev, highest_num])

        rest_of_pairs = []

        for i in range(len(prev_round)):
            if (prev_round[i][0] != last_num_in_prev and
                    prev_round[i][0] != highest_num):
                rest_of_pairs.append(prev_round[i][0])
            if (prev_round[i][1] != last_num_in_prev and
                    prev_round[i][1] != highest_num):
                rest_of_pairs.append(prev_round[i][1])

        rest_of_pairs.reverse()

        for i in range(0, len(rest_of_pairs)-1, 2):
            pairing = [rest_of_pairs[i+1], rest_of_pairs[i]]
            new_round.append(pairing)

        all_pairings.append(new_round)

    # Ahora creamos las rondas y juegos en la base de datos
    rounds_created = []
    for round_num, round_pairings in enumerate(all_pairings, 1):
        # Creamos la ronda
        round_name = f"Ronda {round_num}"
        new_round = Round.objects.create(
            name=round_name,
            tournament=tournament,
            start_date=timezone.now()
        )
        rounds_created.append(new_round)

        # Creamos los juegos para esta ronda
        for i, pairing in enumerate(round_pairings):
            white_idx_1based, black_idx_1based = pairing
            # Convertimos a índices 0-based porque los índices
            # empiezan en 1 en el modelo
            white_idx_0based = white_idx_1based - 1
            black_idx_0based = black_idx_1based - 1

            white_player = players[white_idx_0based]
            black_player = players[black_idx_0based]

            Game.objects.create(
                white=white_player,
                black=black_player,
                round=new_round,
                result=Scores.NOAVAILABLE,
                rankingOrder=i
            )

    return rounds_created
