# cadastro\views.py

from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from cadastro.forms import MusicaForm, ContatoForm
from cadastro.models import Musica
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    busca = request.GET.get('q', '')
    if busca:
        musicas = Musica.objects.filter(
            Q(titulo__icontains=busca) | Q(artista__icontains=busca)
        ).order_by('titulo')
    else:
        musicas = Musica.objects.order_by('titulo')
    total = Musica.objects.count()
    context = {
        'musicas': musicas,
        'total': total,
        'busca': busca,
    }
    return render(request, 'cadastro/index.html', context)


def busca_ajax(request):
    q = request.GET.get('q', '')
    musicas = Musica.objects.filter(
        Q(titulo__icontains=q) | Q(artista__icontains=q)
    ).order_by('titulo')[:8]
    resultado = [
        {
            'id': m.id,
            'titulo': m.titulo,
            'artista': m.artista,
            'capa_url': m.capa_url,
        }
        for m in musicas
    ]
    return JsonResponse({'musicas': resultado})


@login_required
def adicionar(request):
    if request.method == 'POST':
        form = MusicaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Música adicionada com sucesso!')
            return redirect('index')
    else:
        form = MusicaForm()
    return render(request, 'cadastro/adicionar.html', {'form': form})


def detalhe(request, id):
    musica = get_object_or_404(Musica, id=id)
    return render(request, 'cadastro/detalhe.html', {'musica': musica})


@login_required
def editar(request, id):
    musica = get_object_or_404(Musica, id=id)
    if request.method == 'POST':
        form = MusicaForm(request.POST, instance=musica)
        if form.is_valid():
            form.save()
            messages.success(request, f'{musica.titulo} atualizada com sucesso!')
            return redirect('detalhe', id=id)
    else:
        form = MusicaForm(instance=musica)
    return render(request, 'cadastro/editar.html', {
        'form': form,
        'musica': musica,
    })


@login_required
def deletar(request, id):
    musica = get_object_or_404(Musica, id=id)
    if request.method == 'POST':
        musica.delete()
        messages.success(request, 'Música apagada com sucesso!')
        return redirect('index')
    return render(request, 'cadastro/deletar.html', {'musica': musica})

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Conta criada com sucesso! Bem-vindo, {user.username}!')
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})


def contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contato enviado com sucesso!')
            return redirect('contato')
    else:
        form = ContatoForm()
    return render(request, 'cadastro/contato.html', {'form': form})