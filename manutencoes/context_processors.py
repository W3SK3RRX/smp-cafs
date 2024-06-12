from django.conf import settings

def user_permissions(request):
    if request.user.is_authenticated:
        return {
            'can_view_area_administrativa': request.user.has_perm('manutencoes.view_area_administrativa'),
            'can_view_cadastrar_ordem_servico': request.user.has_perm('manutencoes.view_cadastrar_ordem_servico'),
            'can_view_editar_ordem_servico': request.user.has_perm('manutencoes.view_editar_ordem_servico'),
            'can_view_deletar_os': request.user.has_perm('manutencoes.view_deletar_os'),
        }
    return {
        'can_view_area_administrativa': False,
        'can_view_cadastrar_ordem_servico': False,
        'can_view_editar_ordem_servico': False,
        'can_deletar_os': False,
    }

