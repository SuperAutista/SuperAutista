import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Função para criar o potencial
def cria_potencial(L, n_pontos, valor_potencial):
    x = np.linspace(0, L, n_pontos)
    V = np.zeros_like(x)
    V[int(0.4 * n_pontos):int(0.6 * n_pontos)] = valor_potencial  # Poço de potencial para simular junção p-n
    return x, V

# Função para resolver a Equação de Schrödinger usando diferenças finitas
def resolve_schrodinger(V, h_barra, massa_efetiva, L, n_pontos):
    dx = L / n_pontos
    diagonal = np.full(n_pontos, 2 / dx**2)
    fora_diagonal = np.full(n_pontos - 1, -1 / dx**2)
    H = np.diag(diagonal) + np.diag(fora_diagonal, -1) + np.diag(fora_diagonal, 1)
    H += np.diag(V / (h_barra**2 / (2 * massa_efetiva)))
    valores, vetores = eigh(H)
    return valores, vetores

# Função para calcular e exibir os resultados
def calcular():
    try:
        # Obtém os valores das variáveis a partir das entradas do usuário
        h_barra = float(entrada_h_barra.get())
        massa_efetiva = float(entrada_massa_efetiva.get())
        L = float(entrada_L.get())
        n_pontos = int(entrada_n_pontos.get())
        valor_potencial = float(entrada_valor_potencial.get())

        # Gerar potencial e resolver a equação
        x, V = cria_potencial(L, n_pontos, valor_potencial)
        valores, vetores = resolve_schrodinger(V, h_barra, massa_efetiva, L, n_pontos)

        # Seleciona o primeiro estado (mais baixo em energia) para exibir
        psi = vetores[:, 0]
        energia = valores[0]

        # Atualiza os gráficos
        ax1.clear()
        ax1.plot(x * 1e9, V, label='Potencial (J)')
        ax1.plot(x * 1e9, psi**2, label=f'|ψ|² para E={energia:.2e} J')
        ax1.legend(loc='upper right')
        ax1.set_xlabel("Posição (nm)")
        ax1.set_ylabel("Energia (J)")
        ax1.set_title("Modelo da Equação de Schrödinger para Célula Solar", color="blue")
        canvas.draw()

        # Exibe a energia calculada
        messagebox.showinfo("Resultado", f"A energia do estado fundamental é: {energia:.2e} J")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Configuração da interface gráfica
janela = tk.Tk()
janela.title("Calculadora da Equação de Schrödinger para Células Solares")
janela.geometry("800x800")

# Legenda superior
lbl_legenda_superior = tk.Label(janela, text="Autor: Luiz Tiago Wilcke", fg="blue", font=("Arial", 12, "italic"))
lbl_legenda_superior.pack(pady=5)

# Área para entrada de valores
frame_entrada = tk.Frame(janela)
frame_entrada.pack(pady=10)

# Campo para entrada de h_barra
tk.Label(frame_entrada, text="Constante de Planck reduzida (h_barra) em J.s:").grid(row=0, column=0, sticky="e")
entrada_h_barra = tk.Entry(frame_entrada)
entrada_h_barra.grid(row=0, column=1)
entrada_h_barra.insert(0, "1.0545718e-34")

# Campo para entrada da massa efetiva
tk.Label(frame_entrada, text="Massa do elétron (massa_efetiva) em kg:").grid(row=1, column=0, sticky="e")
entrada_massa_efetiva = tk.Entry(frame_entrada)
entrada_massa_efetiva.grid(row=1, column=1)
entrada_massa_efetiva.insert(0, "9.10938356e-31")

# Campo para entrada de L
tk.Label(frame_entrada, text="Largura do poço (L) em metros:").grid(row=2, column=0, sticky="e")
entrada_L = tk.Entry(frame_entrada)
entrada_L.grid(row=2, column=1)
entrada_L.insert(0, "1e-9")

# Campo para entrada do número de pontos
tk.Label(frame_entrada, text="Número de pontos (n_pontos):").grid(row=3, column=0, sticky="e")
entrada_n_pontos = tk.Entry(frame_entrada)
entrada_n_pontos.grid(row=3, column=1)
entrada_n_pontos.insert(0, "1000")

# Campo para o valor do potencial
tk.Label(frame_entrada, text="Valor do potencial no poço (valor_potencial) em J:").grid(row=4, column=0, sticky="e")
entrada_valor_potencial = tk.Entry(frame_entrada)
entrada_valor_potencial.grid(row=4, column=1)
entrada_valor_potencial.insert(0, "1e-18")

# Botão para calcular
btn_calcular = tk.Button(janela, text="Calcular", command=calcular, font=("Arial", 12, "bold"))
btn_calcular.pack(pady=10)

# Área de plotagem
fig, ax1 = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=janela)
canvas.get_tk_widget().pack()

janela.mainloop()
