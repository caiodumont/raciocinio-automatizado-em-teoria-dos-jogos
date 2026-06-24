import itertools
import random

def gerar_jogos_aleatorios(n: int, s: int) -> list:
    # Gera um jogo com n jogadores e s estratégias por jogador.
    # Retorna a utilidade de cada jogador para todos os perfis de estratégias.
    utilidades = []

    for _ in range(n):
        jogador = []

        # Percorre todos os perfis de estratégias possíveis (s^n combinações)
        for combinacao in itertools.product(range(1, s + 1), repeat=n):
            payoff = random.randint(1, s**n)
            jogador.append((combinacao, payoff))

        # Armazena a tabela de utilidade do jogador
        utilidades.append(jogador)

    return utilidades