from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from app_solen.models import MyUser, EnviosNFs

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=MyUser
        fields=('email','tipo_usuario','telefone','nome_fornecedor','password1','password2')

class EnviosNFsForm(forms.ModelForm):
    class Meta:
        model=EnviosNFs
        fields=('pedido_compras','nota_num','pdf_nota','empresa_destinataria','solicitante', 'observacao_fornecedor')        
        