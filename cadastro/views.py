# cadastro\views.py

from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.paginator import Paginator
from cadastro.forms import MusicaForm, ContatoForm
from cadastro.models import Musica
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    busca = request.GET.get('q', '')
    pagina = request.GET.get('pagina', 1)
    formato = request.GET.get('formato', '')

    if busca:
        musicas_lista = Musica.objects.filter(
            Q(titulo__icontains=busca) | Q(artista__icontains=busca)
        ).order_by('titulo')
    else:
        musicas_lista = Musica.objects.order_by('titulo')

    total = Musica.objects.count()
    paginador = Paginator(musicas_lista, 5)
    musicas = paginador.get_page(pagina)

    if formato == 'ajax':
        resultado = [
            {
                'id': m.id,
                'titulo': m.titulo,
                'artista': m.artista,
                'capa_url': m.capa_url,
            }
            for m in musicas
        ]
        return JsonResponse({
            'musicas': resultado,
            'tem_proxima': musicas.has_next(),
            'proxima_pagina': musicas.next_page_number() if musicas.has_next() else None,
        })

    context = {
        'musicas': musicas,
        'total': total,
        'busca': busca,
    }
    return render(request, 'cadastro/index.html', context)


@login_required
def adicionar(request):
    if request.method == 'POST':
        form = MusicaForm(request.POST)
        if form.is_valid():
            musica = form.save(commit=False)
            musica.enviado_por = request.user
            musica.save()
            messages.success(request, 'Música adicionada com sucesso!')
            return redirect('index')
    else:
        form = MusicaForm()
    return render(request, 'cadastro/adicionar.html', {'form': form})


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


from cadastro.forms import MusicaForm, ContatoForm, RegistroForm

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            login(request, user)
            messages.success(request, f'Conta criada com sucesso! Bem-vindo, {user.username}!')
            return redirect('index')
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})

@login_required
def perfil(request):
    musicas_do_usuario = Musica.objects.filter(enviado_por=request.user).order_by('titulo')
    total_musicas = musicas_do_usuario.count()
    return render(request, 'cadastro/perfil.html', {
        'total_musicas': total_musicas,
        'musicas_do_usuario': musicas_do_usuario,
    })

@login_required
def editar_username(request):
    if request.method == 'POST':
        novo_username = request.POST.get('username', '').strip()
        if novo_username:
            request.user.username = novo_username
            request.user.save()
            messages.success(request, 'Nome de usuário atualizado com sucesso!')
        else:
            messages.error(request, 'Nome de usuário não pode ser vazio!')
    return redirect('perfil')

@login_required
def deletar_conta(request):
    if request.method == 'POST':
        user = request.user
        auth_logout(request)
        user.delete()
        messages.success(request, 'Conta deletada com sucesso!')
        return redirect('index')
    return redirect('perfil')

from cadastro.forms import MusicaForm, ContatoForm, RegistroForm


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