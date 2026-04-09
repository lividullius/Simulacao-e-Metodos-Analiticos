# Simulacao e Metodos Analiticos
Repositório para desenvolvimento das atividades da cadeira Simulação e Métodos Analíticos

## M2 - Gerador de números pseudoaleatórios (0 a 1)

Para gerar números pseudoaleatórios, foi utilizado o método da congruência linear (LCG), onde cada valor é calculado a partir do anterior e depois normalizado para ficar entre 0 e 1.

    Declarar:
        a, c, M, X0 : inteiro
        X : inteiro
        i, N : inteiro
    
    Início
        Ler a
        Ler c
        Ler M
        Ler X0
        Ler N
    
        X ← X0
    
        Para i de 1 até N faça
            X ← (a * X + c) mod M
            U ← X / M
            Escrever U
        FimPara
    Fim


## M4 - Simulador de filas orientado a eventos

Simulador de filas baseado em eventos discretos, utilizando números pseudoaleatórios gerados pelo método da congruência linear (LCG).
A simulação é controlada por uma lista de eventos (agenda), onde cada evento pode ser uma chegada ou uma saída. O sistema evolui no tempo conforme esses eventos são processados.

    Início
    
    Inicializar variáveis do sistema
    Definir count como limite de números pseudoaleatórios
    
    Criar lista de eventos vazia
    Inserir primeira chegada na agenda
    
    Enquanto houver eventos e count > 0 faça:
    
        Selecionar e remover o próximo evento da agenda
    
        Atualizar o tempo acumulado do estado atual
        Atualizar o relógio da simulação para o tempo do evento
    
        Se o evento for CHEGADA então:
            Gerar e agendar a próxima chegada
    
            Se existir servidor disponível então:
                iniciar atendimento
                agendar uma SAÍDA
            Senão:
                se houver espaço na fila então:
                    adicionar cliente à fila
                fim se
            fim se
        fim se
    
        Se o evento for SAÍDA então:
            liberar o servidor
    
            Se houver clientes na fila então:
                remover cliente da fila
                iniciar novo atendimento
                agendar próxima SAÍDA
            fim se
        fim se
    
    Fim enquanto

# M6 - Simulador de rede de filas em tandem

Extensão do simulador para suportar uma rede de filas conectadas em série (tandem).  
Nesse modelo, os clientes chegam inicialmente na Fila 1 e, após o atendimento, são encaminhados para a Fila 2. Após o atendimento na segunda fila, o cliente deixa o sistema.

    Início

    Inicializar variáveis do sistema  
    Definir count como limite de números pseudoaleatórios  
    Inicializar relógio da simulação em 0  

    Criar duas filas:

    Fila 1:
    - número de servidores  
    - capacidade total  
    - intervalo de chegadas externas  
    - intervalo de atendimento  
    - contadores inicializados  

    Fila 2:
    - número de servidores  
    - capacidade total  
    - apenas intervalo de atendimento  
    - contadores inicializados  

    Criar lista de eventos vazia  

    Agendar primeira chegada externa na Fila 1 no tempo 1.5  

    Enquanto houver eventos e count > 0 faça:

    Selecionar e remover o próximo evento da agenda  

    Atualizar o tempo acumulado dos estados de cada fila  

    Atualizar o relógio para o tempo do evento  


    Evento CHEGADA_EXTERNA_FILA1

    Gerar e agendar próxima chegada externa  

    Processar entrada na Fila 1:

    Se houver servidor livre então  
     iniciar atendimento  
     agendar SAÍDA da Fila 1  

    Senão se houver espaço na fila então  
     cliente entra na fila  

    Senão  
     cliente é perdido  
    fim se  

 
    Evento SAIDA_FILA1

    Registrar cliente atendido na Fila 1  

    Se houver cliente aguardando então  
     remover cliente da fila  
     iniciar atendimento  
     agendar próxima SAÍDA  
    Senão  
     liberar servidor  
    fim se  

    Encaminhar cliente para a Fila 2  

    Processar chegada na Fila 2:

    Se houver servidor livre então  
     iniciar atendimento  
     agendar SAÍDA da Fila 2  

    Senão se houver espaço na fila então  
     cliente entra na fila  

    Senão  
     cliente é perdido  
    fim se  


    Evento SAIDA_FILA2

    Registrar cliente atendido na Fila 2  

    Se houver clientes na fila então  
     remover cliente da fila  
     iniciar atendimento  
     agendar nova SAÍDA  
    Senão  
     liberar servidor  
    fim se  

    Fim enquanto


    Cálculo das probabilidades

    Para cada fila i:
        Para cada estado k:
            prob[k] ← tempo_estado[k] / tempo_total


Para cada fila:

- configuração da fila (G/G/servidores/capacidade)  
- tempo acumulado por estado  
- distribuição de probabilidades  
- número de clientes atendidos  
- número de clientes perdidos  

- tempo global da simulação
