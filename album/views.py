from django.shortcuts import render, get_object_or_404
from .models import Selecao, Figurinha


def dashboard(request):
    # Equivale ao Selecao::all() do Laravel
    selecoes = Selecao.objects.all()

    context = {
        'selecoes': selecoes,
    }
    # Renderiza o template passando os dados
    return render(request, 'album/dashboard.html', context)


def detalhe_selecao(request, selecao_id):
    # Busca a seleção pelo ID ou retorna erro 404 se não existir
    selecao = get_object_or_404(Selecao, id=selecao_id)

    # Busca todas as figurinhas que pertencem a essa seleção
    figurinhas = selecao.figurinhas.all()

    context = {
        'selecao': selecao,
        'figurinhas': figurinhas,
    }
    return render(request, 'album/detalhe_selecao.html', context)
