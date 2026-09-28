# cadastro/models.py

from django.db import models
from django.contrib.auth.models import User
from cloudinary_storage.storage import RawMediaCloudinaryStorage


class Musica(models.Model):
    titulo = models.CharField(max_length=200)
    artista = models.CharField(max_length=200)
    album = models.CharField(max_length=200, blank=True)
    ano = models.IntegerField(null=True, blank=True)
    capa_url = models.URLField(blank=True)
    tom = models.CharField(max_length=10, blank=True)
    letra_cifra = models.TextField(blank=True)
    enviado_por = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='musicas'
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.artista}"


class Naipe(models.Model):
    """Ex: Soprano, Contralto, Tenor, Baixo, Base instrumental, Click, Guia"""
    nome = models.CharField(max_length=50, unique=True)
    ordem = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome


class FaixaAudio(models.Model):
    musica = models.ForeignKey(Musica, related_name='faixas', on_delete=models.CASCADE)
    naipe = models.ForeignKey(Naipe, on_delete=models.CASCADE)
    audio = models.FileField(upload_to='faixas/', storage=RawMediaCloudinaryStorage())
    enviado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('musica', 'naipe')
        ordering = ['naipe__ordem']

    def __str__(self):
        return f"{self.musica.titulo} - {self.naipe.nome}"


class Contato(models.Model):
    nome = models.CharField(max_length=127)
    email = models.EmailField()
    assunto = models.CharField(max_length=255)
    mensagem = models.TextField()

    def __str__(self):
        return self.nome