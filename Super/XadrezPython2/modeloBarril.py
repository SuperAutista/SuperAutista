import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.integrate import odeint
import csv

class ModeloPetroleoApp:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Modelo Avançado do Preço do Petróleo")
        self.raiz.geometry("1000x700")
        self.raiz.minsize(1000, 700)

        # Configurar as abas
        self.abas = ttk.Notebook(self.raiz)
        self.aba_modelo = ttk.Frame(self.abas)
        self.aba_explicacao = ttk.Frame(self.abas)
        self.abas.add(self.aba_modelo, text="Simulação")
        self.abas.add(self.aba_explicacao, text="Explicação")
        self.abas.pack(expand=1, fill="both")

        self.criar_widgets_modelo()
        self.criar_widgets_explicacao()

    def criar_widgets_modelo(self):
        # Frame para entradas
        frame_entradas = ttk.Frame(self.aba_modelo, padding="10")
        frame_entradas.pack(side=tk.LEFT, fill=tk.Y)

        # Preço inicial
        ttk.Label(frame_entradas, text="Preço Inicial ($):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.preco_inicial = tk.DoubleVar(value=70)
        ttk.Entry(frame_entradas, textvariable=self.preco_inicial).grid(row=0, column=1, pady=5)

        # Preço de equilíbrio
        ttk.Label(frame_entradas, text="Preço de Equilíbrio ($):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.preco_equilibrio = tk.DoubleVar(value=80)
        ttk.Entry(frame_entradas, textvariable=self.preco_equilibrio).grid(row=1, column=1, pady=5)

        # Taxa de ajuste
        ttk.Label(frame_entradas, text="Taxa de Ajuste (α):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.taxa_ajuste = tk.DoubleVar(value=0.1)
        ttk.Entry(frame_entradas, textvariable=self.taxa_ajuste).grid(row=2, column=1, pady=5)

        # Taxa de impacto
        ttk.Label(frame_entradas, text="Taxa de Impacto (β):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.taxa_impacto = tk.DoubleVar(value=0.05)
        ttk.Entry(frame_entradas, textvariable=self.taxa_impacto).grid(row=3, column=1, pady=5)

        # Tempo de simulação
        ttk.Label(frame_entradas, text="Tempo (anos):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.tempo_max = tk.IntVar(value=50)
        ttk.Entry(frame_entradas, textvariable=self.tempo_max).grid(row=4, column=1, pady=5)

        # Fatores Adicionais de Demanda
        ttk.Label(frame_entradas, text="Crescimento Econômico (%):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.crescimento_economico = tk.DoubleVar(value=2.0)
        ttk.Entry(frame_entradas, textvariable=self.crescimento_economico).grid(row=5, column=1, pady=5)

        ttk.Label(frame_entradas, text="Avanços Tecnológicos (α):").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.avancos_tecnologicos = tk.DoubleVar(value=0.03)
        ttk.Entry(frame_entradas, textvariable=self.avancos_tecnologicos).grid(row=6, column=1, pady=5)

        # Eventos Geopolíticos
        ttk.Label(frame_entradas, text="Frequência de Eventos Geopolíticos:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.freq_geopolitica = tk.DoubleVar(value=0.1)
        ttk.Entry(frame_entradas, textvariable=self.freq_geopolitica).grid(row=7, column=1, pady=5)

        # Botões
        ttk.Button(frame_entradas, text="Calcular", command=self.calcular_modelo).grid(row=8, column=0, columnspan=2, pady=10)
        ttk.Button(frame_entradas, text="Exportar Resultados", command=self.exportar_resultados).grid(row=9, column=0, columnspan=2, pady=5)

        # Frame para gráficos
        frame_graficos = ttk.Frame(self.aba_modelo)
        frame_graficos.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Figura principal
        self.figura, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figura, master=frame_graficos)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Figura secundária para fatores
        self.figura2, self.ax2 = plt.subplots(figsize=(6, 2))
        self.canvas2 = FigureCanvasTkAgg(self.figura2, master=frame_graficos)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Autor
        self.ax.legend(["Modelo do Preço do Petróleo"], loc='upper right', fontsize='small', labelcolor="blue")
        self.figura.suptitle("Modelo Avançado do Preço do Petróleo por Luiz Tiago Wilcke", color="blue")

    def criar_widgets_explicacao(self):
        explicacao = """
        Modelo Avançado do Preço do Petróleo

        Este modelo calcula o preço do barril de petróleo ao longo do tempo utilizando uma equação diferencial que considera múltiplos fatores de demanda e oferta.

        Equação Diferencial:
        dP/dt = α * (P_equilíbrio - P) - β * P * (Fator_demanda1 + Fator_demanda2 + ... ) + γ * Eventos_geopolíticos

        Componentes Adicionais:
        - Crescimento Econômico (%):Representa o impacto do crescimento da economia global na demanda por petróleo.
        - Avanços Tecnológicos (α): Considera como inovações tecnológicas podem afetar a eficiência e, consequentemente, a demanda por petróleo.
        - Eventos Geopolíticos: Introduz eventos imprevisíveis que podem causar flutuações abruptas no preço do petróleo.

        Análise de Sensibilidade:
        Permite simular diferentes cenários variando os parâmetros para observar como eles afetam o preço do petróleo.

        Exportação de Resultados:
        Após a simulação, os resultados podem ser exportados para um arquivo CSV para análises futuras ou relatórios.

        Como Usar:
        1. Insira os valores desejados nos campos fornecidos.
        2. Clique em "Calcular" para gerar a projeção do preço ao longo do tempo.
        3. Utilize "Exportar Resultados" para salvar os dados da simulação.
        """
        texto_explicacao = tk.Text(self.aba_explicacao, wrap=tk.WORD, padx=10, pady=10)
        texto_explicacao.insert(tk.END, explicacao)
        texto_explicacao.config(state=tk.DISABLED)
        texto_explicacao.pack(fill=tk.BOTH, expand=True)

    def calcular_modelo(self):
        try:
            # Obter valores dos inputs
            P0 = self.preco_inicial.get()
            Pequil = self.preco_equilibrio.get()
            alpha = self.taxa_ajuste.get()
            beta = self.taxa_impacto.get()
            tempo = self.tempo_max.get()
            crescimento = self.crescimento_economico.get() / 100  # Convertendo para decimal
            tecnologia = self.avancos_tecnologicos.get()
            freq_geo = self.freq_geopolitica.get()

            # Validação
            if P0 <= 0 or Pequil <= 0 or alpha <= 0 or beta <= 0 or tempo <= 0:
                raise ValueError("Os valores devem ser positivos.")

            # Definir o tempo
            t = np.linspace(0, tempo, 1000)

            # Precomputar fatores de demanda
            Fator_demanda_economica = crescimento * np.exp(0.05 * t)  # Crescimento econômico exponencial
            Fator_demanda_tecnologica = tecnologia * np.cos(0.05 * t)  # Avanços tecnológicos cíclicos

            # Eventos geopolíticos como função aleatória
            eventos_geopoliticos = freq_geo * np.random.normal(0, 1, size=len(t))

            # Definir a equação diferencial com múltiplos fatores
            def dPdt(P, t_current):
                # Interpolar fatores
                F_d_econ = np.interp(t_current, t, Fator_demanda_economica)
                F_d_tecn = np.interp(t_current, t, Fator_demanda_tecnologica)
                F_d = F_d_econ + F_d_tecn
                evento = np.interp(t_current, t, eventos_geopoliticos)
                return alpha * (Pequil - P) - beta * P * F_d + evento

            # Resolver a equação diferencial
            P = odeint(dPdt, P0, t)
            P = P.flatten()

            # Limpar os gráficos anteriores
            self.ax.clear()
            self.ax2.clear()

            # Plotar os resultados
            self.ax.plot(t, P, label="Preço do Petróleo", color="green")
            self.ax.set_xlabel("Anos")
            self.ax.set_ylabel("Preço do Barril ($)")
            self.ax.set_title("Projeção do Preço do Petróleo")
            self.ax.legend(["Modelo Avançado do Preço do Petróleo"], loc='upper right', fontsize='small', labelcolor="blue")
            self.figura.suptitle("Modelo Avançado do Preço do Petróleo por Luiz Tiago Wilcke", color="blue")

            # Plotar os fatores de demanda
            self.ax2.plot(t, Fator_demanda_economica, label="Crescimento Econômico", color="blue")
            self.ax2.plot(t, Fator_demanda_tecnologica, label="Avanços Tecnológicos", color="orange")
            self.ax2.set_xlabel("Anos")
            self.ax2.set_ylabel("Fatores de Demanda")
            self.ax2.legend(loc='upper right', fontsize='small')
            self.ax2.set_title("Fatores de Demanda ao Longo do Tempo")

            self.canvas.draw()
            self.canvas2.draw()

            # Armazenar resultados para exportação
            self.resultados = zip(t, P, Fator_demanda_economica, Fator_demanda_tecnologica)

        except ValueError as ve:
            messagebox.showerror("Erro de Validação", f"Erro de validação: {ve}")
        except Exception as e:
            messagebox.showerror("Erro", f"Por favor, insira valores válidos.\nDetalhes: {e}")

    def exportar_resultados(self):
        try:
            # Verificar se os resultados foram gerados
            if not hasattr(self, 'resultados'):
                raise AttributeError("Nenhum resultado para exportar. Execute a simulação primeiro.")

            # Solicitar local para salvar o arquivo
            arquivo = filedialog.asksaveasfilename(defaultextension=".csv",
                                                  filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                                                  title="Salvar Resultados")
            if arquivo:
                with open(arquivo, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Tempo (anos)", "Preço do Petróleo ($)", "Crescimento Econômico (%)", "Avanços Tecnológicos (α)"])
                    for linha in self.resultados:
                        writer.writerow(linha)
                messagebox.showinfo("Sucesso", f"Resultados exportados com sucesso para {arquivo}")
        except AttributeError as ae:
            messagebox.showerror("Erro de Exportação", f"Erro: {ae}")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível exportar os resultados.\nDetalhes: {e}")

if __name__ == "__main__":
    raiz = tk.Tk()
    app = ModeloPetroleoApp(raiz)
    raiz.mainloop()
