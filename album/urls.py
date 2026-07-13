from django.urls import path
from . import views

urlpatterns = [
    # Rota para o dashboard: http://127.0.0.1:8000/album/
    path('', views.dashboard, name='dashboard'),

    # Rota para os detalhes: http://127.0.0.1:8000/album/selecao/1/
    path('selecao/<int:selecao_id>/', views.detalhe_selecao, name='detalhe_selecao'),
]