from django import forms
from .models import Funcionario, OrdemServico, Setor

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome_funcionario', 'setor', 'telefone_funcionario']
        widgets = {
            'nome_funcionario': forms.TextInput(attrs={'class': 'form-control'}),
            'setor': forms.Select(attrs={'class': 'form-control'}),
            'telefone_funcionario': forms.TextInput(attrs={'class': 'form-control'}),
        }

class OsForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = [
            'setor', 
            'funcionario', 
            'data_entrada', 
            'data_conclusao', 
            'descricao', 
            'solicitante', 
            'status', 
            'observacoes'
        ]
        widgets = {
            'setor': forms.Select(attrs={'class': 'form-control'}),
            'funcionario': forms.Select(attrs={'class': 'form-control'}),
            'data_entrada': forms.DateInput(attrs={'class': 'form-control'}),
            'data_conclusao': forms.DateInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'solicitante': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control'}),
        }