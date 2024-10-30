import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Constantes Físicas com 8 dígitos de precisão
CONST = {
    'q': 1.60217663e-19,     # Carga do elétron (C)
    'k_B': 1.380649e-23,     # Constante de Boltzmann (J/K)
    'h': 6.62607015e-34,     # Constante de Planck (J·s)
    'epsilon_0': 8.85418782e-12,  # Permitividade do vácuo (F/m)
    'epsilon_r': 11.7,       # Permitividade relativa do silício
    'T': 300.0,               # Temperatura (K)
}

def fermi_dirac(E, E_f, T):
    """
    Calcula a distribuição de Fermi-Dirac.

    :param E: Energia (J)
    :param E_f: Energia de Fermi (J)
    :param T: Temperatura (K)
    :return: Probabilidade de ocupação
    """
    return 1 / (np.exp((E - E_f) / (CONST['k_B'] * T)) + 1)

# Função que define as equações diferenciais do modelo aprimorado com efeitos quânticos
def modelo_celula_quantico(t, y, parametros):
    n, p = y
    Dn = parametros['Dn']          # Difusividade dos elétrons (m²/s)
    Dp = parametros['Dp']          # Difusividade das lacunas (m²/s)
    mu_n = parametros['mu_n']      # Mobilidade dos elétrons (cm²/V·s)
    mu_p = parametros['mu_p']      # Mobilidade das lacunas (cm²/V·s)
    V = parametros['V']            # Tensão aplicada (V)
    N_d = parametros['N_d']        # Densidade de dopantes do tipo N (m⁻³)
    N_a = parametros['N_a']        # Densidade de dopantes do tipo P (m⁻³)
    G = parametros['G']            # Geração (pares/m³·s)
    B = parametros['B']            # Recombinação (m³/s)
    E_f_n = parametros['E_f_n']    # Energia de Fermi para elétrons (J)
    E_f_p = parametros['E_f_p']    # Energia de Fermi para lacunas (J)
    L = parametros['L']            # Espessura da barreira (m)
    T_q = parametros['T_q']        # Taxa de túnel (m³/s)
    lambda_q = parametros['lambda_q']  # Parâmetro de decaimento quântico (m)

    # Conversão de unidades se necessário
    mu_n_m2 = mu_n * 1e-4  # cm²/V·s para m²/V·s
    mu_p_m2 = mu_p * 1e-4

    # Campo elétrico (V/m) assumido constante para simplificação
    campo_eletrico = V / 1e-6  # Suposição de espessura da junção de 1 µm

    # Distribuição de Fermi-Dirac
    f_n = fermi_dirac(E_f_n, E_f_n, CONST['T'])
    f_p = fermi_dirac(E_f_p, E_f_p, CONST['T'])

    # Recombinação com efeito quântico
    recombinacao = B * n * p * f_n * f_p + T_q * np.exp(-L / lambda_q)

    # Equações de continuidade aprimoradas com efeitos quânticos
    dn_dt = Dn * (-n + N_d - p) + mu_n_m2 * campo_eletrico * n - recombinacao + G
    dp_dt = Dp * (-p + N_a - n) - mu_p_m2 * campo_eletrico * p - recombinacao + G

    return [dn_dt, dp_dt]

# Função para o modelo clássico
def modelo_celula(t, y, parametros):
    n, p = y
    Dn = parametros['Dn']          # Difusividade dos elétrons (m²/s)
    Dp = parametros['Dp']          # Difusividade das lacunas (m²/s)
    mu_n = parametros['mu_n']      # Mobilidade dos elétrons (cm²/V·s)
    mu_p = parametros['mu_p']      # Mobilidade das lacunas (cm²/V·s)
    V = parametros['V']            # Tensão aplicada (V)
    N_d = parametros['N_d']        # Densidade de dopantes do tipo N (m⁻³)
    N_a = parametros['N_a']        # Densidade de dopantes do tipo P (m⁻³)
    G = parametros['G']            # Geração (pares/m³·s)
    B = parametros['B']            # Recombinação (m³/s)

    # Conversão de unidades se necessário
    mu_n_m2 = mu_n * 1e-4  # cm²/V·s para m²/V·s
    mu_p_m2 = mu_p * 1e-4

    # Campo elétrico (V/m) assumido constante para simplificação
    campo_eletrico = V / 1e-6  # Suposição de espessura da junção de 1 µm

    # Recombinação bimolecular clássica
    recombinacao = B * n * p

    # Equações de continuidade clássicas
    dn_dt = Dn * (-n + N_d - p) + mu_n_m2 * campo_eletrico * n - recombinacao + G
    dp_dt = Dp * (-p + N_a - n) - mu_p_m2 * campo_eletrico * p - recombinacao + G

    return [dn_dt, dp_dt]

