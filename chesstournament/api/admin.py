from django.contrib import admin

# Register your models here.
from chess_models.models.tournament import Tournament
from chess_models.models.player import Player
from chess_models.models.referee import Referee
from chess_models.models.game import Game
from chess_models.models.round import Round

admin.site.register(Tournament)
admin.site.register(Player)
admin.site.register(Referee)
admin.site.register(Game)
admin.site.register(Round)
