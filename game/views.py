import random

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Concept, Game


def home(request):
    return render(request, 'game/home.html')


@require_http_methods(["GET", "POST"])
def start_game(request):
    if request.method == 'POST':
        number_of_players = int(request.POST.get('number_of_players', 0))

        if number_of_players < 2:
            return render(request, 'game/start_game.html', {
                'error': 'Se requieren al menos 2 jugadores'
            })

        available_concepts = Concept.objects.filter(used=False)
        if not available_concepts.exists():
            return render(request, 'game/start_game.html', {
                'error': 'No hay conceptos disponibles. Por favor agrega conceptos en el admin.'
            })

        users = User.objects.all()
        if not users.exists():
            return render(request, 'game/start_game.html', {
                'error': 'No hay usuarios disponibles. Por favor agrega usuarios en el admin.'
            })

        concept = random.choice(list(available_concepts))
        impostor = random.choice(list(users))
        short_id = Game.generate_short_id()

        Game.objects.create(
            concept=concept,
            number_of_players=number_of_players,
            impostor=impostor,
            short_id=short_id
        )

        concept.used = True
        concept.save()

        return render(request, 'game/game_created.html', {'short_id': short_id})

    return render(request, 'game/start_game.html')


@require_http_methods(["GET", "POST"])
def join_game(request):
    users = User.objects.all()

    if request.method == 'POST':
        game_id = request.POST.get('game_id', '').upper()
        user_id = request.POST.get('user_id')

        try:
            game = Game.objects.get(short_id=game_id)
        except Game.DoesNotExist:
            return render(request, 'game/join_game.html', {
                'users': users,
                'error': 'Partida no encontrada'
            })

        try:
            selected_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return render(request, 'game/join_game.html', {
                'users': users,
                'error': 'Usuario no encontrado'
            })

        is_impostor = (selected_user == game.impostor)

        return render(request, 'game/reveal.html', {
            'is_impostor': is_impostor,
            'concept': game.concept.text if not is_impostor else None,
            'player_name': f"{selected_user.first_name} {selected_user.last_name}".strip() or selected_user.username
        })

    return render(request, 'game/join_game.html', {'users': users})
