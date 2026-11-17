from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ObraForm, LancamentoFinanceiroForm
from .models import Obra, LancamentoFinanceiro


@login_required
def painel(request):
    obras = Obra.objects.filter(usuario=request.user)

    obras_com_resumo = []
    total_receitas = Decimal("0.00")
    total_despesas = Decimal("0.00")

    for obra in obras:
        resumo = obra.resumo()

        obras_com_resumo.append({
            "obra": obra,
            "resumo": resumo,
        })

        total_receitas += resumo["receitas"]
        total_despesas += resumo["despesas"]

    contexto = {
        "obras": obras_com_resumo,
        "quantidade_obras": obras.count(),
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo_geral": total_receitas - total_despesas,
    }

    return render(request, "obras/painel.html", contexto)


@login_required
def nova_obra(request):
    form = ObraForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        obra = form.save(commit=False)
        obra.usuario = request.user
        obra.save()

        messages.success(request, "Obra cadastrada com sucesso!")
        return redirect("painel")

    return render(request, "obras/obra_form.html", {
        "form": form,
        "titulo": "Cadastrar nova obra",
    })


@login_required
def detalhe_obra(request, obra_id):
    obra = get_object_or_404(
        Obra,
        id=obra_id,
        usuario=request.user
    )

    lancamentos = obra.lancamentos.all().order_by("-data", "-data_registro")
    resumo = obra.resumo()

    contexto = {
        "obra": obra,
        "lancamentos": lancamentos,
        "resumo": resumo,
    }

    return render(request, "obras/detalhe_obra.html", contexto)


@login_required
def novo_lancamento(request, obra_id):
    obra = get_object_or_404(
        Obra,
        id=obra_id,
        usuario=request.user
    )

    form = LancamentoFinanceiroForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        lancamento = form.save(commit=False)
        lancamento.obra = obra
        lancamento.save()

        messages.success(request, "Lançamento registrado com sucesso!")
        return redirect("detalhe_obra", obra_id=obra.id)

    return render(request, "obras/lancamento_form.html", {
        "form": form,
        "obra": obra,
        "titulo": "Novo lançamento financeiro",
    })


@login_required
def editar_lancamento(request, lancamento_id):
    lancamento = get_object_or_404(
        LancamentoFinanceiro,
        id=lancamento_id,
        obra__usuario=request.user
    )

    form = LancamentoFinanceiroForm(
        request.POST or None,
        instance=lancamento
    )

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(request, "Lançamento atualizado com sucesso!")
        return redirect("detalhe_obra", obra_id=lancamento.obra.id)

    return render(request, "obras/lancamento_form.html", {
        "form": form,
        "obra": lancamento.obra,
        "titulo": "Editar lançamento financeiro",
    })
