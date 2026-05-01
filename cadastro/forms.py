# cadastro\forms.py

from django import forms
from .models import Contato, Musica


class MusicaForm(forms.ModelForm):
    class Meta:
        model = Musica
        fields = ['titulo', 'artista', 'album', 'ano', 'capa_url']
        labels = {
            'titulo': 'Nome da faixa',
            'artista': 'Artista',
            'album': 'Álbum',
            'ano': 'Ano',
            'capa_url': 'URL da Capa',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'artista': forms.TextInput(attrs={'class': 'form-control'}),
            'album': forms.TextInput(attrs={'class': 'form-control'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'capa_url': forms.URLInput(attrs={'class': 'form-control'}),
        }


class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'assunto', 'mensagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'assunto': forms.TextInput(attrs={'class': 'form-control'}),
            'mensagem': forms.Textarea(attrs={'class': 'form-control'}),
        }