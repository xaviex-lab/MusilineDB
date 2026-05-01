# cadastro\models.py

from django.db import models

class Musica(models.Model):
    titulo = models.CharField(max_length=200)
    artista = models.CharField(max_length=200)
    album = models.CharField(max_length=200, blank=True)
    ano = models.IntegerField(null=True, blank=True)
    capa_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.titulo} - {self.artista}"

class Contato(models.Model):
    nome = models.CharField(max_length=127)
    email = models.EmailField()
    assunto = models.CharField(max_length=255)
    mensagem = models.TextField()

    def __str__(self):
        return self.nome