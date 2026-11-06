# cadastro\admin.py

from django.contrib import admin
from .models import Contato, Musica

admin.site.register(Musica)
admin.site.register(Contato)
