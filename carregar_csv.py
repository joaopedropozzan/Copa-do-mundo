import os
import csv
import django
import re
import unicodedata

# Configura o ambiente do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'albumFigs.settings')
django.setup()

from album.models import Selecao, Figurinha


def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text).strip('-')
    return text


def importar_dados():
    print("Iniciando a carga de dados...")
    mapa_selecoes = {}

    # 1. Processa as Seleções
    with open('teams.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            team_id = int(row['team_id'])
            nome_pais = row['team_name']
            slug_pais = slugify(nome_pais)

            selecao_obj, criado = Selecao.objects.get_or_create(
                id=team_id,
                defaults={'nome': nome_pais, 'slug': slug_pais}
            )
            mapa_selecoes[team_id] = selecao_obj

    print(f"-> {len(mapa_selecoes)} seleções processadas.")

    # 2. Processa as Figurinhas
    contadores_selecao = {}
    total_figurinhas = 0

    with open('squads_and_players.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            player_id = int(row['player_id'])
            team_id = int(row['team_id'])
            nome_jogador = row['player_name']
            posicao = row['position']

            if team_id not in mapa_selecoes:
                continue

            selecao_obj = mapa_selecoes[team_id]

            if team_id not in contadores_selecao:
                contadores_selecao[team_id] = 1
            else:
                contadores_selecao[team_id] += 1

            numero_figurinha = contadores_selecao[team_id]
            eh_rara = (posicao == 'FWD' or numero_figurinha == 10)

            # O defaults garante que se rodar o script de novo, ele não duplica
            Figurinha.objects.get_or_create(
                id=player_id,
                defaults={
                    'selecao': selecao_obj,
                    'numero': numero_figurinha,
                    'nome_jogador': nome_jogador,
                    'posicao': posicao,
                    'eh_rara': eh_rara
                }
            )
            total_figurinhas += 1

    print(f"-> {total_figurinhas} figurinhas processadas com sucesso!")
    print("Mágica concluída! Seu banco de dados está totalmente populado.")


if __name__ == '__main__':
    importar_dados()