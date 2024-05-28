# models.py
from django.db import models
from django.utils import timezone
from django.db.models import Max

class Setor(models.Model):
    id_setor = models.BigAutoField(primary_key=True)
    nome_setor = models.CharField(max_length=40, null=False)

    def __str__(self):
        return f"{self.nome_setor}"

class Funcionario(models.Model):
    id_funcionario = models.BigAutoField(primary_key=True)
    setor = models.ForeignKey(Setor, on_delete=models.DO_NOTHING)
    nome_funcionario = models.CharField(max_length=40, null=False)
    telefone_funcionario = models.CharField(max_length=14, null=False)

    def __str__(self):
        return f"{self.nome_funcionario}"

class OrdemServico(models.Model):
    STATUS_CHOICES = [
        ('Aberta', 'Aberta'),
        ('Em espera', 'Em espera'),
        ('Concluída', 'Concluída'),
        ('Arquivada', 'Arquivada'),
    ]

    id_ordem_servico = models.BigAutoField(primary_key=True)
    numero_ordem_servico = models.CharField(max_length=50, unique=True, blank=True)
    setor = models.ForeignKey(Setor, on_delete=models.DO_NOTHING)
    data_entrada = models.DateField(default=timezone.now)
    data_conclusao = models.DateField(null=True, blank=True)
    descricao = models.CharField(max_length=400, null=False)
    solicitante = models.CharField(max_length=40, null=False)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default='Aberta')
    observacoes = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if not self.numero_ordem_servico:
            # Gerar número de ordem de serviço
            current_month = timezone.now().month
            last_order = OrdemServico.objects.filter(data_entrada__month=current_month).aggregate(Max('id_ordem_servico'))
            new_number = (last_order['id_ordem_servico__max'] or 0) + 1
            self.numero_ordem_servico = f"ORDEM DE SERVIÇO - n° {new_number}/{current_month:02d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero_ordem_servico} - {self.data_entrada}"
