from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime

import os


class MyUserManager(BaseUserManager):
    def create_user(self, email, tipo_usuario, telefone,nome_fornecedor, password=None):
        if not email:
            raise ValueError("Email é necessário!")
        if not tipo_usuario:
            raise ValueError("Tipo de usuário é necessário!")
        if not telefone:
            raise ValueError("Por favor, insira um telefone!")
        if not nome_fornecedor:
            raise ValueError("Por favor, insira um fornecedor!")

        user = self.model(
            email=self.normalize_email(email),
            tipo_usuario=tipo_usuario,
            telefone=telefone,
            nome_fornecedor=nome_fornecedor
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, tipo_usuario, telefone, nome_fornecedor, password=None):
        user = self.create_user(
            email=email,
            tipo_usuario=tipo_usuario,
            telefone=telefone,
            nome_fornecedor=nome_fornecedor,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

TIPO_USUARIO_CHOICES = (
    ('admin', 'Admin'),
    ('recebimento', 'Recebimento'),
    ('fiscal', 'Fiscal'),
    ('comprador', 'Comprador'),
    ('fornecedor', 'Fornecedor'),
    ('transportadora', 'Transportadora'),
)

class MyUser(AbstractBaseUser):
    email = models.EmailField(verbose_name="Endereço de Email", max_length=60, unique=True)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, verbose_name="Tipo de Usuário")
    telefone = models.CharField(verbose_name="Telefone", max_length=20)
    nome_fornecedor = models.CharField(verbose_name='Nome Fornecedor',max_length=50)
    data_entrada = models.DateTimeField(verbose_name="Data de Entrada", auto_now_add=True)
    ultimo_login = models.DateTimeField(verbose_name="Último Login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['tipo_usuario', 'telefone','nome_fornecedor']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    
EMPRESAS_MULTI = (
     ('MULTI FABRICA - 59.717.553/0006-17','MULTI FABRICA - 59.717.553/0006-17'),
     ('MULTI MATRIZ - 59.717.553/0001-02','MULTI MATRIZ - 59.717.553/0001-02'),
     ('MULTI COMPONENTES - 18.272.566/0001-38','MULTI COMPONENTES - 18.272.566/0001-38'),
     ('BLUE - 59.717.553/0012-65','BLUE - 59.717.553/0012-65'),
)

STATUS_ENVIOS = (
     ('Ag Fiscal','Ag Fiscal'),
     ('Ag Compras','Ag Compras'),
     ('Ag Agendamento','Ag Agendamento'),
     ('Agendado','Agendado'),
     ('Recebido','Recebido'),
     ('Recusado','Recusada'),
     ('Cancelada','Cancelada'),
)

class EnviosNFs(models.Model):
    pedido_compras = models.CharField(max_length=10, verbose_name="Pedido de Compras")
    nota_num = models.CharField(max_length=9, verbose_name="Nota Fiscal")
    pdf_nota = models.FileField(verbose_name="PDF Nota Fiscal")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuário")
    empresa_destinataria = models.CharField(choices=EMPRESAS_MULTI, max_length=50, verbose_name="Empresa Destino")
    solicitante = models.CharField(max_length=50,verbose_name='Solicitante')
    observacao_fiscal = models.TextField(verbose_name="Observação Fiscal", max_length=200, blank=True, null=True)
    data_divergencia_fiscal = models.DateTimeField(verbose_name="Data da Divergencia", blank=True, null=True)
    data_validacao_fiscal = models.DateTimeField(verbose_name="Data de Validação", blank=True, null=True)
    observacao_compras = models.TextField(verbose_name="Observação Compras",max_length=200, blank=True, null=True)
    data_ajuste_compras = models.DateTimeField(verbose_name="Data de Ajuste", blank=True, null=True)
    observacao_fornecedor = models.TextField(verbose_name="Observação", max_length=200, blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de envio")
    status_envio = models.CharField(choices=STATUS_ENVIOS,max_length=50,verbose_name='Status Envio',default='Ag Fiscal')

    def __str__(self):
        return str(self.id)
    
    def get_data_criacao(self):
        return self.data_criacao.strftime("%d/%m/%Y %H:%M")
    
class TabelaAgendados(models.Model):
    id_nota = models.ForeignKey(EnviosNFs, on_delete=models.CASCADE)
    data_agenda = models.DateField(verbose_name="Data de Agenda")
    hora_agenda = models.TimeField(verbose_name="Hora de Agenda")

    def __str__(self):
        return str(self.id)
    
    def get_hora_agenda(self):
        return self.hora_agenda.strftime("%H")