import heapq
import yaml
import sys


class Fila:
    def __init__(self, nome, servidores, capacidade, intervalo_chegada, intervalo_atendimento, routing):
        self.nome = nome
        self.servidores = servidores
        self.capacidade = capacidade
        self.intervalo_chegada = intervalo_chegada       # (min, max) ou None se sem chegada externa
        self.intervalo_atendimento = intervalo_atendimento
        self.routing = routing                           # {fila_destino: probabilidade}

        self.em_espera = 0
        self.em_servico = 0
        self.tempo_estados = [0.0] * (capacidade + 1)  # índice i = tempo com i clientes no sistema
        self.ultimo_evento = 0.0
        self.perdidos = 0

    def total_clientes(self):
        return self.em_servico + self.em_espera

    def contabilizar(self, novo_tempo):
        # acumula o tempo no estado atual antes de qualquer mudança
        self.tempo_estados[self.total_clientes()] += novo_tempo - self.ultimo_evento
        self.ultimo_evento = novo_tempo


class SimuladorRede:

    # Gerador LCG (M2)
    _A    = 1103515245
    _C    = 12345
    _M    = 2 ** 31
    _SEED = 12345

    def __init__(self, config):
        sim_cfg = config.get('simulation', {})
        self.limite = int(sim_cfg.get('num_randomicos', 100000))
        self.primeira_chegada = float(sim_cfg.get('primeira_chegada', 2.0))

        self._rand   = self._SEED
        self._usados = 0

        # cria as filas a partir do arquivo .yml
        self.filas = {}
        for nome, cfg in config['queues'].items():
            chegada = tuple(cfg['chegada']) if cfg.get('chegada') else None
            routing = {str(k): float(v) for k, v in (cfg.get('rede') or {}).items()}
            self.filas[nome] = Fila(
                nome=nome,
                servidores=int(cfg['servidores']),
                capacidade=int(cfg['capacidade']),
                intervalo_chegada=chegada,
                intervalo_atendimento=tuple(cfg['atendimento']),
                routing=routing,
            )

        self.relogio = 0.0
        self._agenda = []
        self._seq    = 0   # desempata eventos com mesmo tempo

    # Gerador 

    def _proximo_random(self):
        self._rand    = (self._A * self._rand + self._C) % self._M
        self._usados += 1
        return self._rand / self._M

    def _uniforme(self, a, b):
        return a + (b - a) * self._proximo_random()

    def _pode(self):
        return self._usados < self.limite

    # Agenda 

    def _agendar(self, tempo, tipo, nome):
        self._seq += 1
        heapq.heappush(self._agenda, (tempo, self._seq, tipo, nome))

    # Roteamento 

    def _sortear_destino(self, routing):
        items = list(routing.items())
        # destino único com prob 1.0: não consome aleatório
        if len(items) == 1 and abs(items[0][1] - 1.0) < 1e-9:
            return items[0][0]
        if not self._pode():
            return 'saida'
        # roleta: sorteia destino com base nas probabilidades
        u = self._proximo_random()
        acumulado = 0.0
        for destino, prob in items:
            acumulado += prob
            if u <= acumulado:
                return destino
        return 'saida'

    # Eventos 

    def _inserir_cliente(self, nome):
        fila = self.filas[nome]
        if fila.em_servico < fila.servidores:
            fila.em_servico += 1
            if self._pode():
                dt = self._uniforme(*fila.intervalo_atendimento)
                self._agendar(self.relogio + dt, 'SAIDA', nome)
        elif fila.total_clientes() < fila.capacidade:
            fila.em_espera += 1
        else:
            fila.perdidos += 1  # sistema cheio: cliente perdido

    def _chegada(self, nome):
        fila = self.filas[nome]
        if fila.intervalo_chegada and self._pode():
            dt = self._uniforme(*fila.intervalo_chegada)
            self._agendar(self.relogio + dt, 'CHEGADA', nome)
        self._inserir_cliente(nome)

    def _saida(self, nome):
        fila = self.filas[nome]
        if fila.em_espera > 0:
            # próximo da fila ocupa o servidor
            fila.em_espera -= 1
            if self._pode():
                dt = self._uniforme(*fila.intervalo_atendimento)
                self._agendar(self.relogio + dt, 'SAIDA', nome)
        else:
            fila.em_servico -= 1  # servidor fica livre

        # roteia o cliente para a próxima fila ou para fora do sistema
        if fila.routing:
            destino = self._sortear_destino(fila.routing)
            if destino != 'saida' and destino in self.filas:
                self._inserir_cliente(destino)

    def _contabilizar(self, novo_tempo):
        for fila in self.filas.values():
            fila.contabilizar(novo_tempo)

    # Laço principal 

    def executar(self):
        # agenda a primeira chegada de cada fila com chegada externa
        for nome, fila in self.filas.items():
            if fila.intervalo_chegada:
                self._agendar(self.primeira_chegada, 'CHEGADA', nome)

        # processa eventos até esgotar os aleatórios
        while self._agenda and self._pode():
            tempo, _, tipo, nome = heapq.heappop(self._agenda)
            self._contabilizar(tempo)
            self.relogio = tempo
            if tipo == 'CHEGADA':
                self._chegada(nome)
            elif tipo == 'SAIDA':
                self._saida(nome)

        self._imprimir_resultados()

    def _imprimir_resultados(self):
        sep = '=' * 56
        print(f'\n{sep}')
        print('  SIMULAÇÃO DE REDE DE FILAS')
        print(sep)

        for nome, fila in self.filas.items():
            tempo_total = sum(fila.tempo_estados)
            print(f'\n  Fila {nome}  [G/G/{fila.servidores}/{fila.capacidade}]')
            print(f'  {"-" * 50}')
            for estado, tempo in enumerate(fila.tempo_estados):
                prob = tempo / tempo_total if tempo_total > 0 else 0.0
                print(f'    Estado {estado:2d}: tempo = {tempo:12.4f}  |  prob = {prob:.6f}')
            print(f'  {"-" * 50}')
            print(f'    Clientes perdidos : {fila.perdidos}')

        print(f'\n{sep}')
        print(f'  Tempo global da simulação : {self.relogio:.4f}')
        print(f'  Randomicos utilizados     : {self._usados}')
        print(f'{sep}\n')


if __name__ == '__main__':
    arquivo = sys.argv[1] if len(sys.argv) > 1 else 'modelo.yml'
    with open(arquivo, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    sim = SimuladorRede(config)
    sim.executar()
