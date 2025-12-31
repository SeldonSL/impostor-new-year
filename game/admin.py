from django.contrib import admin

from .models import Concept, Game


@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    list_display = ('text', 'used')
    list_filter = ('used',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('short_id', 'concept', 'number_of_players', 'impostor')
    readonly_fields = ('short_id',)
