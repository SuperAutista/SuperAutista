import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.integrate import odeint

class ModeloDoomsdayApp:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Modelo Doomsday")
        self.raiz.geometry("800x600")
        self.raiz.minsize(800, 600)

        # Configurar abas
        self.abas = ttk.Notebook(self.raiz)
        self.aba_modelo = ttk.Frame(self.abas)
        self.aba_explicacao = ttk.Frame(self.abas)
        self.abas.add(self.aba_modelo, text="Calculadora")
        self.abas.add(self.aba_explicacao, text="Explicação")
        self.abas.pack(expand=1, fill="both")

        self.criar_widgets_modelo()
        self.criar_widgets_explicacao()

    def criar_widgets_modelo(self):
        # Frame para entradas
        frame_entradas = ttk.Frame(self.aba_modelo, padding="10")
        frame_entradas.pack(side=tk.LEFT, fill=tk.Y)

        # População inicial
        ttk.Label(frame_entradas, text="População Inicial:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.pop_inicial = tk.DoubleVar(value=8000000000)  # 8 bilhões
        ttk.Entry(frame_entradas, textvariable=self.pop_inicial).grid(row=0, column=1, pady=5)

        # Taxa de declínio (k)
        ttk.Label(frame_entradas, text="Taxa de Declínio (k):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.taxa_declinio = tk.DoubleVar(value=0.01)
        ttk.Entry(frame_entradas, textvariable=self.taxa_declinio).grid(row=1, column=1, pady=5)

        # Tempo (anos)
        ttk.Label(frame_entradas, text="Tempo (anos):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.tempo_max = tk.IntVar(value=100)
        ttk.Entry(frame_entradas, textvariable=self.tempo_max).grid(row=2, column=1, pady=5)

        # Botão para calcular
        ttk.Button(frame_entradas, text="Calcular", command=self.calcular_modelo).grid(row=3, column=0, columnspan=2, pady=10)

        # Frame para gráfico
        frame_grafico = ttk.Frame(self.aba_modelo)
        frame_grafico.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.figura, self.ax = plt.subplots(figsize=(5,5))
        self.canvas = FigureCanvasTkAgg(self.figura, master=frame_grafico)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Autor
        self.ax.legend(["Modelo Doomsday"], loc='upper right', fontsize='small', labelcolor="blue")
        self.figura.suptitle("Modelo Doomsday por Luiz Tiago Wilcke", color="blue")

    def criar_widgets_explicacao(self):
        explicacao = """
        Este modelo simula a diminuição da população humana ao longo do tempo devido a um evento catastrófico.
        
        Equação Diferencial:
        dP/dt = -kP
        
        Solução:
        P(t) = P₀ * e^(-kt)
        
        Parâmetros:
        - População Inicial (P₀): Número de seres humanos no início da simulação.
        - Taxa de Declínio (k): Taxa constante de diminuição da população.
        - Tempo (t): Período em anos para a simulação.
        
        Como Usar:
        1. Insira os valores desejados para a população inicial, taxa de declínio e tempo.
        2. Clique em "Calcular" para visualizar a projeção da população ao longo do tempo.
        """
        ttk.Label(self.aba_explicacao, text=explicacao, justify=tk.LEFT, padding=10).pack(fill=tk.BOTH, expand=True)

    def calcular_modelo(self):
        try:
            P0 = self.pop_inicial.get()
            k = self.taxa_declinio.get()
            tempo = self.tempo_max.get()

            if P0 <= 0 or k <= 0 or tempo <=0:
                raise ValueError

            # Definir o tempo
            t = np.linspace(0, tempo, 1000)

            # Definir a equação diferencial
            def dPdt(P, t):
                return -k * P

            # Resolver a equação diferencial
            P = odeint(dPdt, P0, t)
            P = P.flatten()

            # Limitar a população a não ser negativa
            P = np.maximum(P, 0)

            # Limpar o gráfico anterior
            self.ax.clear()

            # Plotar os resultados
            self.ax.plot(t, P, label="População", color="green")
            self.ax.set_xlabel("Anos")
            self.ax.set_ylabel("População")
            self.ax.set_title("Projeção da População Humana")
            self.ax.legend(["Modelo Doomsday"], loc='upper right', fontsize='small', labelcolor="blue")
            self.figura.suptitle("Modelo Doomsday por Luiz Tiago Wilcke", color="blue")

            self.canvas.draw()

        except Exception:
            messagebox.showerror("Erro", "Por favor, insira valores válidos.")

if __name__ == "__main__":
    raiz = tk.Tk()
    app = ModeloDoomsdayApp(raiz)
    raiz.mainloop()
