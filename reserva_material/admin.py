from django.contrib import admin
from .models import Pessoa, Quartel, Material, Cautela

admin.site.register(Pessoa)
admin.site.register(Quartel)
admin.site.register(Material)
admin.site.register(Cautela)
