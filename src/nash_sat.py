import itertools
import networkx as nx
import random

def gerar_jogo_grafico_aleatorio(n_jogadores: int, s_estrategias: int, d_arestas: int) -> tuple:
    # Gera um jogo gráfico aleatório.
    # Retorna a tabela de utilidade de cada jogador considerando os perfis de estratégias da sua vizinhança, 
    # além das respectivas vizinhanças.
    tabelas_utilidade = []
    vizinhancas = []

    # Gera o grafo de interação entre os jogadores
    grafo_interacao = nx.gnm_random_graph(n_jogadores, d_arestas)

    for jogador in range(n_jogadores):
        tabela_utilidade = {}

        # Obtém a vizinhança do jogador, incluindo o próprio jogador
        vizinhanca = sorted([jogador, *grafo_interacao.neighbors(jogador)])

        # Percorre todos os perfis de estratégias possíveis da vizinhança
        for perfil in itertools.product(range(1, s_estrategias+1), repeat=len(vizinhanca)):
            payoff = random.randint(1, s_estrategias**len(vizinhanca))
            tabela_utilidade[perfil] = payoff

        # Armazena a tabela de utilidade e a vizinhança do jogador atual
        tabelas_utilidade.append(tabela_utilidade)
        vizinhancas.append(vizinhanca)

    return tabelas_utilidade, vizinhancas