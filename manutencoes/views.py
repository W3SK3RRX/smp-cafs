from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Setor, Funcionario, OrdemServico
from django.db.models import Count
from django.contrib.messages import constants
from django.contrib import messages
from django.db.models.functions import ExtractMonth, ExtractYear
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from .forms import FuncionarioForm, OsForm
from django.template.loader import render_to_string
from weasyprint import HTML
from usuarios import views
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.

@login_required(login_url="/login/")
def home(request):
    if request.method=="GET":
        setor_list = Setor.objects.all()
        return render(request, 'home.html', {'setor_list':setor_list})


@login_required(login_url="/login/")
@permission_required('manutencoes.view_area_administrativa', raise_exception=True)
def area_administrativa(request):
    if request.method == "GET":
        setor_list = Setor.objects.all()
        funcionarios_list = Funcionario.objects.all()
        anos = OrdemServico.objects.annotate(ano=ExtractYear('data_entrada')).values_list('ano', flat=True).distinct()# Obter todos os anos presentes nos dados
        
        # Processar a seleção do ano e do mês
        selected_year = request.GET.get('ano')
        selected_month = request.GET.get('mes')
        if selected_year:
            ordens_servico = OrdemServico.objects.filter(data_entrada__year=selected_year)# Iniciar com todos os dados para este ano

            if selected_month:
                ordens_servico = ordens_servico.filter(data_entrada__month=selected_month)# Filtrar por mês, se selecionado

        else:
            current_year = timezone.now().year# Obter o ano atual
            ordens_servico = OrdemServico.objects.filter(data_entrada__year=current_year)

        # Realizar contagens e agrupamentos
        status_counts = ordens_servico.values('status').annotate(count=Count('id_ordem_servico'))
        setor_counts = ordens_servico.values('setor__nome_setor').annotate(count=Count('id_ordem_servico'))
        ordens_por_mes = ordens_servico.annotate(mes=ExtractMonth('data_entrada')).values('mes').annotate(total=Count('id_ordem_servico')).order_by('mes')
        
        # Processamento dos dados para o gráfico de ordens de serviço ao longo dos meses
        ordens_meses = [0] * 12  # Inicializa uma lista com contagem zero para cada mês
        for ordem in ordens_por_mes:
            ordens_meses[ordem['mes'] - 1] = ordem['total']  # Subtrai 1 pois o mês é indexado de 1 a 12

        # Organizar dados por setor para o gráfico
        setor_data = {}
        for setor in setor_counts:
            setor_nome = setor['setor__nome_setor']
            setor_data[setor_nome] = [0] * 12  # Inicializa com 12 meses

        for ordem in ordens_servico:
            setor_nome = ordem.setor.nome_setor
            mes = ordem.data_entrada.month
            setor_data[setor_nome][mes - 1] += 1  # Incrementa a contagem para o mês correspondente

        return render(request, "area_administrativa.html", {
            'setor_list': setor_list,
            'funcionarios_list': funcionarios_list,
            'status_counts': status_counts,
            'setor_counts': setor_counts,
            'ordens_por_mes': ordens_por_mes,
            'ordens_meses': ordens_meses,
            'anos': anos,
            'selected_year': selected_year,
            'selected_month': selected_month,
            'setor_data': setor_data  
        })


@login_required(login_url="/login/")
def cadastrar_setor(request):
    if request.method == "GET":
        return render(request, "cadastrar_setor.html")
    else:
        nome_setor = request.POST.get('nome_setor')
        if nome_setor:
            Setor.objects.create(nome_setor=nome_setor)
            return redirect('area_administrativa')
        else:
            messages.add_message(request, constants.ERROR, "Erro ao cadastrar setor!")
            return redirect('/manutencoes/cadastrar_setor')


@login_required(login_url="/login/")
def editar_setor(request, id_setor):
    setor = get_object_or_404(Setor, pk=id_setor)
    
    if request.method == "POST":
        novo_nome = request.POST.get('nome_setor')
        
        if novo_nome:
            setor.nome_setor = novo_nome
            setor.save()
        else:
            messages.add_message(request, constants.ERROR, "Erro ao editar nome do setor! Nome não pode ser vazio.")
            return redirect(f'/manutencoes/editar_setor/{id_setor}')
    
    return render(request, 'editar_setor.html', {'setor': setor})


@login_required(login_url="/login/")
def deletar_setor(request, id_setor):
    setor = get_object_or_404(Setor, id_setor=id_setor)
    setor.delete()
    return redirect('area_administrativa')


