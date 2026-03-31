import heapq


# M2 - Gerador LCG

#paramentros do gerador
a = 1103515245
c = 12345
M = 2**31
seed = 12345

#guarda o último número gerado
_last_random = seed


def next_random():
    """Gera um número pseudoaleatório uniforme entre 0 e 1."""
    global _last_random
    _last_random = (a * _last_random + c) % M
    return _last_random / M


def uniforme(minimo, maximo):
    """Converte o valor do LCG para uma uniforme no intervalo [minimo, maximo]."""
    u = next_random()
    return minimo + (maximo - minimo) * u



# M4 - Simulador de Filas

class SimuladorEventos:
    def __init__(self, num_servidores=1, capacidade_sistema=5, limite_randomicos=100000):
        #parametros do sistema
        self.num_servidores = num_servidores 
        self.capacidade_sistema = capacidade_sistema 
        self.limite_randomicos = limite_randomicos 


        #atributos 
        self.relogio = 0.0 
        self.eventos = [] 
        self.fila_espera = [] 

        self.ocupados = 0 
        self.randomicos_utilizados = 0 

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

    def adicionar_evento(self, instante, tipo):
        heapq.heappush(self.eventos, (instante, tipo))

    def gerar_interchegada(self):
        if self.randomicos_utilizados >= self.limite_randomicos:
            return None
        self.randomicos_utilizados += 1
        return uniforme(2.0, 5.0)

    def gerar_atendimento(self):
        if self.randomicos_utilizados >= self.limite_randomicos:
            return None
        self.randomicos_utilizados += 1
        return uniforme(3.0, 5.0)

    def processar_chegada(self):
        proxima_chegada = self.gerar_interchegada()
        if proxima_chegada is not None:
            self.adicionar_evento(self.relogio + proxima_chegada, "CHEGADA")

        if self.ocupados < self.num_servidores:
            self.ocupados += 1
            tempo_servico = self.gerar_atendimento()
            if tempo_servico is not None:
                self.adicionar_evento(self.relogio + tempo_servico, "SAIDA")
        else:
            if self.clientes_no_sistema() < self.capacidade_sistema:
                self.fila_espera.append(self.relogio)
            else:
                self.total_perdidos += 1

    def processar_saida(self):
        self.total_atendidos += 1

        if len(self.fila_espera) > 0:
            self.fila_espera.pop(0)
            tempo_servico = self.gerar_atendimento()
            if tempo_servico is not None:
                self.adicionar_evento(self.relogio + tempo_servico, "SAIDA")
        else:
            self.ocupados -= 1

    def executar(self, primeira_chegada=2.0):
        self.relogio = primeira_chegada
        self.ultimo_tempo = 0.0
        self.adicionar_evento(primeira_chegada, "CHEGADA")

        while self.eventos and self.randomicos_utilizados < self.limite_randomicos:
            instante, tipo = heapq.heappop(self.eventos)

            self.registrar_tempo_estado(instante)
            self.relogio = instante

            if tipo == "CHEGADA":
                self.processar_chegada()
            elif tipo == "SAIDA":
                self.processar_saida()

        self.mostrar_resultados()

    def mostrar_resultados(self):
        tempo_total = sum(self.tempo_estados)

        print(f"\nSimulação G/G/{self.num_servidores}/{self.capacidade_sistema}")
        print("-" * 40)

        for estado, tempo in enumerate(self.tempo_estados):
            prob = tempo / tempo_total if tempo_total > 0 else 0.0
            print(
                f"Estado {estado}: "
                f"tempo = {tempo:.2f} | probabilidade = {prob:.4f}"
            )

        print("-" * 40)
        print(f"Tempo total simulado: {tempo_total:.2f}")
        print(f"Clientes atendidos: {self.total_atendidos}")
        print(f"Clientes perdidos: {self.total_perdidos}")


if __name__ == "__main__":
    simulacao_1 = SimuladorEventos(num_servidores=1, capacidade_sistema=5, limite_randomicos=100000)
    simulacao_1.executar()

    simulacao_2 = SimuladorEventos(num_servidores=2, capacidade_sistema=5, limite_randomicos=100000)
    simulacao_2.executar()
