import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm, lognorm, t, pareto, beta
import warnings

# Suprimir avisos de distribuições que podem não estar bem definidas
warnings.filterwarnings("ignore")

class ModeloPrecoDolar:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Modelo de Previsão do Preço do Dólar")
        self.criar_gui()
        self.dados = None

    def criar_gui(self):
        # Criar abas
        abas = ttk.Notebook(self.raiz)
        abas.pack(expand=1, fill='both')

        # Aba de Cálculo
        aba_calculo = ttk.Frame(abas)
        abas.add(aba_calculo, text='Modelo')

        # Aba de Explicações
        aba_explicacoes = ttk.Frame(abas)
        abas.add(aba_explicacoes, text='Explicações')

        # Aba de Dados
        aba_dados = ttk.Frame(abas)
        abas.add(aba_dados, text='Dados')

        # Widgets da Aba de Dados
        frame_dados = ttk.Frame(aba_dados, padding="10")
        frame_dados.pack(fill='both', expand=True)

        self.botao_carregar = ttk.Button(frame_dados, text="Carregar Dados CSV", command=self.carregar_dados)
        self.botao_carregar.pack(pady=10)

        self.texto_dados = tk.Text(frame_dados, height=15, width=80, state='disabled')
        self.texto_dados.pack(pady=10)

        # Widgets da Aba de Modelo
        frame_modelo = ttk.Frame(aba_calculo, padding="10")
        frame_modelo.pack(fill='both', expand=True)

        # Seleção de Distribuição
        ttk.Label(frame_modelo, text="Selecione a Distribuição:").grid(row=0, column=0, sticky='W')
        self.distribuicao_var = tk.StringVar()
        self.distribuicao_combo = ttk.Combobox(frame_modelo, textvariable=self.distribuicao_var, state='readonly')
        self.distribuicao_combo['values'] = [
            'Normal',
            'Lognormal',
            't de Student',
            'Pareto',
            'Beta'
        ]
        self.distribuicao_combo.grid(row=0, column=1, pady=5, sticky='W')
        self.distribuicao_combo.bind("<<ComboboxSelected>>", self.atualizar_campos)

        # Parâmetros (Serão atualizados conforme a distribuição selecionada)
        self.parametros_frame = ttk.Frame(frame_modelo)
        self.parametros_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky='W')

        # Botão de Ajuste e Plotagem
        self.botao_ajustar = ttk.Button(frame_modelo, text="Ajustar Distribuição e Plotar", command=self.ajustar_e_plotar)
        self.botao_ajustar.grid(row=2, column=0, columnspan=2, pady=10)

        # Texto de Resultados
        self.texto_resultados = tk.Text(frame_modelo, height=10, width=80, state='disabled')
        self.texto_resultados.grid(row=3, column=0, columnspan=2, pady=10)

        # Autor
        ttk.Label(frame_modelo, text="Autor: Luiz Tiago Wilcke").grid(row=4, column=0, columnspan=2, pady=5)

        # Widgets da Aba de Explicações
        texto_explicacoes = """
### Distribuições Probabilísticas Utilizadas

1. **Distribuição Normal**
   - **Fórmula**: f(x) = (1/(σ√(2π))) * exp(-0.5*((x - μ)/σ)^2)
   - **Descrição**: Assume que as variações seguem uma curva de sino, simétrica em torno da média μ.

2. **Distribuição Lognormal**
   - **Fórmula**: f(x) = (1/(xσ√(2π))) * exp(- (ln(x) - μ)^2 / (2σ^2))
   - **Descrição**: Modela variáveis que são produtos de múltiplos fatores positivos, como preços.

3. **Distribuição t de Student**
   - **Fórmula**: f(x) = Γ((ν+1)/2) / (√(νπ) Γ(ν/2)) * (1 + x²/ν)^(-(ν+1)/2)
   - **Descrição**: Utilizada para modelar dados com caudas mais pesadas que a normal, capturando eventos extremos.

4. **Distribuição Pareto**
   - **Fórmula**: f(x) = α * x_m^α / x^(α+1) para x >= x_m
   - **Descrição**: Modela fenômenos onde há uma grande probabilidade de ocorrência de eventos pequenos e uma pequena probabilidade de eventos muito grandes.

5. **Distribuição Beta**
   - **Fórmula**: f(x) = (x^(α-1) (1-x)^(β-1)) / B(α, β) para 0 <= x <= 1
   - **Descrição**: Utilizada para modelar variáveis limitadas em um intervalo, como probabilidades condicionais.
        """
        self.texto_explicacoes = tk.Text(aba_explicacoes, wrap='word', padx=10, pady=10)
        self.texto_explicacoes.insert('1.0', texto_explicacoes)
        self.texto_explicacoes.configure(state='disabled')
        self.texto_explicacoes.pack(expand=True, fill='both')

    def carregar_dados(self):
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione o Arquivo CSV",
            filetypes=(("Arquivos CSV", "*.csv"), ("Todos os Arquivos", "*.*"))
        )
        if caminho_arquivo:
            try:
                dados = pd.read_csv(caminho_arquivo)
                if 'Preco' not in dados.columns:
                    messagebox.showerror("Erro", "O arquivo CSV deve conter uma coluna chamada 'Preco'.")
                    return
                self.dados = dados['Preco'].dropna()
                # Exibir dados no texto_dados
                self.texto_dados.configure(state='normal')
                self.texto_dados.delete('1.0', tk.END)
                self.texto_dados.insert(tk.END, self.dados.describe().to_string())
                self.texto_dados.configure(state='disabled')
                messagebox.showinfo("Sucesso", "Dados carregados com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível carregar o arquivo:\n{e}")

    def atualizar_campos(self, event):
        # Limpar campos anteriores
        for widget in self.parametros_frame.winfo_children():
            widget.destroy()

        distribuicao = self.distribuicao_var.get()

        self.parametros = {}

        if distribuicao == 'Normal':
            ttk.Label(self.parametros_frame, text="Média (μ):").grid(row=0, column=0, sticky='W')
            self.parametros['media'] = tk.DoubleVar()
            ttk.Entry(self.parametros_frame, textvariable=self.parametros['media']).grid(row=0, column=1, pady=2)

            ttk.Label(self.parametros_frame, text="Desvio Padrão (σ):").grid(row=1, column=0, sticky='W')
            self.parametros['desvio'] = tk.DoubleVar()
            ttk.Entry(self.parametros_frame, textvariable=self.parametros['desvio']).grid(row=1, column=1, pady=2)

        elif distribuicao == 'Lognormal':
            ttk.Label(self.parametros_frame, text="Média Log (μ):").grid(row=0, column=0, sticky='W')
            self.parametros['media_log'] = tk.DoubleVar()
            ttk.Entry(self.parametros_frame, textvariable=self.parametros['media_log']).grid(row=0, column=1, pady=2)

            ttk.Label(self.parametros_frame, text="Desvio Log (σ):").grid(row=1, column=0, sticky='W')
            self.parametros['desvio_log'] = tk.DoubleVar()
            ttk.Entry(self.parametros_frame, textvariable=self.parametros['desvio_log']).grid(row=1, column=1, pady=2)

        elif distribuicao == 't de Student':
            ttk.Label(self.parametros_frame, text="Graus de Liberdade (ν):").grid(row=0, column=0, sticky='W')
            self.parametros['graus'] = tk.DoubleVar()
            ttk.Entry(self.parametros_frame, textvariable=self.parametros['graus']).grid(row=0, column=1, pady=2)

        elif distribuicao == 'Pareto':
            ttk.Label(self.parametros_frame, text="Parâmetro α:").grid(row=0, column=0, sticky='W')
            self.parametros['alpha'] = tk.DoubleVar()
            ttk.Entry(self.parametros_frame, textvariable=self.parametros['alpha']).grid(row=0, column=1, pady=2)

            ttk.Label(self.parametros_frame, text="Valor Mínimo (xₘ):").grid(row=1, column=0, sticky='W')
            self.parametros['xmin'] = tk.DoubleVar()
            ttk.Entry(self.parametros_frame, textvariable=self.parametros['xmin']).grid(row=1, column=1, pady=2)

        elif distribuicao == 'Beta':
            ttk.Label(self.parametros_frame, text="Parâmetro α:").grid(row=0, column=0, sticky='W')
            self.parametros['alpha'] = tk.DoubleVar()
            ttk.Entry(self.parametros_frame, textvariable=self.parametros['alpha']).grid(row=0, column=1, pady=2)

            ttk.Label(self.parametros_frame, text="Parâmetro β:").grid(row=1, column=0, sticky='W')
            self.parametros['beta'] = tk.DoubleVar()
            ttk.Entry(self.parametros_frame, textvariable=self.parametros['beta']).grid(row=1, column=1, pady=2)

    def ajustar_e_plotar(self):
        if self.dados is None:
            messagebox.showerror("Erro", "Por favor, carregue os dados primeiro.")
            return

        distribuicao = self.distribuicao_var.get()

        if not distribuicao:
            messagebox.showerror("Erro", "Por favor, selecione uma distribuição.")
            return

        try:
            dados = self.dados.values

            # Limpar texto de resultados
            self.texto_resultados.configure(state='normal')
            self.texto_resultados.delete('1.0', tk.END)

            if distribuicao == 'Normal':
                mu, sigma = norm.fit(dados)
                parametros = f"Média (μ) = {mu:.4f}\nDesvio Padrão (σ) = {sigma:.4f}"
                self.texto_resultados.insert(tk.END, parametros + "\n\n")

                # Plotagem
                plt.figure(figsize=(8,6))
                plt.hist(dados, bins=30, density=True, alpha=0.6, color='g', label='Dados')
                xmin, xmax = plt.xlim()
                x = np.linspace(xmin, xmax, 1000)
                y = norm.pdf(x, mu, sigma)
                plt.plot(x, y, 'r-', label='Normal Ajustada')
                plt.title(f'Distribuição Normal Ajustada\nμ = {mu:.4f}, σ = {sigma:.4f}')
                plt.xlabel('Preço do Dólar')
                plt.ylabel('Densidade de Probabilidade')
                plt.legend()
                plt.grid(True)
                plt.show()

            elif distribuicao == 'Lognormal':
                # Ajuste da distribuição lognormal
                shape, loc, scale = lognorm.fit(dados, floc=0)
                parametros = f"Forma (σ) = {shape:.4f}\nLocalização = {loc:.4f}\nEscala = {scale:.4f}"
                self.texto_resultados.insert(tk.END, parametros + "\n\n")

                # Plotagem
                plt.figure(figsize=(8,6))
                plt.hist(dados, bins=30, density=True, alpha=0.6, color='g', label='Dados')
                x = np.linspace(min(dados), max(dados), 1000)
                y = lognorm.pdf(x, shape, loc, scale)
                plt.plot(x, y, 'r-', label='Lognormal Ajustada')
                plt.title(f'Distribuição Lognormal Ajustada\nσ = {shape:.4f}, loc = {loc:.4f}, scale = {scale:.4f}')
                plt.xlabel('Preço do Dólar')
                plt.ylabel('Densidade de Probabilidade')
                plt.legend()
                plt.grid(True)
                plt.show()

            elif distribuicao == 't de Student':
                # Ajuste da distribuição t
                df, loc, scale = t.fit(dados)
                parametros = f"Graus de Liberdade (ν) = {df:.4f}\nLocalização = {loc:.4f}\nEscala = {scale:.4f}"
                self.texto_resultados.insert(tk.END, parametros + "\n\n")

                # Plotagem
                plt.figure(figsize=(8,6))
                plt.hist(dados, bins=30, density=True, alpha=0.6, color='g', label='Dados')
                x = np.linspace(min(dados), max(dados), 1000)
                y = t.pdf(x, df, loc, scale)
                plt.plot(x, y, 'r-', label='t de Student Ajustada')
                plt.title(f'Distribuição t de Student Ajustada\nν = {df:.4f}, loc = {loc:.4f}, scale = {scale:.4f}')
                plt.xlabel('Preço do Dólar')
                plt.ylabel('Densidade de Probabilidade')
                plt.legend()
                plt.grid(True)
                plt.show()

            elif distribuicao == 'Pareto':
                # Ajuste da distribuição Pareto
                alpha, loc, scale = pareto.fit(dados, floc=0)
                parametros = f"Parâmetro α = {alpha:.4f}\nLocalização = {loc:.4f}\nEscala = {scale:.4f}"
                self.texto_resultados.insert(tk.END, parametros + "\n\n")

                # Plotagem
                plt.figure(figsize=(8,6))
                plt.hist(dados, bins=30, density=True, alpha=0.6, color='g', label='Dados')
                x = np.linspace(min(dados), max(dados), 1000)
                y = pareto.pdf(x, alpha, loc, scale)
                plt.plot(x, y, 'r-', label='Pareto Ajustada')
                plt.title(f'Distribuição Pareto Ajustada\nα = {alpha:.4f}, loc = {loc:.4f}, scale = {scale:.4f}')
                plt.xlabel('Preço do Dólar')
                plt.ylabel('Densidade de Probabilidade')
                plt.legend()
                plt.grid(True)
                plt.show()

            elif distribuicao == 'Beta':
                # Para distribuição Beta, os dados devem estar no intervalo [0,1]
                minimo, maximo = min(dados), max(dados)
                dados_normalizados = (dados - minimo) / (maximo - minimo)
                alpha_param, beta_param, loc, scale = beta.fit(dados_normalizados, floc=0, fscale=1)
                parametros = f"Parâmetro α = {alpha_param:.4f}\nParâmetro β = {beta_param:.4f}"
                self.texto_resultados.insert(tk.END, parametros + "\n\n")

                # Plotagem
                plt.figure(figsize=(8,6))
                plt.hist(dados_normalizados, bins=30, density=True, alpha=0.6, color='g', label='Dados Normalizados')
                x = np.linspace(0, 1, 1000)
                y = beta.pdf(x, alpha_param, beta_param, loc, scale)
                plt.plot(x, y, 'r-', label='Beta Ajustada')
                plt.title(f'Distribuição Beta Ajustada\nα = {alpha_param:.4f}, β = {beta_param:.4f}')
                plt.xlabel('Preço do Dólar Normalizado')
                plt.ylabel('Densidade de Probabilidade')
                plt.legend()
                plt.grid(True)
                plt.show()

            else:
                messagebox.showerror("Erro", "Distribuição não suportada.")
                return

            self.texto_resultados.configure(state='disabled')

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao ajustar a distribuição:\n{e}")

def main():
    raiz = tk.Tk()
    app = ModeloPrecoDolar(raiz)
    raiz.mainloop()

if __name__ == "__main__":
    main()
