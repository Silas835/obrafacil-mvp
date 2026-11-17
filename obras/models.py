from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum


class Obra(models.Model):
    TIPOS_SERVICO = [
        ("aterramento", "Aterramento"),
        ("demolicao", "Demolição"),
        ("construcao", "Construção"),
        ("reforma", "Reforma"),
        ("compra_venda", "Compra e venda"),
    ]
    STATUS = [
        ("em_andamento", "Em andamento"),
        ("concluida", "Concluída"),
        ("pausada", "Pausada"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="obras"
    )
    nome = models.CharField(max_length=120)
    cliente = models.CharField(max_length=120, blank=True)
    local = models.CharField(max_length=200, blank=True)
    tipo_servico = models.CharField(max_length=20, choices=TIPOS_SERVICO)
    status = models.CharField(max_length=20, choices=STATUS, default="em_andamento")
    data_inicio = models.DateField()
    data_prevista_fim = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-data_inicio"]
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "nome"], name="obra_nome_unico_por_usuario"
            )
        ]

    def __str__(self):
        return self.nome

    def clean(self):
        if (
            self.data_prevista_fim
            and self.data_inicio
            and self.data_prevista_fim < self.data_inicio
        ):
            raise ValidationError(
                {"data_prevista_fim": "A data prevista de fim não pode ser anterior à data de início."}
            )

    def _total(self, tipo):
        total = self.lancamentos.filter(tipo=tipo).aggregate(total=Sum("valor"))["total"]
        return total or Decimal("0.00")

    def resumo(self):
        receitas = self._total("receita")
        despesas = self._total("despesa")
        return {"receitas": receitas, "despesas": despesas, "saldo": receitas - despesas}


class LancamentoFinanceiro(models.Model):
    TIPOS = [("receita", "Receita"), ("despesa", "Despesa")]
    CATEGORIAS = [
        ("material", "Material"),
        ("mao_de_obra", "Mão de obra"),
        ("equipamento", "Equipamento"),
        ("combustivel", "Combustível"),
        ("outros", "Outros"),
    ]

    obra = models.ForeignKey(
        Obra, on_delete=models.PROTECT, related_name="lancamentos"
    )
    tipo = models.CharField(max_length=10, choices=TIPOS)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    data = models.DateField()
    data_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_tipo_display()} de {self.valor} em {self.obra}"
