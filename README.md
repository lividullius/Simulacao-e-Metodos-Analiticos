# Simulacao e Metodos Analiticos
Repositório para desenvolvimento das atividades da cadeira Simulação e Métodos Analíticos

## M2 - Gerador de números pseudoaleatórios (0 a 1)

Para gerar números pseudoaleatórios, foi utilizado o método da congruência linear, onde cada valor é calculado a partir do anterior e depois normalizado para ficar entre 0 e 1.

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