# Função para resolver as equações e plotar os resultados em uma nova janela
def resolver_e_plotar_quantico(tipo_modelo='classico'):
    try:
        # Obter parâmetros a partir das entradas
        Dn = float(entrada_Dn.get())       # m²/s
        Dp = float(entrada_Dp.get())       # m²/s
        mu_n = float(entrada_mu_n.get())   # cm²/V·s
        mu_p = float(entrada_mu_p.get())   # cm²/V·s
        V = float(entrada_V.get())         # V
        N_d = float(entrada_N_d.get())     # m⁻³
        N_a = float(entrada_N_a.get())     # m⁻³
        G = float(entrada_G.get())         # pares/m³·s
        B = float(entrada_B.get())         # m³/s

        if tipo_modelo == 'quantico':
            E_f_n = float(entrada_E_f_n.get())  # Energia de Fermi para elétrons (J)
            E_f_p = float(entrada_E_f_p.get())  # Energia de Fermi para lacunas (J)
            L = float(entrada_L.get())          # Espessura da barreira (m)
            T_q = float(entrada_T_q.get())      # Taxa de túnel (m³/s)
            lambda_q = float(entrada_lambda_q.get())  # Parâmetro de decaimento quântico (m)

            parametros = {
                'Dn': Dn,
                'Dp': Dp,
                'mu_n': mu_n,
                'mu_p': mu_p,
                'V': V,
                'N_d': N_d,
                'N_a': N_a,
                'G': G,
                'B': B,
                'E_f_n': E_f_n,
                'E_f_p': E_f_p,
                'L': L,
                'T_q': T_q,
                'lambda_q': lambda_q
            }
            modelo = modelo_celula_quantico
        else:
            parametros = {
                'Dn': Dn,
                'Dp': Dp,
                'mu_n': mu_n,
                'mu_p': mu_p,
                'V': V,
                'N_d': N_d,
                'N_a': N_a,
                'G': G,
                'B': B
            }
            modelo = modelo_celula

        # Condições iniciais
        y0 = [N_d, N_a]

        # Intervalo de tempo
        t_span = (0, 1e-6)  # Tempo em segundos
        t_eval = np.linspace(t_span[0], t_span[1], 1000)

        # Resolver as equações diferenciais
        solucao = solve_ivp(modelo, t_span, y0, args=(parametros,), t_eval=t_eval, rtol=1e-8, atol=1e-10)

        if solucao.success:
            # Criar uma nova janela para o gráfico
            janela_plot = tk.Toplevel(janela)
            janela_plot.title("Gráfico da Simulação")
            janela_plot.geometry("800x600")

            # Criar a figura para plotagem
            fig, ax = plt.subplots(figsize=(8,6))
            ax.plot(solucao.t, solucao.y[0], label='Elétrons (n)')
            ax.plot(solucao.t, solucao.y[1], label='Lacunas (p)')
            ax.set_xlabel('Tempo (s)')
            ax.set_ylabel('Concentração (m⁻³)')
            ax.set_title('Simulação de Célula Fotovoltaica com Efeitos Quânticos' if tipo_modelo == 'quantico' else 'Simulação de Célula Fotovoltaica Clássica')
            ax.legend()
            fig.tight_layout()

            # Incorporar o gráfico na nova janela
            canvas_plot = FigureCanvasTkAgg(fig, master=janela_plot)
            canvas_widget_plot = canvas_plot.get_tk_widget()
            canvas_widget_plot.pack(fill=tk.BOTH, expand=True)
            canvas_plot.draw()

            # Mostrar resultados numéricos com oito dígitos de precisão na janela principal
            resultado_texto.set(
                f"Concentração final de Elétrons (n): {solucao.y[0][-1]:.8e} m⁻³\n"
                f"Concentração final de Lacunas (p): {solucao.y[1][-1]:.8e} m⁻³"
            )
        else:
            messagebox.showerror("Erro", "A solução das equações diferenciais falhou.")
    except ValueError:
        messagebox.showerror("Erro de Entrada", "Por favor, insira valores numéricos válidos.")

# Criar a janela principal
janela = tk.Tk()
janela.title("Simulador de Célula Fotovoltaica Quântica")
janela.minsize(1000, 800)

# Criar o Notebook (abas)
notebook = ttk.Notebook(janela)
notebook.pack(fill=tk.BOTH, expand=True)

# Criar os frames para cada aba
frame_simulacao = ttk.Frame(notebook, padding="10")
frame_explicacao = ttk.Frame(notebook, padding="10")

notebook.add(frame_simulacao, text='Simulação')
notebook.add(frame_explicacao, text='Explicação')

# --- Aba de Simulação ---

