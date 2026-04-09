import heapq


# M2 - Gerador LCG

# parametros do gerador
a = 1103515245
c = 12345
M = 2**31
seed = 12345

# guarda o último número gerado
_last_random = seed


def next_random():
    #Gera um número pseudoaleatório uniforme entre 0 e 1.
    global _last_random
    _last_random = (a * _last_random + c) % M
    return _last_random / M


def uniforme(minimo, maximo):
    #Converte o valor do LCG para uma uniforme no intervalo [minimo, maximo].
    u = next_random()
    return minimo + (maximo - minimo) * u


# M6 - Simulador de Rede de Filas

class FilaRede:
    def __init__(self, num_servidores, capacidade_sistema, intervalo_chegada=None, intervalo_atendimento=(2.0, 3.0)):
        # parametros da fila
        self.num_servidores = num_servidores
        self.capacidade_sistema = capacidade_sistema
        self.intervalo_chegada = intervalo_chegada
        self.intervalo_atendimento = intervalo_atendimento

        # atributos
        self.fila_espera = []
        self.ocupados = 0

        self.tempo_estados = [0.0 for _ in range(capacidade_sistema + 1)]
        self.ultimo_tempo = 0.0

        self.total_atendidos = 0
        self.total_perdidos = 0

    def clientes_no_sistema(self):
        return self.ocupados + len(self.fila_espera)

    def registrar_tempo_estado(self, novo_tempo):
        estado = self.clientes_no_sistema()
        intervalo = novo_tempo - self.ultimo_tempo
        self.tempo_estados[estado] += intervalo
        self.ultimo_tempo = novo_tempo


class SimuladorRede:
    def __init__(self, limite_randomicos=100000):
        # parametros do sistema
        self.limite_randomicos = limite_randomicos

        # atributos
        self.relogio = 0.0
        self.eventos = []
        self.randomicos_utilizados = 0

        # fila 1: G/G/2/3 com chegada entre 1 e 4 e atendimento entre 3 e 4
        self.fila1 = FilaRede(
            num_servidores=2,
            capacidade_sistema=3,
            intervalo_chegada=(1.0, 4.0),
            intervalo_atendimento=(3.0, 4.0)
        )

        # fila 2: G/G/1/5 sem chegada externa e atendimento entre 2 e 3
        self.fila2 = FilaRede(
            num_servidores=1,
            capacidade_sistema=5,
            intervalo_chegada=None,
            intervalo_atendimento=(2.0, 3.0)
        )

    def adicionar_evento(self, instante, tipo):
        heapq.heappush(self.eventos, (instante, tipo))

    def consumir_randomico(self):
        if self.randomicos_utilizados >= self.limite_randomicos:
            return False
        self.randomicos_utilizados += 1
        return True

    def gerar_interchegada_fila1(self):
        if not self.consumir_randomico():
            return None
        return uniforme(
            self.fila1.intervalo_chegada[0],
            self.fila1.intervalo_chegada[1]
        )

    def gerar_atendimento_fila1(self):
        if not self.consumir_randomico():
            return None
        return uniforme(
            self.fila1.intervalo_atendimento[0],
            self.fila1.intervalo_atendimento[1]
        )

    def gerar_atendimento_fila2(self):
        if not self.consumir_randomico():
            return None
        return uniforme(
            self.fila2.intervalo_atendimento[0],
            self.fila2.intervalo_atendimento[1]
        )

    def registrar_tempo_estados(self, instante):
        self.fila1.registrar_tempo_estado(instante)
        self.fila2.registrar_tempo_estado(instante)

    def processar_chegada_fila1(self):
        proxima_chegada = self.gerar_interchegada_fila1()
        if proxima_chegada is not None:
            self.adicionar_evento(self.relogio + proxima_chegada, "CHEGADA_FILA1")

        if self.fila1.ocupados < self.fila1.num_servidores:
            self.fila1.ocupados += 1
            tempo_servico = self.gerar_atendimento_fila1()
            if tempo_servico is not None:
                self.adicionar_evento(self.relogio + tempo_servico, "SAIDA_FILA1")
        else:
            if self.fila1.clientes_no_sistema() < self.fila1.capacidade_sistema:
                self.fila1.fila_espera.append(self.relogio)
            else:
                self.fila1.total_perdidos += 1

    def processar_saida_fila1(self):
        self.fila1.total_atendidos += 1

        if len(self.fila1.fila_espera) > 0:
            self.fila1.fila_espera.pop(0)
            tempo_servico = self.gerar_atendimento_fila1()
            if tempo_servico is not None:
                self.adicionar_evento(self.relogio + tempo_servico, "SAIDA_FILA1")
        else:
            self.fila1.ocupados -= 1

        self.processar_chegada_fila2()

    def processar_chegada_fila2(self):
        if self.fila2.ocupados < self.fila2.num_servidores:
            self.fila2.ocupados += 1
            tempo_servico = self.gerar_atendimento_fila2()
            if tempo_servico is not None:
                self.adicionar_evento(self.relogio + tempo_servico, "SAIDA_FILA2")
        else:
            if self.fila2.clientes_no_sistema() < self.fila2.capacidade_sistema:
                self.fila2.fila_espera.append(self.relogio)
            else:
                self.fila2.total_perdidos += 1

    def processar_saida_fila2(self):
        self.fila2.total_atendidos += 1

        if len(self.fila2.fila_espera) > 0:
            self.fila2.fila_espera.pop(0)
            tempo_servico = self.gerar_atendimento_fila2()
            if tempo_servico is not None:
                self.adicionar_evento(self.relogio + tempo_servico, "SAIDA_FILA2")
        else:
            self.fila2.ocupados -= 1

    def executar(self, primeira_chegada=1.5):
        self.relogio = primeira_chegada
        self.fila1.ultimo_tempo = 0.0
        self.fila2.ultimo_tempo = 0.0
        self.adicionar_evento(primeira_chegada, "CHEGADA_FILA1")

        while self.eventos and self.randomicos_utilizados < self.limite_randomicos:
            instante, tipo = heapq.heappop(self.eventos)

            self.registrar_tempo_estados(instante)
            self.relogio = instante

            if tipo == "CHEGADA_FILA1":
                self.processar_chegada_fila1()
            elif tipo == "SAIDA_FILA1":
                self.processar_saida_fila1()
            elif tipo == "SAIDA_FILA2":
                self.processar_saida_fila2()

        self.mostrar_resultados()

    def mostrar_resultados_fila(self, fila, nome):
        tempo_total = sum(fila.tempo_estados)

        print(f"\n{nome} - G/G/{fila.num_servidores}/{fila.capacidade_sistema}")
        print("-" * 40)

        for estado, tempo in enumerate(fila.tempo_estados):
            prob = tempo / tempo_total if tempo_total > 0 else 0.0
            print(
                f"Estado {estado}: "
                f"tempo = {tempo:.2f} | probabilidade = {prob:.4f}"
            )

        print("-" * 40)
        print(f"Tempo total simulado na {nome}: {tempo_total:.2f}")
        print(f"Clientes atendidos: {fila.total_atendidos}")
        print(f"Clientes perdidos: {fila.total_perdidos}")

    def mostrar_resultados(self):
        self.mostrar_resultados_fila(self.fila1, "Fila 1")
        self.mostrar_resultados_fila(self.fila2, "Fila 2")
        print(f"\nTempo global da simulacao: {self.relogio:.2f}")
        print(f"Randomicos utilizados: {self.randomicos_utilizados}")


if __name__ == "__main__":
    simulacao_rede = SimuladorRede(limite_randomicos=100000)
    simulacao_rede.executar()