import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Função para calcular a taxa de crescimento ao longo do tempo
def taxa_crescimento(t, taxa_inicial):
    # Taxa de crescimento que diminui exponencialmente ao longo do tempo
    return taxa_inicial * math.exp(-0.001 * t)

# Função para modelar a população humana usando equações diferenciais
def modelar_populacao(tempo_maximo, passo_tempo, taxa_crescimento_inicial, probabilidade_extincao, populacao_inicial):
    tempos = np.arange(0, tempo_maximo, passo_tempo)
    populacoes = []
    P = populacao_inicial
    populacoes.append(P)
    for t in tempos[1:]:
        r = taxa_crescimento(t, taxa_crescimento_inicial)
        # Mudança na população: crescimento menos extinção
        # Usando distribuição Gaussiana para modelar variações na probabilidade de extinção
        delta_P = r * P * passo_tempo - (probabilidade_extincao * math.exp(-((t - tempo_maximo/2)**2)/(2*(tempo_maximo/10)**2))) * P * passo_tempo
        P += delta_P
        # Garantir que a população não seja negativa
        P = max(P, 0)
        populacoes.append(P)
        # Se a população chegar a zero, interromper
        if P == 0:
            break
    return tempos[:len(populacoes)], populacoes

# Função para calcular a probabilidade de extinção até um certo tempo usando distribuição Gaussiana
def calcular_probabilidade_extincao(tempo_maximo, probabilidade_extincao):
    # Distribuição Gaussiana para modelar a probabilidade acumulada de extinção
    mu = tempo_maximo / 2
    sigma = tempo_maximo / 10
    prob_acumulada = 0.5 * (1 + math.erf((tempo_maximo - mu) / (sigma * math.sqrt(2))))
    return prob_acumulada

