import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Raio do universo observável em anos-luz
RAIO_UNIVERSO_ANOS_LUZ = 46e9  # 46 bilhões de anos-luz

# Função para calcular o número de planetas com vida e a distância
def calcular_planetas_com_vida():
    try:
        # Obter valores das entradas
        tempo = float(entrada_tempo.get())
        taxa_formacao_estrelas = float(entrada_taxa_formacao.get())
        fracao_sistemas_planetarios = float(entrada_fracao_sistemas.get())
        planetas_por_sistema = float(entrada_planetas_sistema.get())
        fracao_planetas_hab = float(entrada_fracao_planetas_hab.get())
        fracao_civilizacoes = float(entrada_fracao_civilizacoes.get())

        # Validação das entradas
        if tempo <= 0:
            raise ValueError("O tempo deve ser maior que zero.")
        if not (0 <= fracao_sistemas_planetarios <= 1):
            raise ValueError("A fração de sistemas planetários (β) deve estar entre 0 e 1.")
        if not (0 <= fracao_planetas_hab <= 1):
            raise ValueError("A fração de planetas habitáveis (δ) deve estar entre 0 e 1.")
        if not (0 <= fracao_civilizacoes <= 1):
            raise ValueError("A fração de civilizações (ε) deve estar entre 0 e 1.")

        # Parâmetros do modelo
        alpha = taxa_formacao_estrelas  # Taxa de formação de estrelas
        beta = fracao_sistemas_planetarios  # Fração de estrelas com sistemas planetários
        gamma = planetas_por_sistema  # Número médio de planetas habitáveis por sistema
        delta = fracao_planetas_hab  # Fração de planetas habitáveis que desenvolvem vida
        epsilon = fracao_civilizacoes  # Fração de planetas com vida que desenvolvem civilizações

        # Número de planetas com vida ao longo do tempo
        tempo_array = np.linspace(0, tempo, 100)
        N = alpha * beta * gamma * delta * epsilon * tempo_array

        # Resultado final
        resultado = N[-1]
        label_resultado.config(text=f"Número estimado de planetas com vida: {resultado:.2e}")

        # Cálculo da Distância Média
        distancia_media = (3/4) * RAIO_UNIVERSO_ANOS_LUZ  # Média de uma distribuição f(r) = 3r^2 / R^3
        label_distancia.config(text=f"Distância média dos planetas com vida: {distancia_media:.2e} anos-luz")

        # Plotagem do Número de Planetas com Vida ao Longo do Tempo
        fig.clear()
        ax1 = fig.add_subplot(211)
        ax1.plot(tempo_array, N, label='Planetas com Vida', color='blue')
        ax1.set_xlabel('Tempo (anos)')
        ax1.set_ylabel('Número de Planetas com Vida')
        ax1.set_title('Evolução dos Planetas com Vida ao Longo do Tempo')
        ax1.legend()

        # Plotagem da Distribuição de Probabilidade das Distâncias
        if resultado > 0:
            # Limitar o número de planetas para evitar sobrecarga
            numero_planetas = min(int(resultado), 1000000)  # Limite de 1 milhão
            # Gerar uma amostra de distâncias baseada na distribuição f(r) = 3r^2 / R^3
            # Utilizando a transformação inversa
            u = np.random.uniform(0, 1, numero_planetas)
            r = RAIO_UNIVERSO_ANOS_LUZ * u**(1/3)

            ax2 = fig.add_subplot(212)
            ax2.hist(r, bins=50, density=True, color='green', alpha=0.7)
            ax2.set_xlabel('Distância (anos-luz)')
            ax2.set_ylabel('Densidade de Probabilidade')
            ax2.set_title('Distribuição de Probabilidade das Distâncias dos Planetas com Vida')
        else:
            ax2 = fig.add_subplot(212)
            ax2.text(0.5, 0.5, 'Nenhum planeta com vida estimado.', horizontalalignment='center', verticalalignment='center')
            ax2.set_axis_off()

        fig.tight_layout()
        canvas.draw()

    except ValueError as ve:
        messagebox.showerror("Entrada Inválida", f"Erro: {ve}")

# Função para exibir as fórmulas do modelo
def exibir_formulas():
    formula_texto = (
        "Modelo de Estimativa de Planetas com Vida\n\n"
        "Equações Diferenciais Utilizadas:\n"
        "dN/dt = α * β * γ * δ * ε\n\n"
        "Onde:\n"
        "N = Número de planetas com vida\n"
        "α = Taxa de formação de estrelas (estrelas por ano)\n"
        "β = Fração de estrelas com sistemas planetários\n"
        "γ = Número médio de planetas habitáveis por sistema planetário\n"
        "δ = Fração de planetas habitáveis que desenvolvem vida\n"
        "ε = Fração de planetas com vida que desenvolvem civilizações\n\n"
        "Solução do modelo:\n"
        "N(t) = α * β * γ * δ * ε * t\n\n"
        "Distribuição de Probabilidade das Distâncias:\n"
        "f(r) = \\frac{3r^2}{R^3}\n\n"
        "Onde:\n"
        "r = Distância do planeta com vida\n"
        "R = Raio do universo observável (≈ 46 bilhões de anos-luz)\n\n"
        "A distância média é dada por:\n"
        "\\bar{r} = \\frac{3}{4} R\n\n"
        "Este modelo considera que os planetas com vida estão distribuídos uniformemente no universo observável."
    )
    messagebox.showinfo("Fórmulas do Modelo", formula_texto)

# Criar a janela principal
janela = tk.Tk()
janela.title("Estimativa de Planetas com Vida no Universo")
janela.geometry("900x700")

