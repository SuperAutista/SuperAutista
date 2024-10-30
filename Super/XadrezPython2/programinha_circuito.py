# Autor: Luiz Tiago Wilcke

import tkinter as tk
from tkinter import messagebox
from tkinter import colorchooser

# Definição das classes de componentes

class Componente:
    def __init__(self, tipo, x, y):
        self.tipo = tipo
        self.x = x
        self.y = y
        self.id = None  # ID do componente no canvas
        self.conexoes = []  # Lista de conexões (fios)

class Wire:
    def __init__(self, inicio, fim):
        self.inicio = inicio  # Componente de início
        self.fim = fim        # Componente de fim
        self.id = None        # ID do fio no canvas

class CircuitoMaker:
    def __init__(self, master):
        self.master = master
        self.master.title("Circuit Maker Avançado")
        self.master.geometry("1200x800")

        # Lista de componentes e fios
        self.componentes = []
        self.fios = []

        # Ferramentas
        self.ferramenta_atual = tk.StringVar(value="Nenhuma")
        self.cor_led = "red"

        # Estado para desenhar fios
        self.fio_iniciado = False
        self.componente_inicio = None

        self.criar_barras_de_ferramenta()

        # Canvas para desenhar o circuito
        self.canvas = tk.Canvas(self.master, bg="white", width=1000, height=800)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Eventos de clique no canvas
        self.canvas.bind("<Button-1>", self.acao_canvas)
        self.canvas.bind("<B1-Motion>", self.arrastar_componente)
        self.canvas.bind("<ButtonRelease-1>", self.soltar_componente)

        # Variáveis para arrastar componentes
        self.componente_arrastando = None
        self.offset_x = 0
        self.offset_y = 0

    def criar_barras_de_ferramenta(self):
        barra_ferramenta = tk.Frame(self.master, padx=5, pady=5)
        barra_ferramenta.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(barra_ferramenta, text="Ferramentas", font=("Arial", 14)).pack(pady=10)

        botoes = [
            ("Resistor", "Resistor"),
            ("Fonte de Tensão", "FonteTensao"),
            ("Transistor", "Transistor"),
            ("Diodo", "Diodo"),
            ("LED", "LED"),
            ("Fio", "Fio"),
            ("Simular", "Simular"),
            ("Limpar", "Limpar")
        ]

        for texto, valor in botoes:
            tk.Radiobutton(
                barra_ferramenta, text=texto, variable=self.ferramenta_atual, value=valor
            ).pack(anchor=tk.W, pady=2)

        # Opções para cor do LED
        tk.Label(barra_ferramenta, text="Cor do LED:", font=("Arial", 12)).pack(pady=5)
        cores_led = ["Vermelho", "Verde", "Azul"]
        for cor in cores_led:
            tk.Radiobutton(
                barra_ferramenta, text=cor, variable=tk.StringVar(value="red"), 
                value=cor.lower(), command=lambda c=cor.lower(): self.set_cor_led(c)
            ).pack(anchor=tk.W)

        tk.Button(barra_ferramenta, text="Aplicar", command=self.aplicar_ferramenta).pack(pady=20)

    def set_cor_led(self, cor):
        self.cor_led = cor

    def aplicar_ferramenta(self):
        ferramenta = self.ferramenta_atual.get()
        if ferramenta == "Limpar":
            self.canvas.delete("all")
            self.componentes.clear()
            self.fios.clear()
            messagebox.showinfo("Limpar", "Circuito limpo com sucesso!")
        elif ferramenta == "Simular":
            self.simular_circuito()
        else:
            messagebox.showinfo("Ferramenta Selecionada", f"Ferramenta atual: {ferramenta}")

    def acao_canvas(self, event):
        ferramenta = self.ferramenta_atual.get()
        x, y = event.x, event.y

        if ferramenta in ["Resistor", "FonteTensao", "Transistor", "Diodo", "LED"]:
            componente = Componente(ferramenta, x, y)
            self.desenhar_componente(componente)
            self.componentes.append(componente)
        elif ferramenta == "Fio":
            componente = self.encontrar_componente_proximo(x, y)
            if componente:
                if not self.fio_iniciado:
                    self.fio_iniciado = True
                    self.componente_inicio = componente
                else:
                    if componente != self.componente_inicio:
                        self.criar_fio(self.componente_inicio, componente)
                        self.fio_iniciado = False
                        self.componente_inicio = None
        else:
            # Seleção ou outra ferramenta
            pass

    def encontrar_componente_proximo(self, x, y, raio=20):
        for componente in self.componentes:
            if abs(componente.x - x) <= raio and abs(componente.y - y) <= raio:
                return componente
        return None

    def criar_fio(self, inicio, fim):
        fio = Wire(inicio, fim)
        fio.id = self.canvas.create_line(inicio.x, inicio.y, fim.x, fim.y, fill="black", width=2)
        self.fios.append(fio)
        # Adicionar conexão aos componentes
        inicio.conexoes.append(fio)
        fim.conexoes.append(fio)

    def desenhar_componente(self, componente):
        tipo = componente.tipo
        x, y = componente.x, componente.y

        if tipo == "Resistor":
            comprimento, altura = 60, 20
            componente.id = self.canvas.create_rectangle(
                x, y, x + comprimento, y + altura, fill="orange"
            )
            self.canvas.create_text(x + comprimento / 2, y + altura / 2, text="R", fill="white")
        elif tipo == "FonteTensao":
            comprimento, altura = 60, 40
            componente.id = self.canvas.create_rectangle(
                x, y, x + comprimento, y + altura, fill="red"
            )
            self.canvas.create_text(x + comprimento / 2, y + altura / 2, text="V", fill="white")
        elif tipo == "Transistor":
            comprimento, altura = 40, 60
            componente.id = self.canvas.create_polygon(
                x, y, x + comprimento, y + altura / 2, x, y + altura, x + comprimento, y + altura / 2,
                fill="blue"
            )
            self.canvas.create_text(x + comprimento / 2, y + altura / 2, text="T", fill="white")
        elif tipo == "Diodo":
            comprimento, altura = 40, 20
            componente.id = self.canvas.create_polygon(
                x, y, x + comprimento, y + altura / 2, x, y + altura,
                fill="yellow"
            )
            self.canvas.create_text(x + comprimento / 2, y + altura / 2, text="D", fill="black")
        elif tipo == "LED":
            comprimento, altura = 40, 20
            componente.id = self.canvas.create_oval(
                x, y, x + comprimento, y + altura, fill=self.cor_led
            )
            self.canvas.create_text(x + comprimento / 2, y + altura / 2, text="LED", fill="white")

    def arrastar_componente(self, event):
        if self.componente_arrastando:
            x, y = event.x, event.y
            self.canvas.coords(
                self.componente_arrastando.id,
                x - self.offset_x, y - self.offset_y,
                x - self.offset_x + 60, y - self.offset_y + 20
            )
            self.componente_arrastando.x = x - self.offset_x
            self.componente_arrastando.y = y - self.offset_y
            # Atualizar fios conectados
            for fio in self.componente_arrastando.conexoes:
                if fio.inicio == self.componente_arrastando:
                    self.canvas.coords(fio.id, fio.inicio.x, fio.inicio.y, fio.fim.x, fio.fim.y)
                elif fio.fim == self.componente_arrastando:
                    self.canvas.coords(fio.id, fio.inicio.x, fio.inicio.y, fio.fim.x, fio.fim.y)

    def soltar_componente(self, event):
        self.componente_arrastando = None

    def simular_circuito(self):
        # Simulação simples: acender LEDs se estiverem conectados a uma fonte de tensão
        # Este é um exemplo básico e não representa uma simulação real
        for componente in self.componentes:
            if componente.tipo == "LED":
                conectado = False
                for fio in componente.conexoes:
                    if fio.inicio.tipo == "FonteTensao" or fio.fim.tipo == "FonteTensao":
                        conectado = True
                        break
                if conectado:
                    # Acender LED com sua cor
                    self.canvas.itemconfig(componente.id, fill=componente.id.split()[-1])
                else:
                    # Apagar LED
                    self.canvas.itemconfig(componente.id, fill="grey")

    # Método para selecionar e arrastar componentes
    def selecionar_componente(self, event):
        x, y = event.x, event.y
        componente = self.encontrar_componente_proximo(x, y)
        if componente:
            self.componente_arrastando = componente
            self.offset_x = x - componente.x
            self.offset_y = y - componente.y

def main():
    root = tk.Tk()
    app = CircuitoMaker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
