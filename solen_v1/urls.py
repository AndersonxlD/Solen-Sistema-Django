from django.contrib import admin
from django.urls import path, include
from app_solen import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_solen.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Solen"
admin.site.site_title = "Solução em Sistemas Web"
admin.site.index_title = "Sistema de Gerenciamento de Agendamentos"