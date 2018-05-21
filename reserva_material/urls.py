from django.urls import path
from django.conf.urls.static import static
from . import views
from site_reserva import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('pessoal', views.pessoal, name='pessoal'),
    path('material', views.material, name='material'),
    path('cautelas', views.cautelas, name='cautelas'),
    path('emprestar', views.emprestar, name='emprestar'),
    path('receber', views.receber, name='receber'),
    path('cautelas_vencidas', views.cautelas_vencidas, name='cautelas_vencidas'),
    path('pronto', views.pronto, name='pronto'),
    path('imprimir_pronto', views.imprimir_pronto, name='imprimir_pronto'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #+ static(settings.STATIC_URL, document_root=settings.STATIC_URL)
