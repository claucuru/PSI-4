from django.db import models
from django.utils import timezone
from .tournament import Tournament


class Round(models.Model):
    """Modelo que representa una ronda de un torneo.

    Atributos:
        name (str): Nombre de la ronda.
        tournament (Tournament): Torneo al que pertenece la ronda.
        start_date (datetime): Fecha y hora de inicio de la ronda.
        end_date (datetime): Fecha y hora de fin de la ronda.
        finish (bool): Indica si la ronda ha terminado o no.
    """
    name = models.CharField(max_length=128)
    tournament = models.ForeignKey(Tournament,
                                   on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    finish = models.BooleanField(default=False)

    def __str__(self):
        """Devuelve una representación en cadena del objeto Round."""
        return self.name
