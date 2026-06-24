import itertools
import networkx
import random

def gerar_jogos_aleatorios(n: int, s: int, d: int) -> list:
    # Gera um jogo gráfico aleatório com n jogadores, s estratégias e d arestas.
    # Retorna as utilidades de cada jogador e suas respectivas vizinhanças.
    utilidades = []
    vizinhancas = []

    # Gera um grafo aleatório com n vértices (jogadores) e d arestas
    grafo = networkx.gnm_random_graph(n, d)

    for i in range(n):
        jogador = []

        vizinhanca = sorted([i, *grafo.neighbors(i)])

        # Percorre todas as combinações de estratégias possíveis para os jogadores da vizinhança
        for combinacao in itertools.product(range(1, s+1), repeat=len(vizinhanca)):
            payoff = random.randint(1, s**len(vizinhanca))
            jogador.append((combinacao, payoff))

        # Armazena a tabela de utilidade do jogador e sua respectiva vizinhança
        utilidades.append(jogador)
        vizinhancas.append(vizinhanca)

    return utilidades, vizinhancas