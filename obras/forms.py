from django import forms

from .models import Obra, LancamentoFinanceiro


class ObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = [
            "nome",
            "cliente",
            "local",
            "tipo_servico",
            "status",
            "data_inicio",
            "data_prevista_fim",
        ]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "cliente": forms.TextInput(attrs={"class": "form-control"}),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "tipo_servico": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "data_inicio": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "data_prevista_fim": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }


class LancamentoFinanceiroForm(forms.ModelForm):
    class Meta:
        model = LancamentoFinanceiro
        fields = [
            "tipo",
            "categoria",
            "descricao",
            "valor",
            "data",
        ]

        widgets = {
            "tipo": forms.Select(attrs={"class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-control"}),
            "descricao": forms.TextInput(attrs={"class": "form-control"}),
            "valor": forms.NumberInput(
                attrs={"class": "form-control", "min": "0.01", "step": "0.01"}
            ),
            "data": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }
