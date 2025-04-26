from django.db import models
import requests


class LichessAPIError(Exception):
    """Excepción que se lanza cuando hay un error con la API de Lichess."""
    pass


class Player(models.Model):
    """Modelo que representa a un jugador de ajedrez.
    Atributos:
        name (str): Nombre del jugador.
        email (str): Correo electrónico del jugador.
        country (str): País del jugador.
        lichess_username (str): Nombre de usuario en Lichess.
        lichess_rating_bullet (int): Rating de bullet en Lichess.
        lichess_rating_blitz (int): Rating de blitz en Lichess.
        lichess_rating_rapid (int): Rating de rapid en Lichess.
        lichess_rating_classical (int): Rating de classical en Lichess.
        fide_id (int): Identificador FIDE del jugador.
        fide_rating_blitz (int): Rating de blitz en FIDE.
        fide_rating_rapid (int): Rating de rapid en FIDE.
        fide_rating_classical (int): Rating de classical en FIDE.
        creation_date (datetime): Fecha de creación del jugador.
        update_date (datetime): Fecha de última actualización del jugador.
    """

    name = models.CharField(max_length=256)
    email = models.EmailField()
    country = models.CharField(max_length=2, blank=True, default='')
    lichess_username = models.CharField(
        max_length=150, unique=True, blank=True, null=True
    )
    lichess_rating_bullet = models.IntegerField(default=0)
    lichess_rating_blitz = models.IntegerField(default=0)
    lichess_rating_rapid = models.IntegerField(default=0)
    lichess_rating_classical = models.IntegerField(default=0)
    fide_id = models.IntegerField(unique=True, null=True, blank=True)
    fide_rating_blitz = models.IntegerField(default=0)
    fide_rating_rapid = models.IntegerField(default=0)
    fide_rating_classical = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Guarda el jugador en la base de datos.
        Si el jugador ya existe, actualiza los datos y mantiene el id.
        Si el jugador no existe, lo crea.
        También obtiene los ratings de Lichess si el nombre de usuario existe.
        """
        # Bandera para evitar la recursión
        update_lichess_ratings = kwargs.pop('update_lichess_ratings', True)

        # Creamos una query vacía
        query = models.Q()

        # Añadimos condiciones a la query si existen los valores
        if self.id:
            query = query | models.Q(id=self.id)

        if self.lichess_username:
            query = query | models.Q(lichess_username=self.lichess_username)

        if self.fide_id:
            query = query | models.Q(fide_id=self.fide_id)

        if self.email and self.name:
            query = query | models.Q(email=self.email, name=self.name)

        if self.lichess_username and not self.name:
            self.name = self.lichess_username

        # Solo buscamos si tenemos condiciones en la query
        jugador_existente = None
        if query:
            jugador_existente = Player.objects.filter(query).first()

        # Si el jugador ya existe, actualizamos los datos y mantenemos el id
        if jugador_existente:
            self.id = jugador_existente.id
            self.creation_date = jugador_existente.creation_date
            super().save(*args, **kwargs)
        else:
            # Creamos el nuevo jugador
            super().save(*args, **kwargs)

        # Solo actualizamos los ratings de lichess si el username existe
        # y la bandera está activa
        if self.lichess_username and self.lichess_username.strip() and update_lichess_ratings:
            self.get_lichess_user_ratings()

    def check_lichess_user_exists(self):
        """Verifica si el usuario de lichess existe."""
        if not self.lichess_username or not self.lichess_username.strip():
            # Si el username está vacío o es solo espacios, no existe
            return False

        url = f"https://lichess.org/api/user/{self.lichess_username}"
        response = requests.get(url)

        # El usuario existe
        return response.status_code == 200

    def get_lichess_user_ratings(self):
        """Obtiene los ratings de lichess para el usuario."""
        if not self.lichess_username:
            return

        url = f"https://lichess.org/api/user/{self.lichess_username}"
        response = requests.get(url)

        if response.status_code == 200:  # ¿existe el usuario?
            data = response.json()
            perfs = data.get('perfs', {})
            # procesamos los datos
            self.lichess_rating_bullet = perfs.get('bullet', {}).get(
                'rating', 0)
            self.lichess_rating_blitz = perfs.get('blitz', {}).get('rating', 0)
            self.lichess_rating_rapid = perfs.get('rapid', {}).get('rating', 0)
            self.lichess_rating_classical = perfs.get(
                'classical', {}).get('rating', 0)
            # Llamamos a save con update_lichess_ratings=False
            # para evitar recursión infinita
            self.save(update_lichess_ratings=False)
        else:  # el usuario no existe
            # Lanzamos una excepción como espera el test
            raise LichessAPIError(
                f"El usuario de Lichess '{self.lichess_username}' no existe"
            )

    def __str__(self):
        """Devuelve el username de lichess como representación en cadena."""
        return self.lichess_username if self.lichess_username else self.name
