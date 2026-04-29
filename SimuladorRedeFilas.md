# Simulador Generalizado Para Rede de Filas
Este simulador suporta qualquer topologia de rede de filas definida em um arquivo de configuração YAML.

## Requisitos
- Python 3.8+
- PyYAML: `pip install pyyaml`
- O gerador LCG já está embutido no próprio simulador (não precisa de arquivo externo)

## Como usar
Executar o simulador:
```
python simulador_rede_filas.py
```

Especificar arquivo de configuração:
```
python simulador_rede_filas.py modelo.yml
```
- Pressione Enter para usar o arquivo padrão `modelo.yml`
- Ou passe o nome de outro arquivo YAML como argumento

## Formato do arquivo de configuração YAML
```yaml
simulation:
  num_randomicos: 100000    # Máximo de números aleatórios
  primeira_chegada: 2.0     # Tempo da primeira chegada

queues:
  nome_fila:
    servidores: 1           # Número de servidores (c)
    capacidade: 5           # Capacidade total do sistema (K)
    chegada: [2.0, 4.0]     # Intervalo de chegada externa [min, max]
                            # Use null se não houver chegada externa
    atendimento: [1.0, 2.0] # Intervalo de atendimento [min, max]
    rede:                   # Roteamento probabilístico
      fila_destino: 0.8     # 80% vão para fila_destino
                            # O restante até 1.0 sai do sistema
                            # Omita "rede" para saída total (100%)
```

## Exemplo de configuração (modelo.yml)
O arquivo `modelo.yml` implementa a rede com 3 filas conforme a especificação:

- Q1: G/G/1 (1 servidor, capacidade 10)
- Q2: G/G/2/5 (2 servidores, capacidade 5)
- Q3: G/G/2/10 (2 servidores, capacidade 10)

Com roteamento probabilístico:

- Q1 → Q2 (80%), Q3 (20%)
- Q2 → Q1 (30%), Q3 (50%), saída (20%)
- Q3 → Q2 (70%), saída (30%)

## Saída do simulador
O simulador produz um relatório contendo:

- **Informações gerais:** tempo global da simulação e total de aleatórios usados
- **Para cada fila:**
  - Configuração no formato G/G/c/K
  - Clientes perdidos (chegaram com fila cheia)
  - Distribuição de probabilidades por estado
  - Tempo acumulado em cada estado

## Validação
O simulador foi testado com 100.000 números aleatórios, iniciando com filas vazias e primeira chegada no tempo 2.0, conforme especificado. Os resultados foram validados comparando uma fila única com o simulador M4, obtendo valores idênticos de tempo e probabilidade para cada estado.

## Estrutura do código
- **Fila:** classe que representa uma fila individual da rede
- **SimuladorRede:** classe principal que gerencia toda a rede de filas
- Eventos são gerenciados por uma heap (fila de prioridade)
- Suporte a roteamento probabilístico entre filas (roleta)
- Gerador LCG embutido com as constantes do módulo M2
- Coleta automática de estatísticas de tempo por estado

## Arquivos

|---|---|
| `simulador_rede_filas.py` | Código principal do simulador |
| `modelo.yml` | Rede com 3 filas e feedback probabilístico |