@login_required(login_url="/login/")
def cadastrar_funcionario(request):
    if request.method == "GET":
        setor_list = Setor.objects.all()
        return render(request, 'cadastrar_funcionario.html', {'setor_list': setor_list})
    elif request.method == "POST":
        setor_id = request.POST.get('setor')
        nome_funcionario = request.POST.get('nome')
        telefone_funcionario = request.POST.get('tel')
        if setor_id and nome_funcionario and telefone_funcionario:
            setor = Setor.objects.get(pk=setor_id)
            Funcionario.objects.create(setor=setor, nome_funcionario=nome_funcionario, telefone_funcionario=telefone_funcionario)
            return redirect('area_administrativa')
        else:
            messages.add_message(request, constants.ERROR, "Por favor, preencha todos os campos!")
            return HttpResponseRedirect(reverse('cadastrar_funcionario'))


@login_required(login_url="/login/")
def editar_funcionario(request, id_funcionario):
    funcionario = get_object_or_404(Funcionario, pk=id_funcionario)
    if request.method == "POST":
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            return redirect('area_administrativa')
        else:
            messages.add_message(request, constants.ERROR, "Todos os campos são obrigatórios.")
    else:
        form = FuncionarioForm(instance=funcionario)

    context = {
        'form': form,
        'funcionario': funcionario,
    }
    return render(request, 'editar_funcionario.html', context)


@login_required(login_url="/login/")
def deletar_funcionario(request, id_funcionario):
    funcionario = get_object_or_404(Funcionario, id_funcionario=id_funcionario)
    funcionario.delete()
    return redirect('area_administrativa')


@login_required(login_url="/login/")
def demandas(request, id_setor):
    setor = get_object_or_404(Setor, pk=id_setor)
    os_list = OrdemServico.objects.filter(setor=setor)

    # Obter todos os anos presentes nos dados para o setor específico
    anos = os_list.annotate(ano=ExtractYear('data_entrada')).values_list('ano', flat=True).distinct()

    # Processar a seleção do ano e do mês
    selected_year = request.GET.get('ano')
    selected_month = request.GET.get('mes')

    if selected_year:
        os_list = os_list.filter(data_entrada__year=selected_year)
        if selected_month:
            os_list = os_list.filter(data_entrada__month=selected_month)

    # Realizar contagens e agrupamentos
    status_counts = os_list.values('status').annotate(count=Count('id_ordem_servico'))

    return render(request, "demandas.html", {
        'setor': setor,
        'os_list': os_list,
        'anos': anos,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'status_counts': status_counts,
    })


@login_required(login_url="/login/")
def cadastrar_ordem_servico(request):
    setor_list = Setor.objects.all()
    if request.method == "POST":
        setor_id = request.POST.get('setor')
        descricao = request.POST.get('descricao')
        solicitante = request.POST.get('solicitante')
        observacoes = request.POST.get('observacoes')
        
        setor = Setor.objects.get(id_setor=setor_id)
        
        nova_ordem_servico = OrdemServico(
            setor=setor,
            descricao=descricao,
            solicitante=solicitante,
            observacoes=observacoes
        )
        nova_ordem_servico.save()

        return redirect('demandas', id_setor=setor_id)  # Passar o id_setor no redirecionamento
    return render(request, "cadastrar_ordem_servico.html", {'setor_list': setor_list})


@login_required(login_url="/login/")
def ordem_servico(request, id_ordem_servico):
    os = get_object_or_404(OrdemServico, pk=id_ordem_servico)
    if request.method == "GET":
        return render(request, "ordem_servico.html", {'os':os})


@login_required(login_url="/login/")
def editar_ordem_servico(request, id_ordem_servico):
    os = get_object_or_404(OrdemServico, pk=id_ordem_servico)
    id_setor = os.setor.id_setor
    if request.method == "POST":
        form = OsForm(request.POST, instance=os)
        if form.is_valid():
            form.save()
            return redirect(f'/manutencoes/demandas/{id_setor}', id_ordem_servico)
        else:
            messages.add_message(request, constants.ERROR, "Todos os campos são obrigatórios.")
    else:
        form = OsForm(instance=os)

    context = {
        'form': form,
        'os': os,
    }
    return render(request, 'editar_ordem_servico.html', context)


@login_required(login_url="/login/")
def download_os_pdf(request, id_ordem_servico):
    os = OrdemServico.objects.get(id_ordem_servico=id_ordem_servico)

    html_string = render_to_string('ordem_servico_pdf.html', {'os': os})
    html = HTML(string=html_string)

    # Cria um response como um PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ordem_servico_{id_ordem_servico}_{os.data_entrada}.pdf"'

    # Gera o PDF e escreve no response
    html.write_pdf(response)

    return response


@login_required(login_url="/login/")
def deletar_os(request, id_ordem_servico):
    os = get_object_or_404(OrdemServico, id_ordem_servico=id_ordem_servico)
    id_setor = os.setor.id_setor
    os.delete()
    return redirect(f'/manutencoes/demandas/{id_setor}')
