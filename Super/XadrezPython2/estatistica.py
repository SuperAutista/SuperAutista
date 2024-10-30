import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy import stats

class AplicativoProbabilidadeAvancada(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cálculos Avançados de Probabilidade")
        self.geometry("900x700")
        
        # Variáveis
        self.distribuicao_var = tk.StringVar(value="Normal")
        self.parametros_var = {}
        self.resultado_var = tk.StringVar()
        
        # Interface
        self.criar_widgets()
    
    def criar_widgets(self):
        # Frame para seleção de distribuição
        frame_distribuicao = ttk.LabelFrame(self, text="Seleção da Distribuição")
        frame_distribuicao.pack(pady=10, padx=10, fill='x')
        
        lbl_distribuicao = ttk.Label(frame_distribuicao, text="Distribuição:")
        lbl_distribuicao.pack(side='left', padx=5, pady=5)
        
        opções_distribuicao = ["Normal", "Binomial", "Poisson"]
        menu_distribuicao = ttk.OptionMenu(frame_distribuicao, self.distribuicao_var, opções_distribuicao[0], *opções_distribuicao, command=self.atualizar_parametros)
        menu_distribuicao.pack(side='left', padx=5, pady=5)
        
        # Frame para parâmetros
        self.frame_parametros = ttk.LabelFrame(self, text="Parâmetros da Distribuição")
        self.frame_parametros.pack(pady=10, padx=10, fill='x')
        
        self.atualizar_parametros(self.distribuicao_var.get())
        
        # Frame para cálculos
        frame_calculos = ttk.LabelFrame(self, text="Cálculos de Probabilidade")
        frame_calculos.pack(pady=10, padx=10, fill='x')
        
        lbl_tipo_calculo = ttk.Label(frame_calculos, text="Tipo de Cálculo:")
        lbl_tipo_calculo.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        self.tipo_calculo_var = tk.StringVar(value="P(X ≤ x)")
        opções_calculo = ["P(X ≤ x)", "P(X = k)", "P(a ≤ X ≤ b)"]
        menu_calculo = ttk.OptionMenu(frame_calculos, self.tipo_calculo_var, opções_calculo[0], *opções_calculo, command=self.atualizar_campos_calculo)
        menu_calculo.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        # Campos dinâmicos para cálculos
        self.campos_calculo_frame = ttk.Frame(frame_calculos)
        self.campos_calculo_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='w')
        
        self.atualizar_campos_calculo(self.tipo_calculo_var.get())
        
        # Botão para calcular
        btn_calcular = ttk.Button(frame_calculos, text="Calcular", command=self.calcular_probabilidade)
        btn_calcular.grid(row=2, column=0, padx=5, pady=10, sticky='w')
        
        # Botão para plotar
        btn_plotar = ttk.Button(frame_calculos, text="Plotar Distribuição", command=self.plotar_distribuicao)
        btn_plotar.grid(row=2, column=1, padx=5, pady=10, sticky='w')
        
        # Botão para resetar
        btn_resetar = ttk.Button(frame_calculos, text="Resetar", command=self.resetar)
        btn_resetar.grid(row=2, column=2, padx=5, pady=10, sticky='w')
        
        # Frame para resultado
        frame_resultado = ttk.LabelFrame(self, text="Resultado")
        frame_resultado.pack(pady=10, padx=10, fill='both', expand=True)
        
        lbl_resultado = ttk.Label(frame_resultado, textvariable=self.resultado_var, justify='left', font=("Arial", 12))
        lbl_resultado.pack(padx=10, pady=10)
    
    def atualizar_parametros(self, distribuicao):
        # Limpar frame de parâmetros
        for widget in self.frame_parametros.winfo_children():
            widget.destroy()
        self.parametros_var.clear()
        
        if distribuicao == "Normal":
            # Média e Desvio Padrão
            lbl_media = ttk.Label(self.frame_parametros, text="Média (μ):")
            lbl_media.grid(row=0, column=0, padx=5, pady=5, sticky='w')
            entry_media = ttk.Entry(self.frame_parametros)
            entry_media.grid(row=0, column=1, padx=5, pady=5, sticky='w')
            self.parametros_var['media'] = entry_media
            
            lbl_desvio = ttk.Label(self.frame_parametros, text="Desvio Padrão (σ):")
            lbl_desvio.grid(row=1, column=0, padx=5, pady=5, sticky='w')
            entry_desvio = ttk.Entry(self.frame_parametros)
            entry_desvio.grid(row=1, column=1, padx=5, pady=5, sticky='w')
            self.parametros_var['desvio'] = entry_desvio
        
        elif distribuicao == "Binomial":
            # Número de Tentativas e Probabilidade de Sucesso
            lbl_n = ttk.Label(self.frame_parametros, text="Número de Tentativas (n):")
            lbl_n.grid(row=0, column=0, padx=5, pady=5, sticky='w')
            entry_n = ttk.Entry(self.frame_parametros)
            entry_n.grid(row=0, column=1, padx=5, pady=5, sticky='w')
            self.parametros_var['n'] = entry_n
            
            lbl_p = ttk.Label(self.frame_parametros, text="Probabilidade de Sucesso (p):")
            lbl_p.grid(row=1, column=0, padx=5, pady=5, sticky='w')
            entry_p = ttk.Entry(self.frame_parametros)
            entry_p.grid(row=1, column=1, padx=5, pady=5, sticky='w')
            self.parametros_var['p'] = entry_p
        
        elif distribuicao == "Poisson":
            # Taxa Média (λ)
            lbl_lambda = ttk.Label(self.frame_parametros, text="Taxa Média (λ):")
            lbl_lambda.grid(row=0, column=0, padx=5, pady=5, sticky='w')
            entry_lambda = ttk.Entry(self.frame_parametros)
            entry_lambda.grid(row=0, column=1, padx=5, pady=5, sticky='w')
            self.parametros_var['lambda'] = entry_lambda
    
    def atualizar_campos_calculo(self, tipo_calculo):
        # Limpar frame de campos de cálculo
        for widget in self.campos_calculo_frame.winfo_children():
            widget.destroy()
        
        self.campos_calculo = {}
        
        if tipo_calculo == "P(X ≤ x)":
            lbl_x = ttk.Label(self.campos_calculo_frame, text="Valor de x:")
            lbl_x.grid(row=0, column=0, padx=5, pady=5, sticky='w')
            entry_x = ttk.Entry(self.campos_calculo_frame)
            entry_x.grid(row=0, column=1, padx=5, pady=5, sticky='w')
            self.campos_calculo['x'] = entry_x
        
        elif tipo_calculo == "P(X = k)":
            lbl_k = ttk.Label(self.campos_calculo_frame, text="Valor de k:")
            lbl_k.grid(row=0, column=0, padx=5, pady=5, sticky='w')
            entry_k = ttk.Entry(self.campos_calculo_frame)
            entry_k.grid(row=0, column=1, padx=5, pady=5, sticky='w')
            self.campos_calculo['k'] = entry_k
        
        elif tipo_calculo == "P(a ≤ X ≤ b)":
            lbl_a = ttk.Label(self.campos_calculo_frame, text="Valor de a:")
            lbl_a.grid(row=0, column=0, padx=5, pady=5, sticky='w')
            entry_a = ttk.Entry(self.campos_calculo_frame)
            entry_a.grid(row=0, column=1, padx=5, pady=5, sticky='w')
            self.campos_calculo['a'] = entry_a
            
            lbl_b = ttk.Label(self.campos_calculo_frame, text="Valor de b:")
            lbl_b.grid(row=1, column=0, padx=5, pady=5, sticky='w')
            entry_b = ttk.Entry(self.campos_calculo_frame)
            entry_b.grid(row=1, column=1, padx=5, pady=5, sticky='w')
            self.campos_calculo['b'] = entry_b
    
    def obter_parametros(self):
        distribuicao = self.distribuicao_var.get()
        parametros = {}
        try:
            if distribuicao == "Normal":
                media = float(self.parametros_var['media'].get())
                desvio = float(self.parametros_var['desvio'].get())
                if desvio <= 0:
                    raise ValueError("O desvio padrão deve ser positivo.")
                parametros['media'] = media
                parametros['desvio'] = desvio
            elif distribuicao == "Binomial":
                n = int(self.parametros_var['n'].get())
                p = float(self.parametros_var['p'].get())
                if n <= 0 or not (0 <= p <= 1):
                    raise ValueError("n deve ser positivo e p entre 0 e 1.")
                parametros['n'] = n
                parametros['p'] = p
            elif distribuicao == "Poisson":
                lambda_ = float(self.parametros_var['lambda'].get())
                if lambda_ <= 0:
                    raise ValueError("λ deve ser positivo.")
                parametros['lambda'] = lambda_
            return parametros
        except ValueError as e:
            messagebox.showerror("Erro de Entrada", str(e))
            return None
    
    def calcular_probabilidade(self):
        distribuicao = self.distribuicao_var.get()
        parametros = self.obter_parametros()
        if not parametros:
            return
        
        tipo_calculo = self.tipo_calculo_var.get()
        try:
            if tipo_calculo == "P(X ≤ x)":
                x = float(self.campos_calculo['x'].get())
                if distribuicao == "Normal":
                    media = parametros['media']
                    desvio = parametros['desvio']
                    prob = stats.norm.cdf(x, loc=media, scale=desvio)
                elif distribuicao == "Binomial":
                    n = parametros['n']
                    p = parametros['p']
                    prob = stats.binom.cdf(int(x), n, p)
                elif distribuicao == "Poisson":
                    lambda_ = parametros['lambda']
                    prob = stats.poisson.cdf(int(x), lambda_)
                self.resultado_var.set(f"P(X ≤ {x}) = {prob:.4f}")
            
            elif tipo_calculo == "P(X = k)":
                k = int(self.campos_calculo['k'].get())
                if distribuicao == "Normal":
                    # Para distribuições contínuas, P(X = k) é praticamente 0
                    prob = stats.norm.pdf(k, loc=parametros['media'], scale=parametros['desvio'])
                    self.resultado_var.set(f"P(X = {k}) ≈ {prob:.4f} (densidade de probabilidade)")
                elif distribuicao == "Binomial":
                    n = parametros['n']
                    p = parametros['p']
                    prob = stats.binom.pmf(k, n, p)
                    self.resultado_var.set(f"P(X = {k}) = {prob:.4f}")
                elif distribuicao == "Poisson":
                    lambda_ = parametros['lambda']
                    prob = stats.poisson.pmf(k, lambda_)
                    self.resultado_var.set(f"P(X = {k}) = {prob:.4f}")
            
            elif tipo_calculo == "P(a ≤ X ≤ b)":
                a = float(self.campos_calculo['a'].get())
                b = float(self.campos_calculo['b'].get())
                if a > b:
                    raise ValueError("a deve ser menor ou igual a b.")
                if distribuicao == "Normal":
                    media = parametros['media']
                    desvio = parametros['desvio']
                    prob = stats.norm.cdf(b, loc=media, scale=desvio) - stats.norm.cdf(a, loc=media, scale=desvio)
                elif distribuicao == "Binomial":
                    n = parametros['n']
                    p = parametros['p']
                    prob = stats.binom.cdf(int(b), n, p) - stats.binom.cdf(int(a)-1, n, p)
                elif distribuicao == "Poisson":
                    lambda_ = parametros['lambda']
                    prob = stats.poisson.cdf(int(b), lambda_) - stats.poisson.cdf(int(a)-1, lambda_)
                self.resultado_var.set(f"P({a} ≤ X ≤ {b}) = {prob:.4f}")
        
        except ValueError as e:
            messagebox.showerror("Erro de Entrada", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
    
    def plotar_distribuicao(self):
        distribuicao = self.distribuicao_var.get()
        parametros = self.obter_parametros()
        if not parametros:
            return
        
        fig, ax = plt.subplots(figsize=(6,4))
        
        if distribuicao == "Normal":
            media = parametros['media']
            desvio = parametros['desvio']
            x = np.linspace(media - 4*desvio, media + 4*desvio, 1000)
            y = stats.norm.pdf(x, loc=media, scale=desvio)
            ax.plot(x, y, label='Densidade de Probabilidade')
            ax.fill_between(x, y, alpha=0.2)
            ax.set_title(f'Distribuição Normal (μ={media}, σ={desvio})')
            ax.set_xlabel('x')
            ax.set_ylabel('f(x)')
        
        elif distribuicao == "Binomial":
            n = parametros['n']
            p = parametros['p']
            k = np.arange(0, n+1)
            y = stats.binom.pmf(k, n, p)
            ax.bar(k, y, color='skyblue', edgecolor='black')
            ax.set_title(f'Distribuição Binomial (n={n}, p={p})')
            ax.set_xlabel('k')
            ax.set_ylabel('P(X=k)')
        
        elif distribuicao == "Poisson":
            lambda_ = parametros['lambda']
            k = np.arange(0, stats.poisson.ppf(0.99, lambda_) + 1)
            y = stats.poisson.pmf(k, lambda_)
            ax.bar(k, y, color='lightgreen', edgecolor='black')
            ax.set_title(f'Distribuição de Poisson (λ={lambda_})')
            ax.set_xlabel('k')
            ax.set_ylabel('P(X=k)')
        
        ax.grid(True)
        ax.legend()
        
        # Exibir gráfico em uma nova janela
        janela_plot = tk.Toplevel(self)
        janela_plot.title("Gráfico da Distribuição")
        canvas = FigureCanvasTkAgg(fig, master=janela_plot)
        canvas.draw()
        canvas.get_tk_widget().pack()
    
    def resetar(self):
        # Resetar todos os campos
        self.distribuicao_var.set("Normal")
        self.atualizar_parametros("Normal")
        self.tipo_calculo_var.set("P(X ≤ x)")
        self.atualizar_campos_calculo("P(X ≤ x)")
        self.resultado_var.set("")
    
if __name__ == "__main__":
    app = AplicativoProbabilidadeAvancada()
    app.mainloop()
