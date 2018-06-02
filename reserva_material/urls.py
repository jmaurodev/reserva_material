from django.urls import path
from django.conf.urls.static import static
from site_reserva import settings
from .views import pdfgen, commons, formularios

urlpatterns = [
    path('', commons.index, name='index'),
    path('pessoal', commons.pessoal, name='pessoal'),
    path('material', commons.material, name='material'),
    path('cautelas', commons.cautelas, name='cautelas'),
    path('cautelas_vencidas', commons.cautelas_vencidas, name='cautelas_vencidas'),
    path('pronto', pdfgen.imprimir_pronto, name='pronto'),
    path('emprestar', formularios.emprestar, name='emprestar'),
    path('receber', formularios.receber, name='receber'),
    path('imprimir_pronto', pdfgen.imprimir_pronto, name='imprimir_pronto'),
    path('imprimir_cautela', pdfgen.imprimir_cautela, name='imprimir_cautela'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #+ static(settings.STATIC_URL, document_root=settings.STATIC_URL)
