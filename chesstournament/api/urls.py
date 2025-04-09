from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tournaments', views.TournamentViewSet)
router.register(r'players', views.PlayerViewSet)
router.register(r'referees', views.RefereeViewSet)
router.register(r'games', views.GameViewSet)
router.register(r'rounds', views.RoundViewSet)
router.register(r'users', views.CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Tournament API endpoints
    path('tournament_create/', views.TournamentCreateAPIView.as_view()),
    path('create_round/', views.CreateRoundAPIView.as_view()),
    path('searchTournaments/', views.SearchTournamentsAPIView.as_view()),
    path('get_ranking/<int:tournament_id>/', views.GetRanking.as_view()),
    path('get_players/<int:tournament_id>/', views.GetPlayers.as_view()),
    path('get_round_results/<int:tournament_id>/',
         views.GetRoundResults.as_view()),
    # Game update endpoints
    path('update_lichess_game/', views.UpdateLichessGameAPIView.as_view()),
    path('update_otb_game/', views.UpdateOTBGameAPIView.as_view()),
    path('admin_update_game/', views.AdminUpdateGameAPIView.as_view()),
    # Authentication endpoints
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]
