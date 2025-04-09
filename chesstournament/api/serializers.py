from rest_framework import serializers
from django.contrib.auth.models import User
from chess_models.models.tournament import Tournament
from chess_models.models.player import Player
from chess_models.models.referee import Referee
from chess_models.models.game import Game
from chess_models.models.round import Round


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


class RefereeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referee
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'


class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = '__all__'
