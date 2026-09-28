# cadastro/admin.py

from django.contrib import admin
from .models import Contato, Musica, Naipe, FaixaAudio


@admin.register(Musica)
class MusicaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'artista', 'album', 'ano', 'enviado_por', 'criado_em')
    search_fields = ('titulo', 'artista')


@admin.register(Naipe)
class NaipeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ordem')
    ordering = ('ordem',)


@admin.register(FaixaAudio)
class FaixaAudioAdmin(admin.ModelAdmin):
    list_display = ('musica', 'naipe', 'enviado_por', 'criado_em')
    list_filter = ('naipe',)


admin.site.register(Contato)
