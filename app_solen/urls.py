from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/',login_view, name='login'),
    path('login/submit',submit_login, name='submit_login'),
    path('logout',logout_user,name='logout'),
    path('usuarios',register,name='register'),
    path('envios/novo',envios_nfs, name='envios_nfs'),
    path('envios/meus_envios',meus_envios,name='meus_envios'),
    path('envios/meus_envios/editar/<int:id>',editar_envios,name='editar_envios'),
    path('envios/meus_envios/cancelar_nf/<int:id>',cancelar_nf,name='cancelar_nf'),
    path('usuarios/delete/<int:id>', delete_user, name='delete_user'),
    path('usuarios/editar/<int:id>', editar_user, name='editar_user'),
    path('envios/todos_envios/tabela',todos_envios,name='todos_envios'),
    path('envios/compras',compras_envios,name='compras_envios'),
    path('envios/compras/envio_ajustado/<int:id>',envio_ajustado_compras,name='envio_ajustado_compras'),
    path('envios/fiscal',fiscal_envios,name='fiscal_envios'),
    path('envios/fiscal/envio_com_divergencia/<int:id>',envio_com_divergencia,name='envio_com_divergencia'),
    path('envios/fiscal/envio_liberado/<int:id>',envio_liberado,name='envio_liberado'),
    path('envios/todos_envios/exportar_csv/',exportar_csv,name="exportar_csv"),
]