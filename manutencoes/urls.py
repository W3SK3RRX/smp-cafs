from django.urls import path
from . import views
from .views import deletar_setor,deletar_funcionario, editar_setor, editar_funcionario

urlpatterns = [
    path('home/', views.home, name="home"),

    path('area_administrativa/', views.area_administrativa, name="area_administrativa"),

    #Setor
    path('cadastrar_setor', views.cadastrar_setor, name="cadastrar_setor"),
    path('deletar_setor/<int:id_setor>', deletar_setor, name="deletar_setor"),
    path('editar_setor/<int:id_setor>', editar_setor, name="editar_setor"),

    #Funcionario
    path('cadastrar_funcionario', views.cadastrar_funcionario, name="cadastrar_funcionario"),
    path('deletar_funcionario/<int:id_funcionario>', deletar_funcionario, name="deletar_funcionario"),
    path('editar_funcionario/<int:id_funcionario>', editar_funcionario, name="editar_funcionario"),

    path('demandas/<int:id_setor>', views.demandas, name="demandas"),

    path('cadastrar_ordem_servico', views.cadastrar_ordem_servico, name="cadastrar_ordem_servico"),
]
