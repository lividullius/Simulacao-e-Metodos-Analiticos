# Gerador Pseudoaleatório (LCG) --> M2

a = 1103515245        # multiplicador
c = 12345             # incremento
M = 2147483648        # módulo (2^31)
seed = 12345          # semente inicial

_last_random = seed

def next_random():
    """
    Gera um número pseudoaleatório uniforme entre 0 e 1
    utilizando o método da congruência linear (LCG).
    """
    global _last_random

    _last_random = (a * _last_random + c) % M
    valor_normalizado = _last_random / M

    return valor_normalizado
