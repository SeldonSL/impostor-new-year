import random
import string

from django.contrib.auth.models import User
from django.db import models


class Concept(models.Model):
    text = models.TextField()
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:50]


class Game(models.Model):
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE)
    number_of_players = models.PositiveIntegerField()
    impostor = models.ForeignKey(User, on_delete=models.CASCADE)
    short_id = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return f"Game {self.short_id}"

    @staticmethod
    def generate_short_id():
        while True:
            short_id = ''.join(random.choices(string.ascii_uppercase, k=4))
            if not Game.objects.filter(short_id=short_id).exists():
                return short_id