# Adicionar legenda azul no topo
header = tk.Label(janela, text="Autor: Luiz Tiago Wilcke", fg="blue", font=("Helvetica", 12, "bold"))
header.pack(side='top', pady=10)

# Criar abas
abas = ttk.Notebook(janela)
aba_calculadora = ttk.Frame(abas)
aba_formulas = ttk.Frame(abas)
abas.add(aba_calculadora, text='Calculadora')
abas.add(aba_formulas, text='Fórmulas')
abas.pack(expand=1, fill='both')

# Conteúdo da aba Calculadora
frame = ttk.Frame(aba_calculadora, padding=10)
frame.grid(row=0, column=0, sticky='nsew')

# Configurar o grid do frame
aba_calculadora.rowconfigure(0, weight=1)
aba_calculadora.columnconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=3)

# Entradas de dados com valores padrão
ttk.Label(frame, text="Tempo (anos):").grid(row=0, column=0, sticky='W', pady=5, padx=5)
entrada_tempo = ttk.Entry(frame)
entrada_tempo.grid(row=0, column=1, pady=5, padx=5)
entrada_tempo.insert(0, "1e9")  # 1 bilhão de anos

ttk.Label(frame, text="Taxa de Formação de Estrelas (α):").grid(row=1, column=0, sticky='W', pady=5, padx=5)
entrada_taxa_formacao = ttk.Entry(frame)
entrada_taxa_formacao.grid(row=1, column=1, pady=5, padx=5)
entrada_taxa_formacao.insert(0, "1e11")  # Exemplo: 100 bilhões de estrelas formadas por ano

ttk.Label(frame, text="Fração de Sistemas Planetários (β):").grid(row=2, column=0, sticky='W', pady=5, padx=5)
entrada_fracao_sistemas = ttk.Entry(frame)
entrada_fracao_sistemas.grid(row=2, column=1, pady=5, padx=5)
entrada_fracao_sistemas.insert(0, "0.5")  # 50%

ttk.Label(frame, text="Planetas Habitáveis por Sistema (γ):").grid(row=3, column=0, sticky='W', pady=5, padx=5)
entrada_planetas_sistema = ttk.Entry(frame)
entrada_planetas_sistema.grid(row=3, column=1, pady=5, padx=5)
entrada_planetas_sistema.insert(0, "2")  # 2 planetas habitáveis por sistema

ttk.Label(frame, text="Fração de Planetas Habitáveis que Desenvolvem Vida (δ):").grid(row=4, column=0, sticky='W', pady=5, padx=5)
entrada_fracao_planetas_hab = ttk.Entry(frame)
entrada_fracao_planetas_hab.grid(row=4, column=1, pady=5, padx=5)
entrada_fracao_planetas_hab.insert(0, "0.1")  # 10%

ttk.Label(frame, text="Fração de Civilizações (ε):").grid(row=5, column=0, sticky='W', pady=5, padx=5)
entrada_fracao_civilizacoes = ttk.Entry(frame)
entrada_fracao_civilizacoes.grid(row=5, column=1, pady=5, padx=5)
entrada_fracao_civilizacoes.insert(0, "0.01")  # 1%

# Botão de calcular
botao_calcular = ttk.Button(frame, text="Calcular", command=calcular_planetas_com_vida)
botao_calcular.grid(row=6, column=0, columnspan=2, pady=10)

# Resultados
label_resultado = ttk.Label(frame, text="Número estimado de planetas com vida: ")
label_resultado.grid(row=7, column=0, columnspan=2, pady=5, padx=5)

label_distancia = ttk.Label(frame, text="Distância média dos planetas com vida: ")
label_distancia.grid(row=8, column=0, columnspan=2, pady=5, padx=5)

# Plotagem
fig = plt.Figure(figsize=(8,6), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.draw()
canvas.get_tk_widget().grid(row=9, column=0, columnspan=2, pady=10, padx=5)

# Ajuste das linhas para expandir
frame.rowconfigure(9, weight=1)

# Conteúdo da aba Fórmulas
frame_formulas = ttk.Frame(aba_formulas, padding=10)
frame_formulas.pack(fill='both', expand=True)

texto_formulas = (
    "Modelo de Estimativa de Planetas com Vida\n\n"
    "Equações Diferenciais Utilizadas:\n"
    "dN/dt = α * β * γ * δ * ε\n\n"
    "Onde:\n"
    "N = Número de planetas com vida\n"
    "α = Taxa de formação de estrelas (estrelas por ano)\n"
    "β = Fração de estrelas com sistemas planetários\n"
    "γ = Número médio de planetas habitáveis por sistema planetário\n"
    "δ = Fração de planetas habitáveis que desenvolvem vida\n"
    "ε = Fração de planetas com vida que desenvolvem civilizações\n\n"
    "Solução do modelo:\n"
    "N(t) = α * β * γ * δ * ε * t\n\n"
    "Distribuição de Probabilidade das Distâncias:\n"
    "f(r) = \\frac{3r^2}{R^3}\n\n"
    "Onde:\n"
    "r = Distância do planeta com vida\n"
    "R = Raio do universo observável (≈ 46 bilhões de anos-luz)\n\n"
    "A distância média é dada por:\n"
    "\\bar{r} = \\frac{3}{4} R\n\n"
    "Este modelo considera que os planetas com vida estão distribuídos uniformemente no universo observável."
)

label_formulas = tk.Label(frame_formulas, text=texto_formulas, justify='left', wraplength=850)
label_formulas.pack()

# Rodapé com autor em azul (opcional, já adicionamos no topo)
# rodape = tk.Label(janela, text="Autor: Luiz Tiago Wilcke", fg="blue", font=("Helvetica", 10, "italic"), anchor='center')
# rodape.pack(side='bottom', pady=10)

# Iniciar o loop da interface
janela.mainloop()