# Função para plotar o gráfico usando Matplotlib integrado ao Tkinter
def plotar_grafico(tempos, populacoes, canvas_frame):
    # Limpar o frame anterior
    for widget in canvas_frame.winfo_children():
        widget.destroy()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(tempos, populacoes, color='blue', label='População Humana')
    ax.set_xlabel('Tempo (anos)')
    ax.set_ylabel('População')
    ax.set_title('Evolução da População Humana ao Longo do Tempo')
    ax.legend()
    ax.grid(True)
    
    # Renderizar a fórmula de probabilidade usando o texto do Matplotlib
    formula = r'$P(E) = \frac{1}{2} \left[1 + \text{erf}\left(\frac{t - \mu}{\sigma \sqrt{2}}\right)\right]$'
    ax.text(0.95, 0.95, formula, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', horizontalalignment='right', color='green')
    
    # Integrar o gráfico ao Tkinter
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# Função para exibir explicações baseadas nos resultados
def exibir_explicacao(tempos, populacoes, probabilidade_extincao, tempo_maximo_val, canvas_explicacao, taxa_crescimento_inicial_val, populacao_inicial_val):
    # Limpar o frame anterior
    for widget in canvas_explicacao.winfo_children():
        widget.destroy()
    
    if populacoes[-1] == 0:
        tempo_extincao = tempos[-1]
        texto = f"""
**Resultado:**

A população humana atingiu zero após **{tempo_extincao} anos**.

**Parâmetros Utilizados:**
- **Taxa de Crescimento Inicial:** {taxa_crescimento_inicial_val}% ao ano
- **Probabilidade Anual de Extinção:** {probabilidade_extincao}
- **População Inicial:** {populacao_inicial_val} habitantes

**Explicação:**

O modelo utilizado considera uma taxa de crescimento populacional que diminui exponencialmente ao longo do tempo, refletindo fatores como recursos limitados e mudanças ambientais. Além disso, a probabilidade de extinção foi modelada usando uma distribuição Gaussiana, que permite variações naturais e eventos aleatórios que podem acelerar ou retardar a extinção.

Neste cenário, a combinação desses fatores levou a uma extinção completa da população humana em **{tempo_extincao} anos**. Este resultado ilustra a fragilidade da continuidade da espécie diante de riscos persistentes e variáveis.

**Considerações Finais:**

É importante notar que este modelo é uma simplificação e serve para ilustrar o argumento do Doomsday. Fatores reais que influenciam a população humana são extremamente complexos e incluem avanços tecnológicos, mudanças ambientais, políticas sociais, entre outros.
"""
    else:
        tempo_extincao = "mais do que o tempo máximo definido."
        texto = f"""
**Resultado:**

A população humana **não** atingiu zero dentro do tempo máximo de **{tempo_maximo_val} anos**.

**Parâmetros Utilizados:**
- **Taxa de Crescimento Inicial:** {taxa_crescimento_inicial_val}% ao ano
- **Probabilidade Anual de Extinção:** {probabilidade_extincao}
- **População Inicial:** {populacao_inicial_val} habitantes

**Explicação:**

O modelo utilizado considera uma taxa de crescimento populacional que diminui exponencialmente ao longo do tempo, refletindo fatores como recursos limitados e mudanças ambientais. A probabilidade de extinção foi modelada usando uma distribuição Gaussiana, permitindo variações naturais e eventos aleatórios que podem afetar a continuidade da espécie.

Neste cenário, a população humana **não** chegou ao fim dentro do período de **{tempo_maximo_val} anos**. Isso sugere que, sob as condições modeladas, a humanidade pode persistir além do horizonte temporal considerado, possivelmente devido a fatores estabilizadores da população ou a baixa probabilidade de eventos de extinção catastróficos durante o período analisado.

**Considerações Finais:**

É importante notar que este modelo é uma simplificação e serve para ilustrar o argumento do Doomsday. Fatores reais que influenciam a população humana são extremamente complexos e incluem avanços tecnológicos, mudanças ambientais, políticas sociais, entre outros.
"""
    
    # Configurar o texto com formatação Markdown-like
    label_explicacao = tk.Label(canvas_explicacao, text=texto, font=("Arial", 12), justify="left", wraplength=800, fg="black")
    label_explicacao.pack(padx=10, pady=10)

# Função principal para processar os dados e atualizar a interface
def calcular_modelo():
    try:
        # Obter valores das entradas
        tm = float(tempo_maximo.get())
        pt = float(passo_tempo.get())
        tc_inicial = float(taxa_crescimento_inicial.get()) / 100  # Converter porcentagem para decimal
        pe = float(probabilidade_extincao.get())
        pi = float(populacao_inicial.get())
        
        # Validação dos inputs
        if tm <= 0 or pt <= 0 or tc_inicial < 0 or pe < 0 or pi <= 0:
            messagebox.showerror("Erro de Entrada", "Por favor, insira valores positivos e válidos.")
            return
        
        # Modelar a população
        tempos, populacoes = modelar_populacao(tm, pt, tc_inicial, pe, pi)
        
        # Calcular a probabilidade de extinção
        prob_acumulada = calcular_probabilidade_extincao(tm, pe)
        
        # Plotar o gráfico com a fórmula
        plotar_grafico(tempos, populacoes, canvas_grafico)
        
        # Exibir explicação
        exibir_explicacao(
            tempos, 
            populacoes, 
            pe, 
            tm, 
            canvas_explicacao, 
            taxa_crescimento_inicial.get(), 
            populacao_inicial.get()
        )
        
    except ValueError:
        messagebox.showerror("Erro de Entrada", "Por favor, insira valores numéricos válidos.")

# Criar a janela principal
janela = tk.Tk()
janela.title("Calculadora do Argumento Doomsday")
janela.state('zoomed')  # Maximizar a janela
# janela.geometry("1200x800")  # Removido para que 'zoomed' funcione corretamente
janela.resizable(True, True)  # Permitir redimensionamento

# Criar frames para organizar a interface
frame_inputs = ttk.LabelFrame(janela, text="Parâmetros do Modelo", padding=(20, 10))
frame_inputs.pack(fill="x", padx=20, pady=10)

frame_botao = ttk.Frame(janela)
frame_botao.pack(pady=10)

frame_grafico = ttk.LabelFrame(janela, text="Gráfico da População", padding=(10, 10))
frame_grafico.pack(fill="both", expand=True, padx=20, pady=10)

frame_explicacao = ttk.LabelFrame(janela, text="Explicação dos Resultados", padding=(10, 10))
frame_explicacao.pack(fill="both", expand=True, padx=20, pady=10)

# Adicionar campos de entrada
ttk.Label(frame_inputs, text="Tempo Máximo (anos):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
tempo_maximo = tk.StringVar(value="1000")
ttk.Entry(frame_inputs, textvariable=tempo_maximo).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_inputs, text="Passo de Tempo (anos):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
passo_tempo = tk.StringVar(value="1")
ttk.Entry(frame_inputs, textvariable=passo_tempo).grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_inputs, text="Taxa de Crescimento Inicial (% ao ano):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
taxa_crescimento_inicial = tk.StringVar(value="1")  # 1% ao ano
ttk.Entry(frame_inputs, textvariable=taxa_crescimento_inicial).grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame_inputs, text="Probabilidade Anual de Extinção:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
probabilidade_extincao = tk.StringVar(value="0.0001")
ttk.Entry(frame_inputs, textvariable=probabilidade_extincao).grid(row=3, column=1, padx=5, pady=5)

ttk.Label(frame_inputs, text="População Inicial:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
populacao_inicial = tk.StringVar(value="8000000000")  # 8 bilhões
ttk.Entry(frame_inputs, textvariable=populacao_inicial).grid(row=4, column=1, padx=5, pady=5)

# Botão para calcular
ttk.Button(frame_botao, text="Calcular", command=calcular_modelo).pack()

# Canvas para o gráfico
canvas_grafico = ttk.Frame(frame_grafico)
canvas_grafico.pack(fill="both", expand=True)

# Canvas para a explicação
canvas_explicacao = ttk.Frame(frame_explicacao)
canvas_explicacao.pack(fill="both", expand=True)

# Adicionar autoria
label_autor = tk.Label(janela, text="Autor: Luiz Tiago Wilcke", fg="blue", font=("Arial", 10))
label_autor.pack(pady=5, anchor='e', padx=20)

# Iniciar a interface
janela.mainloop()
