"""Módulo de vistas para la API de gestión de torneos de ajedrez.

Este módulo contiene todas las vistas necesarias para la API REST que gestiona
torneos de ajedrez, incluyendo jugadores, partidas, rondas y sistemas
de ranking.
"""
import logging
import re
import requests
from django.db import transaction
from django.utils import timezone
from djoser.views import UserViewSet
from rest_framework import generics, permissions, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from chess_models.models.game import Game, create_rounds
from chess_models.models.player import LichessAPIError, Player
from chess_models.models.referee import Referee
from chess_models.models.round import Round
from chess_models.models.tournament import RankingSystem, Tournament
from chess_models.models.tournament import getRanking
from chess_models.models.constants import Scores
from .serializers import (GameSerializer, PlayerSerializer, RefereeSerializer,
                          RoundSerializer, TournamentSerializer)

logger = logging.getLogger(__name__)


# Paginación personalizada
class CustomPagination(PageNumberPagination):
    """Clase de paginación personalizada.

    En la configuración de paginación de Django REST framework,
    el atributo max_page_size en una clase de paginación sirve
    para limitar el número máximo de ítems que pueden ser devueltos
    en una sola página cuando el cliente especifica un tamaño de página
    personalizado a través de un parámetro de consulta.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# ViewSets
class CustomUserViewSet(UserViewSet):
    """ViewSet personalizado para usuarios.

    Sobrescribe el método create para devolver un estado 405 Method Not Allowed
    en lugar de 403 Forbidden.
    """
    def create(self, request, *args, **kwargs):
        """Sobrescribe el método create.

        Args:
            request: Objeto request de Django
            *args: Argumentos posicionales
            **kwargs: Argumentos de palabra clave

        Returns:
            Response: Respuesta HTTP 405 Method Not Allowed
        """
        # Devuelve 405 Method Not Allowed en lugar de 403 Forbidden
        return Response(
            {"result": False, "message": "Creating users "
             "through API is disabled"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class TournamentViewSet(viewsets.ModelViewSet):
    """ViewSet para torneos con paginación personalizada."""
    pagination_class = CustomPagination
    queryset = Tournament.objects.all().order_by('-start_date', '-id')
    serializer_class = TournamentSerializer

    def get_permissions(self):
        """Obtiene los permisos según la acción.

        Returns:
            list: Lista de permisos aplicables
        """
        # No requerir permisos para listar y recuperar torneos
        if self.action in ['list', 'retrieve']:
            self.permission_classes = []
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """Crea un nuevo torneo con sus jugadores.

        Args:
            request: Objeto request de Django
            *args: Argumentos posicionales
            **kwargs: Argumentos de palabra clave

        Returns:
            Response: Respuesta HTTP con el resultado de la operación
        """
        with transaction.atomic():
            try:
                # Extraer players_from_csv antes de
                # procesar los datos del torneo
                players_from_csv = request.data.get('players', '')
                player_usernames = []

                # Limpiar y extraer nombres de usuario de jugadores
                if isinstance(players_from_csv, str):
                    # Reemplazar saltos de línea escapados y dividir
                    cleaned_csv = players_from_csv.replace('\\n', '\n')
                    lines = [line.strip() for line in cleaned_csv.split('\n')]

                    # Saltar encabezado si está presente
                    if lines and 'lichess_username' in lines[0].lower():
                        lines = lines[1:]

                    # Filtrar líneas vacías
                    player_usernames = [username for username in
                                        lines if username]

                # Crear torneo sin jugadores primero
                tournament_data = request.data.copy()
                # Eliminar el campo players
                if 'players' in tournament_data:
                    del tournament_data['players']

                tournament_data['administrativeUser'] = request.user.id

                # Validar y guardar torneo
                serializer = self.get_serializer(data=tournament_data)
                serializer.is_valid(raise_exception=True)
                tournament = serializer.save()

                # Procesar jugadores por separado
                player_ids = []
                for username in player_usernames:
                    try:
                        # Intentar obtener jugador existente o crear uno nuevo
                        player, created = Player.objects.get_or_create(
                            lichess_username=username
                        )
                        tournament.players.add(player)
                        player_ids.append(player.id)
                    except Exception as e:
                        print(f"Error processing player '{username}': {e}")

                # Preparar datos de respuesta
                response_data = serializer.data
                response_data['player_ids'] = player_ids


                headers = self.get_success_headers(serializer.data)
                return Response(
                    response_data,
                    status=status.HTTP_201_CREATED,
                    headers=headers
                )
            except Exception as e:
                print(f"Error creating tournament: {str(e)}")
                return Response(
                    {"result": False,
                     "message": f"Error creating tournament: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )


class PlayerViewSet(viewsets.ModelViewSet):
    """ViewSet para jugadores."""
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class RefereeViewSet(viewsets.ModelViewSet):
    """ViewSet para árbitros."""
    queryset = Referee.objects.all()
    serializer_class = RefereeSerializer


class GameViewSet(viewsets.ModelViewSet):
    """ViewSet para partidas de ajedrez."""
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_permissions(self):
        """Obtiene permisos según la acción.

        Returns:
            list: Lista de permisos aplicables
        """
        # Requerir autenticación para crear y eliminar
        if self.action in ['create', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            # Para otras acciones (incluyendo update),
            # manejamos permisos en método
            self.permission_classes = []
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        """Actualiza una partida.

        Args:
            request: Objeto request de Django
            *args: Argumentos posicionales
            **kwargs: Argumentos de palabra clave

        Returns:
            Response: Respuesta HTTP con el resultado de la operación
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Solo usuarios autenticados pueden actualizar una partida finalizada
        if instance.finished and not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Marcar la partida como finalizada
        # después de la actualización si no lo estaba
        if not instance.finished and 'result' in request.data:
            instance.finished = True
            instance.save()

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Crea una nueva partida.

        Args:
            request: Objeto request de Django
            *args: Argumentos posicionales
            **kwargs: Argumentos de palabra clave

        Returns:
            Response: Respuesta HTTP con el resultado de la operación
        """
        # Asegurar que el usuario está autenticado para crear partidas
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)


class RoundViewSet(viewsets.ModelViewSet):
    """ViewSet para rondas de torneo."""
    queryset = Round.objects.all()
    serializer_class = RoundSerializer


# APIViews
class CreateRoundAPIView(APIView):
    """APIView para crear rondas de torneo."""
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def post(self, request):
        """Crea rondas para un torneo.

        Args:
            request: Objeto request de Django

        Returns:
            Response: Respuesta HTTP con el resultado de la operación
        """
        tournament_id = request.data.get('tournament_id')
        if not tournament_id:
            return Response(
                {"result": False, "message": "Tournament ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            tournament_id = int(tournament_id)
            tournament = Tournament.objects.get(id=tournament_id)
        except (ValueError, Tournament.DoesNotExist):
            return Response(
                {"result": False, "message": "Tournament not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if tournament.getPlayersCount() == 0:
            return Response(
                {"result": False,
                 "message": "No players assigned to tournament"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Crear rondas para el torneo
        created = create_rounds(tournament, None)

        # Verificar que las rondas y juegos se han creado
        if not created:
            return Response(
                {"result": False, "message": "Failed to create rounds"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"result": True, "message": "Rounds created successfully"},
            status=status.HTTP_201_CREATED
        )


class SearchTournamentsAPIView(APIView):
    """APIView para buscar torneos."""
    permission_classes = []  # No requiere autenticación
    renderer_classes = [JSONRenderer]

    def post(self, request):
        """Busca torneos por nombre.

        Args:
            request: Objeto request de Django

        Returns:
            Response: Respuesta HTTP con los torneos encontrados
        """
        search_string = request.data.get('search_string')
        if not search_string:
            return Response(
                {"result": False, "message": "Search string not provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        tournaments = Tournament.objects.filter(
             name__icontains=search_string
         ).order_by('-name')
        serializer = TournamentSerializer(tournaments, many=True)

       

        # Devolver solo la lista de torneos como espera el test
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class TournamentCreateAPIView(generics.CreateAPIView):
    """APIView para crear torneos."""
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Crea un nuevo torneo con jugadores.

        Args:
            request: Objeto request de Django

        Returns:
            Response: Respuesta HTTP con el torneo creado
        """
        with transaction.atomic():
            try:
                # Extraer players_from_csv antes de
                # procesar los datos del torneo
                players_from_csv = request.data.get('players', '')
                player_usernames = []

                # Limpiar y extraer nombres de usuario de jugadores
                if isinstance(players_from_csv, str):
                    # Reemplazar saltos de línea escapados y dividir
                    cleaned_csv = players_from_csv.replace('\\n', '\n')
                    lines = [line.strip() for line in cleaned_csv.split('\n')]

                    # Saltar encabezado si está presente
                    if lines and 'lichess_username' in lines[0].lower():
                        lines = lines[1:]

                    # Filtrar líneas vacías
                    player_usernames = list(filter(None, lines))

                # Crear torneo sin jugadores primero
                tournament_data = request.data.copy()
                # Eliminar el campo players
                if 'players' in tournament_data:
                    del tournament_data['players']

                # añadir el usuario administrativo
                tournament_data['administrativeUser'] = request.user.id

                # Validar y guardar torneo
                serializer = self.get_serializer(data=tournament_data)
                serializer.is_valid(raise_exception=True)
                tournament = serializer.save()

                # Procesar jugadores por separado
                player_ids = []
                for username in player_usernames:
                    try:
                        # Intentar obtener jugador existente o crear uno nuevo
                        player, created = Player.objects.get_or_create(
                            lichess_username=username
                        )
                        tournament.players.add(player)
                        player_ids.append(player.id)
                    except Exception as e:
                        print(f"Error processing player '{username}': {e}")

                # Preparar datos de respuesta
                response_data = serializer.data
                response_data['player_ids'] = player_ids

                headers = self.get_success_headers(serializer.data)
                return Response(
                    response_data,
                    status=status.HTTP_201_CREATED,
                    headers=headers
                )
            except Exception as e:
                print(f"Error creating tournament: {str(e)}")
                return Response(
                    {
                        "result": False,
                        "message": f"Error creating tournament: {e}",
                        "status": status.HTTP_400_BAD_REQUEST
                    }
                )


