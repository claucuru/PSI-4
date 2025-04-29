from django.db import models


class Referee(models.Model):
    """
    Modelo que representa a un árbitro involucrado en partidas o torneos.
    Asumimos que hay un único árbitro por torneo.
    """
    name = models.CharField(max_length=128, verbose_name="Nombre del árbitro")
    refereeNumber = models.CharField(max_length=32, default="-1",
                                     verbose_name="Número de árbitro")

    class Meta:
        verbose_name = "Árbitro"
        verbose_name_plural = "Árbitros"
        constraints = [
            models.UniqueConstraint(fields=['refereeNumber'],
                                    name='unique_referee_number')]

    def __str__(self):
        """
        Representación en cadena del árbitro.
        """
        return f"{self.name} ({self.refereeNumber})"