# Lista de parâmetros e suas labels
parametros = [
    ('Dn (Difusividade dos elétrons, m²/s)', 'Dn'),
    ('Dp (Difusividade das lacunas, m²/s)', 'Dp'),
    ('µn (Mobilidade dos elétrons, cm²/V·s)', 'mu_n'),
    ('µp (Mobilidade das lacunas, cm²/V·s)', 'mu_p'),
    ('V (Tensão aplicada, V)', 'V'),
    ('N_d (Densidade de dopantes N, m⁻³)', 'N_d'),
    ('N_a (Densidade de dopantes P, m⁻³)', 'N_a'),
    ('G (Geração, pares/m³·s)', 'G'),
    ('B (Recombinação, m³/s)', 'B')
]

# Adicionar entradas para parâmetros quânticos
parametros_quanticos = [
    ('E_f_n (Energia de Fermi para elétrons, J)', 'E_f_n'),
    ('E_f_p (Energia de Fermi para lacunas, J)', 'E_f_p'),
    ('L (Espessura da barreira, m)', 'L'),
    ('T_q (Taxa de túnel, m³/s)', 'T_q'),
    ('λ_q (Parâmetro de decaimento quântico, m)', 'lambda_q')
]

# Dicionário para armazenar as entradas
entradas = {}
for idx, (label_text, var_name) in enumerate(parametros):
    label = ttk.Label(frame_simulacao, text=label_text + ":")
    label.grid(row=idx, column=0, sticky=tk.W, pady=2, padx=5)
    entrada = ttk.Entry(frame_simulacao, width=25)
    entrada.grid(row=idx, column=1, pady=2, padx=5)
    entradas[var_name] = entrada

# Atribuir entradas às variáveis
entrada_Dn = entradas['Dn']
entrada_Dp = entradas['Dp']
entrada_mu_n = entradas['mu_n']
entrada_mu_p = entradas['mu_p']
entrada_V = entradas['V']
entrada_N_d = entradas['N_d']
entrada_N_a = entradas['N_a']
entrada_G = entradas['G']
entrada_B = entradas['B']

# Valores padrão (opcional, podem ser ajustados conforme necessário)
entrada_Dn.insert(0, "1.45e-3")        # Exemplo para silício
entrada_Dp.insert(0, "4.25e-3")
entrada_mu_n.insert(0, "1400")
entrada_mu_p.insert(0, "450")
entrada_V.insert(0, "0.7")
entrada_N_d.insert(0, "1e21")
entrada_N_a.insert(0, "1e21")
entrada_G.insert(0, "1e23")
entrada_B.insert(0, "1e-16")

# Adicionar campos para parâmetros quânticos
for idx, (label_text, var_name) in enumerate(parametros_quanticos, start=len(parametros)):
    label = ttk.Label(frame_simulacao, text=label_text + ":")
    label.grid(row=idx, column=0, sticky=tk.W, pady=2, padx=5)
    entrada = ttk.Entry(frame_simulacao, width=25)
    entrada.grid(row=idx, column=1, pady=2, padx=5)
    entradas[var_name] = entrada

# Atribuir entradas às variáveis quânticas
entrada_E_f_n = entradas['E_f_n']
entrada_E_f_p = entradas['E_f_p']
entrada_L = entradas['L']
entrada_T_q = entradas['T_q']
entrada_lambda_q = entradas['lambda_q']

# Valores padrão para parâmetros quânticos
entrada_E_f_n.insert(0, "5.0e-19")  # Exemplo
entrada_E_f_p.insert(0, "5.0e-19")  # Exemplo
entrada_L.insert(0, "1e-9")         # 1 nm
entrada_T_q.insert(0, "1e-16")      # Exemplo
entrada_lambda_q.insert(0, "1e-9")  # 1 nm

# Adicionar um botão ou opção para selecionar o tipo de modelo
def selecionar_modelo():
    tipo = modelo_var.get()
    if tipo == 'quantico':
        # Habilitar entradas quânticas
        for _, var_name in parametros_quanticos:
            entradas[var_name].configure(state='normal')
    else:
        # Desabilitar entradas quânticas
        for _, var_name in parametros_quanticos:
            entradas[var_name].configure(state='disabled')

modelo_var = tk.StringVar(value='classico')
radio_classico = ttk.Radiobutton(frame_simulacao, text='Modelo Clássico', variable=modelo_var, value='classico', command=selecionar_modelo)
radio_quantico = ttk.Radiobutton(frame_simulacao, text='Modelo Quântico', variable=modelo_var, value='quantico', command=selecionar_modelo)
radio_classico.grid(row=len(parametros) + len(parametros_quanticos), column=0, pady=5, sticky=tk.W, padx=5)
radio_quantico.grid(row=len(parametros) + len(parametros_quanticos)+1, column=0, pady=5, sticky=tk.W, padx=5)