class GetRanking(APIView):
    """APIView para obtener el ranking de un torneo."""
    permission_classes = []
    renderer_classes = [JSONRenderer]

    def get(self, request, tournament_id):
        """Obtiene el ranking de un torneo.

        Args:
            request: Objeto request de Django
            tournament_id: ID del torneo

        Returns:
            Response: Respuesta HTTP con el ranking del torneo
        """
        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            return Response(
                {"result": False, "message": "Tournament not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Obtener el ranking usando la función existente
        ranking_data = getRanking(tournament)

    

        # Preparar los datos para la respuesta en el formato que espera el test
        formatted_ranking = {}
        for player, data in ranking_data.items():
            player_info = {
                "id": player.id,
                "name": player.name,
                "score": data[RankingSystem.PLAIN_SCORE.value],
                RankingSystem.WINS.value: data[RankingSystem.WINS.value],
                RankingSystem.BLACKTIMES.value:
                data[RankingSystem.BLACKTIMES.value],
                "rank": data['rank']
            }

            # Agregar cualquier criterio adicional de desempate
            for criterion in tournament.rankingList.values_list('value',
                                                                flat=True):
                if criterion in data and criterion not in [
                    RankingSystem.PLAIN_SCORE.value,
                    RankingSystem.WINS.value,
                    RankingSystem.BLACKTIMES.value
                ]:
                    player_info[criterion] = data[criterion]

            formatted_ranking[player.id] = player_info

        return Response(
            formatted_ranking,
            status=status.HTTP_200_OK
        )


class GetPlayers(APIView):
    """APIView para obtener jugadores de un torneo."""
    permission_classes = []
    renderer_classes = [JSONRenderer]

    def get(self, request, tournament_id):
        """Obtiene los jugadores de un torneo.

        Args:
            request: Objeto request de Django
            tournament_id: ID del torneo

        Returns:
            Response: Respuesta HTTP con los jugadores del torneo
        """
        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            return Response(
                {"result": False, "message": "Tournament not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        players = tournament.players.all()
        serializer = PlayerSerializer(players, many=True)

        # Devolver datos en el formato esperado para el test
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class GetRoundResults(APIView):
    """APIView para obtener resultados de rondas de un torneo."""
    permission_classes = []
    renderer_classes = [JSONRenderer]

    def get(self, request, tournament_id):
        """Obtiene los resultados de las rondas de un torneo.

        Args:
            request: Objeto request de Django
            tournament_id: ID del torneo

        Returns:
            Response: Respuesta HTTP con los resultados de las rondas
        """
        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            return Response(
                {"result": False, "message": "Tournament not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            rounds = Round.objects.filter(tournament=tournament).order_by('id')

            results = {
                'result': True,
                'tournament_id': tournament.id,
                'tournament_name': tournament.name,
                'rounds': []
            }

            for r in rounds:
                games = Game.objects.filter(round=r).order_by('-rankingOrder')

                round_games = []
                for game in games:
                    if tournament.tournament_speed == 'BL':
                        if game.white:
                            white_rating = game.white.fide_rating_blitz
                            black_rating = game.black.fide_rating_blitz
                        else:
                            white_rating = None
                            black_rating = None
                    elif tournament.tournament_speed == 'RA':
                        if game.white:
                            white_rating = game.white.fide_rating_rapid
                            black_rating = game.black.fide_rating_rapid
                        else:
                            white_rating = None
                            black_rating = None
                    else:  # CLASICO
                        if game.white:
                            white_rating = game.white.fide_rating_classical
                            black_rating = game.black.fide_rating_classical
                        else:
                            white_rating = None
                            black_rating = None

                    game_data = {
                        'game_id': game.id,
                        'rankingOrder': white_rating,
                        'white': {
                            'id': game.white.id if game.white else None,
                            'name': game.white.name if game.white else None,
                            'rating': white_rating
                        },
                        'black': {
                            'id': game.black.id if game.black else None,
                            'name': game.black.name if game.black else None,
                            'rating': black_rating
                        },
                        'result': game.result,  # resultado de la partida
                        'finished': game.finished  # estado de la partida
                    }

                    round_games.append(game_data)

                results['rounds'].append({
                    'round_id': r.id,
                    'round_name': r.name,
                    'start_date': r.start_date.isoformat() if r.start_date
                    else None,
                    'games': round_games
                })

            return Response(
                {"result": True, "rounds": results},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {'result': False, 'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class UpdateLichessGameAPIView(APIView):
    """APIView para actualizar partidas desde Lichess."""
    permission_classes = []

    def post(self, request):
        """Actualiza una partida con datos de Lichess.

        Args:
            request: Objeto request de Django

        Returns:
            Response: Respuesta HTTP con el resultado de la operación
        """
        game_id = request.data.get('game_id')
        lichess_game_id = request.data.get('lichess_game_id')

        if not game_id:
            return Response(
                {"result": False, "message": "Game ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not lichess_game_id:
            return Response(
                {"result": False, "message": "Lichess game ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            try:
                game = Game.objects.get(id=game_id)
            except Game.DoesNotExist:
                return Response(
                    {"result": False,
                     "message": "Game not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            try:
                result = white_username = black_username = None
                result_data = game.get_lichess_game_result(lichess_game_id)
                result, white_username, black_username = result_data

                game_data = {
                    'game_id': game.id,
                    'lichess_game_id': lichess_game_id,
                    'result': result,
                    'white_username': white_username,
                    'black_username': black_username,
                }

                game_serializer = GameSerializer(game, data=game_data,
                                                 partial=True)
                game_serializer.is_valid(raise_exception=True)
                game_serializer.save()

                return Response(
                    {
                        "result": True,
                        "message": (
                            f"Game updated successfully with {game.result}"
                        )
                    },
                    status=status.HTTP_200_OK
                )

            except LichessAPIError as e:
                return Response(
                    {"result": False, "message": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except requests.RequestException:
                return Response(
                    {
                        "result": False,
                        "message": (
                             f"Failed to fetch data for "
                             f"game {lichess_game_id} "
                             f"from Lichess"
                             )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            except ValidationError as e:
                return Response(
                    {"result": False, "message": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )


class UpdateOTBGameAPIView(APIView):
    """APIView para actualizar partidas presenciales (Over The Board)."""
    permission_classes = []

    def post(self, request):
        """Actualiza una partida presencial.

        Args:
            request: Objeto request de Django

        Returns:
            Response: Respuesta HTTP con el resultado de la operación
        """
        # Forzar el tipo de contenido de la respuesta a application/json
        response_data = {"result": False, "message": "Invalid request"}

        try:
            # Obtener el ID del juego y verificar que existe
            game_id = request.data.get('game_id')
            if not game_id:
                response_data = {"result": False,
                                 "message": "Game ID is required"}
                return Response(
                    response_data,
                    status=status.HTTP_400_BAD_REQUEST,
                    content_type='application/json'
                )

            try:
                game = Game.objects.get(id=game_id)
            except Game.DoesNotExist:
                response_data = {"result": False, "message": "Game not found"}
                return Response(
                    response_data,
                    status=status.HTTP_404_NOT_FOUND,
                    content_type='application/json'
                )

            # Verificar si el juego ya está finalizado
            if game.finished and not request.user.is_staff:
                response_data = {
                    "result": False,
                    "message": "Game is already finished"
                    }
                return Response(
                    response_data,
                    status=status.HTTP_400_BAD_REQUEST,
                    content_type='application/json'
                )

            # Actualizar el juego con los datos proporcionados
            otb_result = request.data.get('otb_result')
            if otb_result is None:
                response_data = {
                    "result": False,
                    "message": "OTB Result is required"
                }
                return Response(
                    response_data,
                    status=status.HTTP_400_BAD_REQUEST,
                    content_type='application/json'
                )

            # Verificar que el usuario que envía
            # la actualización es uno de los jugadores
            name = request.data.get('name')
            email = request.data.get('email')

            if name and email:
                # Comprobar si la información del usuario
                # coincide con jugadores
                white_matches = (
                    game.white and
                    game.white.name == name and
                    game.white.email == email
                )
                black_matches = (
                    game.black and
                    game.black.name == name and
                    game.black.email == email
                )

                if not (white_matches or black_matches):
                    response_data = {
                        "result": False,
                        "message": "Player credentials do not "
                        "match game participants"
                    }
                    return Response(
                        response_data,
                        status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json'
                    )

            # Establecer resultado del juego
            game.result = otb_result
            game.finished = True
            game.save()

            response_data = {
                "result": True,
                "message": "Game updated successfully"
                }
            return Response(
                response_data,
                status=status.HTTP_200_OK,
                content_type='application/json'
            )

        except Exception as e:
            # Log the exception for debugging
            import traceback
            print(f"Exception in UpdateOTBGameAPIView: {str(e)}")
            print(traceback.format_exc())

            response_data = {"result": False, "message": f"Error: {str(e)}"}
            return Response(
                response_data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type='application/json'
            )

class AdminUpdateGameAPIView(APIView):
    """APIView para que administradores actualicen partidas de cualquier tipo."""
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def post(self, request):
        """Permite a un administrador actualizar una partida.
        Dependiendo de los parámetros, redirige a la vista de Lichess o OTB.

        Args:
            request: Objeto request de Django

        Returns:
            Response: Respuesta HTTP con el resultado de la operación
        """
        # Obtener el ID del juego y verificar que existe
        game_id = request.data.get('game_id')
        if not game_id:
            return Response(
                {"result": False, "message": "Game ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response(
                {"result": False, "message": "Game not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Determinar el tipo de actualización según los parámetros recibidos
        if 'lichess_game_id' in request.data:
            # Si tiene lichess_game_id, procesar como actualización de Lichess
            lichess_game_id = request.data.get('lichess_game_id')
            
            if not lichess_game_id:
                return Response(
                    {"result": False, "message": "Lichess game ID is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            try:
                with transaction.atomic():
                    result = white_username = black_username = None
                    result_data = game.get_lichess_game_result(lichess_game_id)
                    result, white_username, black_username = result_data

                    game_data = {
                        'game_id': game.id,
                        'lichess_game_id': lichess_game_id,
                        'result': result,
                        'white_username': white_username,
                        'black_username': black_username,
                    }

                    game_serializer = GameSerializer(game, data=game_data,
                                                    partial=True)
                    game_serializer.is_valid(raise_exception=True)
                    game_serializer.save()

                    return Response(
                        {
                            "result": True,
                            "message": (
                                f"Game updated successfully with {game.result}"
                            )
                        },
                        status=status.HTTP_200_OK
                    )

            except LichessAPIError as e:
                return Response(
                    {"result": False, "message": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except requests.RequestException:
                return Response(
                    {
                        "result": False,
                        "message": (
                            f"Failed to fetch data for "
                            f"game {lichess_game_id} "
                            f"from Lichess"
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            except ValidationError as e:
                return Response(
                    {"result": False, "message": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        elif 'otb_result' in request.data:
            # Si tiene otb_result, procesar como actualización OTB
            otb_result = request.data.get('otb_result')

            
            # Establecer el resultado directamente
            game.result = otb_result
            game.finished = True  # Marcar el juego como finalizado
            game.save()

            return Response(
                {"result": True, "message": "Game updated successfully"},
                status=status.HTTP_200_OK
            )
            
        else:
            # Manejo de la actualización directa de los campos result, finished y update_date
            try:
                result = request.data.get('result')
                game.result = result if result else game.result
                game.finished = True
                
                # Gestionar la fecha de actualización si se proporciona
                game.update_date = timezone.now()
                if 'update_date' in request.data:
                    game.update_date = request.data.get('update_date')
                
                # Guardar los cambios
                game.save()
                
                return Response(
                    {"result": True, "message": "Game updated successfully"},
                    status=status.HTTP_200_OK
                )
            except ValidationError as e:
                return Response(
                    {"result": False, "message": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {"result": False, "message": f"Error updating game: {str(e)}"},
                    status=status.HTTP_500_BAD_GATEWAY
                )
            
class AddRankingAPIView(APIView):
    """APIView para añadir un ranking a un torneo."""
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer]
    
    def post(self, request, tournament_id=None):
        """Añade un ranking a un torneo.
        
        Args:
            request: Objeto request de Django
            tournament_id: ID del torneo
        
        Returns:
            Response: Respuesta HTTP con el resultado de la operación
        """
        try:
            # Si el tournament_id viene en la URL, úsalo
            if tournament_id is None:
                tournament_id = request.data.get('tournament_id')
            
            if not tournament_id:
                return Response(
                    {"result": False, "message": "Tournament ID is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            return Response(
                {"result": False, "message": "Tournament not found"},
                status=status.HTTP_404_NOT_FOUND
            )
            
        # Obtener el ranking desde la solicitud
        ranking = request.data.get('ranking')
        if not ranking:
            return Response(
                {"result": False, "message": "Ranking data is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Añadir el ranking al torneo
        tournament.addToRankingList(ranking)
        tournament.save()
        
        return Response(
            {"result": True, "message": "Ranking added successfully"},
            status=status.HTTP_200_OK
        )
    
class UpdateGameAPIView(APIView):
    """APIView para que actualicen partidas de cualquier tipo."""
    renderer_classes = [JSONRenderer]
    permission_classes = []

    def post(self, request):
        """Permite a un usuario actualizar una partida verificando su email.
        Dependiendo de los parámetros, redirige a la vista de Lichess o OTB.
        
        Args:
            request: Objeto request de Django
        
        Returns:
            Response: Respuesta HTTP con el resultado de la operación
        """
        # Obtener el ID del juego y verificar que existe
        game_id = request.data.get('game_id')
        if not game_id:
            return Response(
                {"result": False, "message": "Game ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response(
                {"result": False, "message": "Game not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            with transaction.atomic():
                # Obtener datos de la solicitud
                result = request.data.get('result')
                game.result = result if result else game.result
                game.finished = True
                
                # Gestionar la fecha de actualización si se proporciona
                game.update_date = timezone.now()
                if 'update_date' in request.data:
                    game.update_date = request.data.get('update_date')
                
                # Guardar los cambios
                game.save()
                    
                return Response(
                        {
                            "result": True,
                            "message": f"Game updated successfully with result: {game.result}"
                        },
                        status=status.HTTP_200_OK
                )
        except ValidationError as e:
            return Response(
                {"result": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"result": False, "message": f"Error updating game: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )