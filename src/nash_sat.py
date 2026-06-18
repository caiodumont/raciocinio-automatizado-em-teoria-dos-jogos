import itertools
import random

def gerar_jogos_aleatorios(n: int, s: int) -> list:
    # Gera um jogo aleatório com n jogadores e s estratégias por jogador.
    # Retorna uma lista contendo as utilidades de cada jogador para todos os perfis de estratégias possíveis.
    utilidades = []
    combinacoes = list(itertools.product(range(1, s+1), repeat=n))

    for _ in range(n):
        jogador = []

        for combinacao in combinacoes:
            payoff = random.randint(1, s**n)
            jogador.append([combinacao, payoff])
        
        utilidades.append(jogador)

    return utilidades