# Inicialmente desabilitar entradas quânticas
for _, var_name in parametros_quanticos:
    entradas[var_name].configure(state='disabled')

# Label para mostrar resultados numéricos
resultado_texto = tk.StringVar()
label_resultado = ttk.Label(frame_simulacao, textvariable=resultado_texto, justify=tk.LEFT, padding="10")
label_resultado.grid(row=len(parametros) + len(parametros_quanticos)+2, column=0, columnspan=2, pady=10, sticky=tk.W)

# Adicionar a legenda do autor
label_autor = ttk.Label(frame_simulacao, text="Autor: Luiz Tiago Wilcke", foreground="blue")
label_autor.grid(row=len(parametros) + len(parametros_quanticos)+3, column=0, columnspan=2, pady=10)

# Botão para resolver e plotar
botao_resolver = ttk.Button(frame_simulacao, text="Resolver e Plotar", command=lambda: resolver_e_plotar_quantico(tipo_modelo=modelo_var.get()))
botao_resolver.grid(row=len(parametros) + len(parametros_quanticos)+4, column=0, columnspan=2, pady=10)

# --- Aba de Explicação ---

texto_explicacao = (
    "Este simulador de Célula Fotovoltaica Quântica permite a modelagem e análise do comportamento de células fotovoltaicas considerando tanto modelos clássicos quanto quânticos.\n\n"
    "Parâmetros de Entrada:\n"
    "Dn: Difusividade dos elétrons (m²/s)\n"
    "Dp: Difusividade das lacunas (m²/s)\n"
    "µn: Mobilidade dos elétrons (cm²/V·s)\n"
    "µp: Mobilidade das lacunas (cm²/V·s)\n"
    "V: Tensão aplicada (V)\n"
    "N_d: Densidade de dopantes do tipo N (m⁻³)\n"
    "N_a: Densidade de dopantes do tipo P (m⁻³)\n"
    "G: Taxa de geração de pares elétron-lacuna (pares/m³·s)\n"
    "B: Taxa de recombinação bimolecular (m³/s)\n\n"
    "Parâmetros Quânticos (disponíveis somente no Modelo Quântico):\n"
    "E_f_n: Energia de Fermi para elétrons (J)\n"
    "E_f_p: Energia de Fermi para lacunas (J)\n"
    "L: Espessura da barreira de túnel (m)\n"
    "T_q: Taxa de túnel quântico (m³/s)\n"
    "λ_q: Parâmetro de decaimento quântico (m)\n\n"
    "Como Usar:\n"
    "1. Insira os valores desejados para os parâmetros de entrada. Valores padrão estão fornecidos para referência.\n"
    "2. Selecione o tipo de modelo a ser utilizado: 'Modelo Clássico' ou 'Modelo Quântico'.\n"
    "   - No Modelo Clássico, apenas os parâmetros básicos são utilizados.\n"
    "   - No Modelo Quântico, os parâmetros adicionais relacionados aos efeitos quânticos são considerados.\n"
    "3. Clique no botão 'Resolver e Plotar' para executar a simulação.\n"
    "4. Após a resolução das equações diferenciais, uma nova janela será aberta exibindo o gráfico das concentrações de elétrons e lacunas ao longo do tempo.\n"
    "5. Os resultados numéricos finais das concentrações também serão exibidos na aba de Simulação.\n\n"
    "Interpretação dos Resultados:\n"
    "O gráfico mostra a evolução das concentrações de elétrons (n) e lacunas (p) ao longo do tempo. No Modelo Quântico, efeitos como recombinação via túnel quântico são considerados, o que pode alterar o comportamento das concentrações em comparação ao Modelo Clássico.\n\n"
    "Considerações sobre a Incorporação da Equação de Schrödinger:\n"
    "Embora a equação de Schrödinger seja fundamental para descrever o comportamento quântico de partículas, sua aplicação direta em modelos de simulação de dispositivos semicondutores como células fotovoltaicas é complexa e computacionalmente intensiva. Em vez disso, efeitos quânticos específicos podem ser incorporados através de aproximações ou correções ao modelo clássico, como a densidade de estados modificada ou termos de recombinação quântica. Para simulações que requerem uma descrição detalhada do comportamento quântico, métodos avançados ou softwares especializados são recomendados."
)

# Adicionar um widget de texto com rolagem para a explicação
scrollbar = ttk.Scrollbar(frame_explicacao, orient=tk.VERTICAL)
texto = tk.Text(frame_explicacao, wrap=tk.WORD, yscrollcommand=scrollbar.set, padx=10, pady=10)
scrollbar.config(command=texto.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

texto.insert(tk.END, texto_explicacao)
texto.configure(state='disabled')  # Tornar o texto somente leitura

# Iniciar o loop principal da interface
janela.mainloop()