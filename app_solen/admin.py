from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import MyUser, EnviosNFs, TabelaAgendados

class MyUserAdmin(BaseUserAdmin):
    list_display=('id','email','tipo_usuario','telefone','nome_fornecedor','data_entrada','ultimo_login','is_admin','is_active','is_staff','is_superuser')
    search_fields=('email','tipo_usuario')
    readonly_fields=('data_entrada','ultimo_login')
    filter_horizontal=()
    list_filter=('last_login',)
    fieldsets=()

    add_fieldsets=(
        (None,{
            'classes':('wide'),
            'fields':('email','tipo_usuario','telefone','nome_fornecedor','password1','password2'),
        }),
    )

    ordering=('email',)

admin.site.register(MyUser, MyUserAdmin)

class EnviosNFsAdmins(admin.ModelAdmin):
    list_display = ('id','pedido_compras','nota_num','pdf_nota','usuario','empresa_destinataria','solicitante', 'data_criacao','data_validacao_fiscal','data_divergencia_fiscal','observacao_fiscal','data_ajuste_compras','observacao_compras','observacao_fornecedor', 'status_envio')

admin.site.register(EnviosNFs, EnviosNFsAdmins)

class DataAgendasAdmin(admin.ModelAdmin):
    list_display = ('id','id_nota','data_agenda','hora_agenda')

admin.site.register(TabelaAgendados, DataAgendasAdmin)