
# Entrega de Pacotes em Grid

Projeto desenvolvido para a disciplina de Inteligência Artificial e Robótica.

## Objetivo

Implementar um agente capaz de encontrar uma sequência ótima de ações para coletar e entregar um pacote em um grid quadrado contendo obstáculos e pedágios.

## Funcionalidades

- Geração aleatória de mapas NxN
- Posicionamento aleatório do agente
- Posicionamento aleatório do pacote
- Posicionamento aleatório do destino
- Geração de obstáculos e pedágios
- Busca de caminho utilizando A*
- Cálculo do custo das ações
- Identificação de cenários sem solução
- Visualização gráfica com Tkinter

## Algoritmo

Foi utilizado o algoritmo A*, que seleciona os estados considerando:

f(n) = g(n) + h(n)

Onde:

- g(n): custo acumulado desde o estado inicial.
- h(n): estimativa do custo restante até a entrega.
- f(n): prioridade utilizada na busca.

A heurística considera a distância de Manhattan entre o agente, o pacote e o destino, além das ações necessárias para pegar e entregar.

## Estrutura

interface.py
requirements.txt
README.md

## Execução

Execute:

python interface.py

Na interface, informe a dimensão do grid, gere um mapa e clique em Resolver.

## Observação

A fórmula de pedágio ainda precisa ser confirmada conforme o enunciado oficial.

Atualmente, cada ação custa 1, com acréscimo de 4 quando executada em uma célula com pedágio.
