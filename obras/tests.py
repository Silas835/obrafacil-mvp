from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import LancamentoFinanceiro, Obra


class ObraELancamentoTests(TestCase):
    def setUp(self):
        self.usuario = get_user_model().objects.create_user(
            username="demo", password="senha-de-teste-123"
        )
        self.obra = Obra.objects.create(
            usuario=self.usuario,
            nome="Reforma Casa 01",
            tipo_servico="reforma",
            data_inicio=date(2026, 11, 5),
        )

    def novo_lancamento(self, tipo, valor):
        return LancamentoFinanceiro(
            obra=self.obra,
            tipo=tipo,
            categoria="material",
            descricao="Lançamento de teste",
            valor=Decimal(valor),
            data=date(2026, 11, 10),
        )

    def test_resumo_calcula_receitas_despesas_e_saldo(self):
        self.novo_lancamento("receita", "1000.00").save()
        self.novo_lancamento("despesa", "300.00").save()
        self.novo_lancamento("despesa", "200.00").save()
        resumo = self.obra.resumo()
        self.assertEqual(resumo["receitas"], Decimal("1000.00"))
        self.assertEqual(resumo["despesas"], Decimal("500.00"))
        self.assertEqual(resumo["saldo"], Decimal("500.00"))

    def test_obra_sem_lancamentos_tem_resumo_zerado(self):
        resumo = self.obra.resumo()
        self.assertEqual(resumo["saldo"], Decimal("0.00"))

    def test_valor_zero_e_recusado(self):
        with self.assertRaises(ValidationError):
            self.novo_lancamento("despesa", "0.00").full_clean()

    def test_valor_negativo_e_recusado(self):
        with self.assertRaises(ValidationError):
            self.novo_lancamento("despesa", "-10.00").full_clean()

    def test_nome_de_obra_duplicado_para_o_mesmo_usuario_e_recusado(self):
        duplicada = Obra(
            usuario=self.usuario,
            nome="Reforma Casa 01",
            tipo_servico="reforma",
            data_inicio=date(2026, 11, 6),
        )
        with self.assertRaises(ValidationError):
            duplicada.full_clean()

    def test_data_de_fim_anterior_ao_inicio_e_recusada(self):
        obra = Obra(
            usuario=self.usuario,
            nome="Aterro Lote 07",
            tipo_servico="aterramento",
            data_inicio=date(2026, 11, 10),
            data_prevista_fim=date(2026, 11, 1),
        )
        with self.assertRaises(ValidationError):
            obra.full_clean()