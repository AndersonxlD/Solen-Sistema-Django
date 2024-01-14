from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login
from django.contrib import messages
from django.http.response import Http404, JsonResponse
from django.contrib import messages
from datetime import datetime, timedelta, date
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.shortcuts import get_object_or_404
from django.template import loader
from app_solen.forms import UserRegistrationForm, EnviosNFsForm
import csv

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from app_solen.models import MyUser, EnviosNFs

def login_view(request):
    return render(request, 'login.html')

def submit_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Usuário ou senha inválidos")
    return redirect('login')

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso.')
            form = UserRegistrationForm()
        else:
            messages.error(request, 'Erro ao enviar o formulário. Verifique os dados!')
    else:
        form = UserRegistrationForm()

    usuarios = MyUser.objects.all()
    context = {
        'form': form,
        'usuarios':usuarios
    }
    return render(request, 'register.html', context)


@login_required(login_url='login') 
def delete_user(request, id):
    usuarios = MyUser.objects.get(id=id)
    usuarios.delete()
    messages.success(request, "Usuario excluido!")
    return redirect('register')

@login_required(login_url='login') 
def editar_user(request, id):
    
    usuarios = MyUser.objects.get(id=id)

    if request.method == 'POST':
        # Receba os dados do formulário
        novo_email = request.POST.get('email')
        novo_telefone = request.POST.get('telefone')
        novo_fornecedor = request.POST.get('nome_fornecedor')
        novo_tipo_usuario = request.POST.get('tipo_usuario')
        novo_is_active = request.POST.get('is_active')

        usuarios.email = novo_email
        usuarios.telefone = novo_telefone
        usuarios.nome_fornecedor = novo_fornecedor
        usuarios.tipo_usuario = novo_tipo_usuario
        usuarios.is_active = novo_is_active

        usuarios.save()
        messages.success(request, "Usuário alterado!")
        return redirect('register')
    
    context = {
        'usuarios':usuarios
    }
    return render(request, 'register.html',context)
    

@login_required(login_url='login')
def index(request):
    return render(request, "index.html")

@login_required(login_url='login')
def envios_nfs(request):
    if request.method == 'POST':
        form = EnviosNFsForm(request.POST, request.FILES)
        if form.is_valid():
            envios_nfs = form.save(commit=False)
            envios_nfs.usuario = request.user
            envios_nfs.save()
            messages.success(request, "Enviado com sucesso!")
            return redirect('envios_nfs')
    else:
        form = EnviosNFsForm()
    context = {
        'form':form,
    }
    return render(request, 'envios.html',context)

@login_required(login_url='login')
def meus_envios(request):
    usuario = request.user
    envios = EnviosNFs.objects.filter(usuario=usuario)
    context = {
        'envios':envios,
    }
    return render(request, "meus_envios.html", context)

@login_required(login_url='login')
def editar_envios(request, id):
    envios = EnviosNFs.objects.get(id=id)
    
    if request.method == 'POST':
        novo_pedido = request.POST.get('pedido_compras')
        novo_nf = request.POST.get('nota_num')
        novo_solicitante = request.POST.get('solicitante')

        envios.pedido_compras = novo_pedido
        envios.nota_num = novo_nf
        envios.solicitante = novo_solicitante

        # Verificar se um arquivo foi enviado antes de tentar acessá-lo
        if 'pdf_nota' in request.FILES:
            novo_anexo = request.FILES['pdf_nota']
            envios.pdf_nota = novo_anexo

        envios.save()
        messages.success(request, "Envio alterado!")
        return redirect('meus_envios')
    
    context = {
        'envios': envios
    }
    return render(request, 'meus_envios.html', context)

@login_required(login_url='login')
def cancelar_nf(request,id):
    envios = EnviosNFs.objects.get(id=id)

    envios.status_envio = 'Cancelada'
    envios.save()

    messages.success(request, "NF Cancelada com sucesso")
    return redirect('meus_envios')

@login_required(login_url='login')
def todos_envios(request):
    todos_envios = EnviosNFs.objects.select_related('usuario').all()

    context = {
        'todos_envios':todos_envios
    }
    return render(request, 'todos_envios.html',context)

@login_required(login_url='login')
def exportar_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="envios.csv"'

    writer = csv.writer(response)
    writer.writerow(['Pedido de Compras', 'Nota Fiscal', 'Anexo', 'Destino', 'Solicitante', 'Fornecedor', 'Data de Envio', 'Status'])

    envios = EnviosNFs.objects.select_related('usuario').all()

    for envio in envios:
        writer.writerow([envio.pedido_compras, envio.nota_num, envio.pdf_nota.url if envio.pdf_nota else 'Nenhum anexo disponível', envio.empresa_destinataria, envio.solicitante, envio.usuario.nome_fornecedor, envio.get_data_criacao(), envio.status_envio])

    return response

@login_required(login_url='login')
def compras_envios(request):
    envios = EnviosNFs.objects.select_related('usuario').filter(status_envio='Ag Compras')

    context = {
        'envios':envios
    }
    return render(request, "envios_compras.html", context)

@login_required(login_url='login')
def envio_ajustado_compras(request, id):
    envios = EnviosNFs.objects.get(id=id)

    envios.status_envio = 'Ag Fiscal'
    envios.save()

    messages.success(request, "Status alterado com sucesso!")
    return redirect('compras_envios')

@login_required(login_url='login')
def fiscal_envios(request):
    envios_div = EnviosNFs.objects.select_related('usuario').filter(status_envio='Ag Fiscal')

    context = {
        'envios_div':envios_div
    }
    return render(request, "envios_fiscal.html", context)

@login_required(login_url='login')
def envio_com_divergencia(request, id):
    envios_div = EnviosNFs.objects.get(id=id)
    envios_div.status_envio = 'Ag Compras'
    
    envios_div.save()

    messages.success(request, "Status alterado com sucesso!")
    return redirect('fiscal_envios')
 
@login_required(login_url='login')
def envio_liberado(request, id):
    envios_lib = EnviosNFs.objects.get(id=id)

    envios_lib.status_envio = 'Ag Agendamento'
    envios_lib.save()

    messages.success(request, "Status alterado com sucesso!")
    return redirect('fiscal_envios')