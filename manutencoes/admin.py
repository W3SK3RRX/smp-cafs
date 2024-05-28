from django.contrib import admin
from .models import Setor, Funcionario, OrdemServico

# Register your models here.
admin.site.register(Setor)
admin.site.register(Funcionario)
admin.site.register(OrdemServico)