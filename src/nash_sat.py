import itertools
import networkx as nx
import random
from pysat.formula import CNF

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
        for perfil in itertools.product(range(1, s_estrategias + 1), repeat=len(vizinhanca)):
            payoff = random.randint(1, s_estrategias ** len(vizinhanca))
            tabela_utilidade[perfil] = payoff

        # Armazena a tabela de utilidade e a vizinhança do jogador atual
        tabelas_utilidade.append(tabela_utilidade)
        vizinhancas.append(vizinhanca)

    return tabelas_utilidade, vizinhancas

def transformar_jogo_para_cnf(tabelas_utilidade: list, vizinhancas: list, s_estrategias: int) -> CNF:
    # Transforma um jogo gráfico aleatório em uma fórmula CNF.
    # A fórmula é satisfatível se, e somente se, o jogo possui um equilíbrio de Nash puro.
    n_jogadores = len(tabelas_utilidade)

    cnf = CNF()

    # Associa um identificador único a cada par (jogador, estratégia)
    # Jogadores são indexados de 0 a n_jogadores-1
    # Estratégias são indexadas de 1 a s_estrategias
    def var(jogador: int, estrategia: int) -> int:
        return jogador * s_estrategias + estrategia

    # Cada jogador deve escolher pelo menos uma estratégia
    for jogador in range(n_jogadores):
        clausula = []

        for estrategia in range(1, s_estrategias + 1):
            clausula.append(var(jogador, estrategia))

        cnf.append(clausula)

    # Cada jogador pode escolher no máximo uma estratégia
    for jogador in range(n_jogadores):
        for estrategia_1, estrategia_2 in itertools.combinations(range(1, s_estrategias + 1), 2):
            clausula = [-var(jogador, estrategia_1), -var(jogador, estrategia_2)]

            cnf.append(clausula)

    # Gera as cláusulas que impõem a condição de melhor resposta
    for jogador in range(n_jogadores):
        tabela_utilidade = tabelas_utilidade[jogador]
        vizinhanca = vizinhancas[jogador]

        # Obtém a lista dos vizinhos, sem incluir o próprio jogador
        vizinhos = [v for v in vizinhanca if v != jogador]

        # Percorre todos os perfis possíveis dos vizinhos
        for perfil_vizinhos in itertools.product(range(1, s_estrategias + 1), repeat=len(vizinhos)):

            # Calcula o payoff de cada estratégia do jogador
            payoffs = []

            for estrategia in range(1, s_estrategias + 1):
                perfil = []

                indice_vizinho = 0

                for elemento in vizinhanca:
                    if elemento == jogador:
                        perfil.append(estrategia)
                    else:
                        perfil.append(perfil_vizinhos[indice_vizinho])
                        indice_vizinho += 1

                perfil = tuple(perfil)
                payoffs.append(tabela_utilidade[perfil])

            payoff_maximo = max(payoffs)

            # Descobre quais estratégias são melhores respostas
            melhores_respostas = []

            for indice_estrategia, payoff in enumerate(payoffs, start=1):
                if payoff == payoff_maximo:
                    melhores_respostas.append(indice_estrategia)

            # Monta a cláusula
            clausula = []

            for vizinho, estrategia in zip(vizinhos, perfil_vizinhos):
                clausula.append(-var(vizinho, estrategia))

            for estrategia in melhores_respostas:
                clausula.append(var(jogador, estrategia))

            cnf.append(clausula)

    return cnf