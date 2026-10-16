
"""APS: entrega de pacote em grid. Execute: python interface.py"""

import heapq
import itertools
import random
import tkinter as tk
from tkinter import messagebox

# HIPÓTESE TEMPORÁRIA:
# Custo 1 por ação, com acréscimo de 4 em células de pedágio.
PEDAGIO_EXTRA = 4

MOVIMENTOS = {
    "cima": (-1, 0),
    "baixo": (1, 0),
    "esquerda": (0, -1),
    "direita": (0, 1),
}


def gerar_mapa(n):
    casas = [(i, j) for i in range(n) for j in range(n)]
    random.shuffle(casas)

    inicio, pacote, destino = casas[:3]
    restantes = casas[3:]

    qtd_obstaculos = int(len(restantes) * 0.20)
    qtd_pedagios = int(len(restantes) * 0.10)

    obstaculos = set(restantes[:qtd_obstaculos])
    pedagios = set(
        restantes[qtd_obstaculos:qtd_obstaculos + qtd_pedagios]
    )

    return inicio, pacote, destino, obstaculos, pedagios


def heuristica(estado, destino):
    pos, pacote, carregando, entregue = estado

    if entregue:
        return 0

    def distancia(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    if carregando:
        return distancia(pos, destino) + 1

    return (
        distancia(pos, pacote)
        + distancia(pacote, destino)
        + 2
    )


def buscar(n, inicio, pacote, destino, obstaculos, pedagios):
    """Executa A* e retorna estados, ações e custo."""

    inicial = (inicio, pacote, False, False)

    contador = itertools.count()

    fila = [
        (heuristica(inicial, destino), next(contador), 0, inicial)
    ]

    custos = {inicial: 0}
    pais = {}

    while fila:
        _, _, custo, estado = heapq.heappop(fila)

        if custo != custos[estado]:
            continue

        pos, pacote_atual, carregando, entregue = estado

        if entregue:
            estados = [estado]
            acoes = []

            while estado in pais:
                anterior, acao = pais[estado]
                estados.append(anterior)
                acoes.append(acao)
                estado = anterior

            return estados[::-1], acoes[::-1], custo

        proximos = []

        # Movimentos do agente
        for acao, (di, dj) in MOVIMENTOS.items():
            novo = (pos[0] + di, pos[1] + dj)

            if not (0 <= novo[0] < n and 0 <= novo[1] < n):
                continue

            if novo in obstaculos:
                continue

            nova_pos_pacote = novo if carregando else pacote_atual

            proximos.append((
                acao,
                (novo, nova_pos_pacote, carregando, False)
            ))

        # Pegar pacote
        if not carregando and pos == pacote_atual:
            proximos.append((
                "pegar",
                (pos, pos, True, False)
            ))

        # Entregar pacote
        if carregando and pos == destino:
            proximos.append((
                "entregar",
                (pos, pos, False, True)
            ))

        # Avaliar sucessores
        for acao, proximo in proximos:

            novo_custo = (
                custo
                + 1
                + (PEDAGIO_EXTRA if pos in pedagios else 0)
            )

            if novo_custo < custos.get(proximo, float("inf")):
                custos[proximo] = novo_custo
                pais[proximo] = (estado, acao)

                prioridade = (
                    novo_custo + heuristica(proximo, destino)
                )

                heapq.heappush(
                    fila,
                    (
                        prioridade,
                        next(contador),
                        novo_custo,
                        proximo
                    )
                )

    return None


class Interface:

    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Entrega de pacote - APS")

        barra = tk.Frame(self.janela)
        barra.pack(pady=8)

        tk.Label(
            barra,
            text="Dimensão:"
        ).pack(side="left")

        self.entrada = tk.Entry(barra, width=5)
        self.entrada.insert(0, "10")
        self.entrada.pack(side="left", padx=5)

        tk.Button(
            barra,
            text="Gerar mapa",
            command=self.gerar
        ).pack(side="left", padx=4)

        tk.Button(
            barra,
            text="Resolver",
            command=self.resolver
        ).pack(side="left", padx=4)

        self.mensagem = tk.Label(self.janela, text="")
        self.mensagem.pack(pady=4)

        self.canvas = tk.Canvas(self.janela, bg="white")
        self.canvas.pack(padx=10, pady=10)

        self.dados = None
        self.gerar()

    def gerar(self):
        try:
            n = int(self.entrada.get())

            if n < 2 or n > 50:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Erro",
                "Digite uma dimensão entre 2 e 50."
            )
            return

        self.n = n
        self.dados = gerar_mapa(n)

        self.mensagem.config(
            text="A: agente | P: pacote | X: destino | cinza: pedágio"
        )

        self.desenhar()

    def desenhar(self, caminho=None):
        inicio, pacote, destino, obstaculos, pedagios = self.dados

        lado = min(40, max(10, 650 // self.n))

        self.canvas.config(
            width=lado * self.n,
            height=lado * self.n
        )

        self.canvas.delete("all")

        rota = set(caminho or [])

        for i in range(self.n):
            for j in range(self.n):
                pos = (i, j)

                cor = "#cde8ff" if pos in rota else "white"

                if pos in pedagios:
                    cor = "#aaaaaa"

                if pos in obstaculos:
                    cor = "#222222"

                self.canvas.create_rectangle(
                    j * lado,
                    i * lado,
                    (j + 1) * lado,
                    (i + 1) * lado,
                    fill=cor,
                    outline="#dddddd"
                )

                marca = (
                    "A" if pos == inicio else
                    "P" if pos == pacote else
                    "X" if pos == destino else
                    ""
                )

                if marca:
                    self.canvas.create_text(
                        (j + 0.5) * lado,
                        (i + 0.5) * lado,
                        text=marca,
                        font=("Arial", max(8, lado // 3), "bold")
                    )

    def resolver(self):
        if self.dados is None:
            return

        resultado = buscar(self.n, *self.dados)

        if resultado is None:
            self.mensagem.config(
                text="Não existe solução para este mapa."
            )
            self.desenhar()
            return

        estados, acoes, custo = resultado

        self.desenhar([
            estado[0] for estado in estados
        ])

        self.mensagem.config(
            text=f"{len(acoes)} ações | custo total: {custo}"
        )

        print("Plano:", " -> ".join(acoes))
        print("Custo:", custo)

    def executar(self):
        self.janela.mainloop()


if __name__ == "__main__":
    Interface().executar()
