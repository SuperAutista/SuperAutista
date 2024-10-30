import tkinter as tk
from tkinter import messagebox, simpledialog
from decimal import Decimal, getcontext
from sympy import symbols, sympify, integrate, solve, plot, Eq
from sympy.core.sympify import SympifyError
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Configuração de precisão decimal
getcontext().prec = 50

# Definição das variáveis simbólicas para integrais múltiplas
x, y, z = symbols('x y z')

class TI84Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Calculadora TI-84 Estilo")
        master.geometry("600x800")
        master.configure(bg="#1E1E1E")  # Fundo escuro similar à TI-84

        # Frame para o display
        self.frame_display = tk.Frame(master, bg="#1E1E1E")
        self.frame_display.pack(fill=tk.BOTH, padx=10, pady=20)

        self.display = tk.Entry(self.frame_display, font=("Consolas", 24), borderwidth=2, relief="groove",
                                justify='right', bg="#000000", fg="#00FF00")
        self.display.pack(fill=tk.BOTH, ipady=10)

        # Frame para os botões
        self.frame_botoes = tk.Frame(master, bg="#1E1E1E")
        self.frame_botoes.pack(fill=tk.BOTH, padx=10, pady=10)

        # Definição dos botões com cores diferenciadas
        botoes = [
            ['7', '8', '9', '/', 'sin'],
            ['4', '5', '6', '*', 'cos'],
            ['1', '2', '3', '-', 'tan'],
            ['0', '.', '^', '+', 'log'],
            ['(', ')', '√', 'EXP', 'ln'],
            ['C', 'DEL', '∫', 'Solve', 'Plot'],
            ['Stat', 'Matrix', 'Prog', 'Ans', '=']
        ]

        # Cores para diferentes tipos de botões
        cores_botoes = {
            'numeros': "#4CAF50",      # Verde para números
            'operadores': "#FF9800",   # Laranja para operadores
            'funcoes': "#2196F3",      # Azul para funções
            'especial': "#f44336"      # Vermelho para funções especiais
        }

        # Criação da grade de botões usando grid dentro de frame_botoes
        for linha, fila in enumerate(botoes, start=0):
            for coluna, botao in enumerate(fila):
                if botao.isdigit() or botao in ['.', 'EXP']:
                    cor = cores_botoes['numeros']
                elif botao in ['/', '*', '-', '+', '^']:
                    cor = cores_botoes['operadores']
                elif botao in ['sin', 'cos', 'tan', '√', 'log', 'ln']:
                    cor = cores_botoes['funcoes']
                elif botao in ['C', 'DEL', '∫', 'Solve', 'Plot', 'Stat', 'Matrix', 'Prog', 'Ans', '=']:
                    cor = cores_botoes['especial']
                else:
                    cor = "#FFFFFF"  # Branco como padrão

                action = lambda x=botao: self.clicar(x)
                tk.Button(
                    self.frame_botoes, text=botao, width=8, height=2, font=("Consolas", 14),
                    bg=cor, fg="#FFFFFF", activebackground="#555555", activeforeground="#FFFFFF",
                    borderwidth=0, relief="flat", command=action
                ).grid(row=linha, column=coluna, padx=3, pady=3)

        # Botão para acessar o histórico (implementação futura)
        self.historico = []

    def clicar(self, valor):
        if valor == 'C':
            self.display.delete(0, tk.END)
        elif valor == 'DEL':
            texto_atual = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(0, texto_atual[:-1])
        elif valor == '=':
            expressao = self.display.get()
            try:
                resultado = self.calcular(expressao)
                self.historico.append(f"{expressao} = {resultado}")
                self.display.delete(0, tk.END)
                self.display.insert(0, str(resultado))
            except Exception as e:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Erro")
        elif valor == '∫':
            self.resolver_integral()
        elif valor == 'Solve':
            self.resolver_equacao()
        elif valor == 'Plot':
            self.plotar_grafico()
        elif valor == 'Stat':
            self.analisar_estatisticas()
        elif valor == 'Matrix':
            self.manipular_matriz()
        elif valor == 'Prog':
            self.programar_calculadora()
        elif valor == 'Ans':
            self.usar_ultimo_resultado()
        else:
            self.display.insert(tk.END, valor)

    def calcular(self, expressao):
        # Substituições para funções matemáticas
        expressao = expressao.replace('^', '**')
        expressao = expressao.replace('√', 'sqrt')
        expressao = expressao.replace('EXP', 'e')
        try:
            expr = sympify(expressao)
            resultado = expr.evalf(26)
            return resultado
        except SympifyError:
            # Uso de Decimal para operações básicas
            try:
                return str(Decimal(expressao))
            except:
                raise
        except Exception as e:
            raise

    def resolver_integral(self):
        # Janela para inserir a integral definida
        janela = tk.Toplevel(self.master)
        janela.title("Resolver Integral Definida")
        janela.geometry("400x400")
        janela.configure(bg="#1E1E1E")

        # Frame para os campos de entrada
        frame_entrada = tk.Frame(janela, bg="#1E1E1E")
        frame_entrada.pack(pady=10, padx=10)

        # Expressão
        tk.Label(frame_entrada, text="Expressão:", font=("Consolas", 12), bg="#1E1E1E", fg="#FFFFFF").grid(row=0, column=0, sticky='e', pady=5)
        entrada_expr = tk.Entry(frame_entrada, font=("Consolas", 14), width=25, bg="#000000", fg="#00FF00")
        entrada_expr.grid(row=0, column=1, pady=5)

        # Variável
        tk.Label(frame_entrada, text="Variável:", font=("Consolas", 12), bg="#1E1E1E", fg="#FFFFFF").grid(row=1, column=0, sticky='e', pady=5)
        entrada_var = tk.Entry(frame_entrada, font=("Consolas", 14), width=25, bg="#000000", fg="#00FF00")
        entrada_var.grid(row=1, column=1, pady=5)

        # Limite Inferior
        tk.Label(frame_entrada, text="Limite Inferior:", font=("Consolas", 12), bg="#1E1E1E", fg="#FFFFFF").grid(row=2, column=0, sticky='e', pady=5)
        entrada_lim_inf = tk.Entry(frame_entrada, font=("Consolas", 14), width=25, bg="#000000", fg="#00FF00")
        entrada_lim_inf.grid(row=2, column=1, pady=5)

        # Limite Superior
        tk.Label(frame_entrada, text="Limite Superior:", font=("Consolas", 12), bg="#1E1E1E", fg="#FFFFFF").grid(row=3, column=0, sticky='e', pady=5)
        entrada_lim_sup = tk.Entry(frame_entrada, font=("Consolas", 14), width=25, bg="#000000", fg="#00FF00")
        entrada_lim_sup.grid(row=3, column=1, pady=5)

        # Botão para calcular a integral
        def calcular_integral():
            expr = entrada_expr.get()
            var = entrada_var.get()
            lim_inf = entrada_lim_inf.get()
            lim_sup = entrada_lim_sup.get()
            try:
                simbolo = symbols(var)
                expr_sympy = sympify(expr)
                lim_inf_sym = sympify(lim_inf)
                lim_sup_sym = sympify(lim_sup)
                integral = integrate(expr_sympy, (simbolo, lim_inf_sym, lim_sup_sym))
                resultado = integral.evalf(26)
                messagebox.showinfo("Resultado", f"Integral Definida: {resultado}")
            except Exception as e:
                messagebox.showerror("Erro", "Erro ao calcular a integral.")

        tk.Button(
            janela, text="Calcular", font=("Consolas", 14), command=calcular_integral,
            bg="#2196F3", fg="#FFFFFF", activebackground="#555555", activeforeground="#FFFFFF",
            borderwidth=0, relief="flat"
        ).pack(pady=20)

    def resolver_equacao(self):
        # Janela para resolver equações
        janela = tk.Toplevel(self.master)
        janela.title("Resolver Equação")
        janela.geometry("400x300")
        janela.configure(bg="#1E1E1E")

        frame_entrada = tk.Frame(janela, bg="#1E1E1E")
        frame_entrada.pack(pady=10, padx=10)

        tk.Label(frame_entrada, text="Equação:", font=("Consolas", 12), bg="#1E1E1E", fg="#FFFFFF").grid(row=0, column=0, sticky='e', pady=5)
        entrada_eq = tk.Entry(frame_entrada, font=("Consolas", 14), width=25, bg="#000000", fg="#00FF00")
        entrada_eq.grid(row=0, column=1, pady=5)

        tk.Label(frame_entrada, text="Variável:", font=("Consolas", 12), bg="#1E1E1E", fg="#FFFFFF").grid(row=1, column=0, sticky='e', pady=5)
        entrada_var = tk.Entry(frame_entrada, font=("Consolas", 14), width=25, bg="#000000", fg="#00FF00")
        entrada_var.grid(row=1, column=1, pady=5)

        def resolver():
            eq = entrada_eq.get()
            var = entrada_var.get()
            try:
                simbolo = symbols(var)
                equacao = sympify(eq)
                sol = solve(Eq(equacao, 0), simbolo)
                messagebox.showinfo("Resultado", f"Solução: {sol}")
            except Exception as e:
                messagebox.showerror("Erro", "Erro ao resolver a equação.")

        tk.Button(
            janela, text="Resolver", font=("Consolas", 14), command=resolver,
            bg="#2196F3", fg="#FFFFFF", activebackground="#555555", activeforeground="#FFFFFF",
            borderwidth=0, relief="flat"
        ).pack(pady=20)

    def plotar_grafico(self):
        # Janela para plotar gráficos
        janela = tk.Toplevel(self.master)
        janela.title("Plotar Gráfico")
        janela.geometry("700x600")
        janela.configure(bg="#1E1E1E")

        frame_entrada = tk.Frame(janela, bg="#1E1E1E")
        frame_entrada.pack(pady=10, padx=10)

        tk.Label(frame_entrada, text="Função f(x):", font=("Consolas", 12), bg="#1E1E1E", fg="#FFFFFF").grid(row=0, column=0, sticky='e', pady=5)
        entrada_func = tk.Entry(frame_entrada, font=("Consolas", 14), width=30, bg="#000000", fg="#00FF00")
        entrada_func.grid(row=0, column=1, pady=5)

        tk.Label(frame_entrada, text="x Inicial:", font=("Consolas", 12), bg="#1E1E1E", fg="#FFFFFF").grid(row=1, column=0, sticky='e', pady=5)
        entrada_x_inicial = tk.Entry(frame_entrada, font=("Consolas", 14), width=30, bg="#000000", fg="#00FF00")
        entrada_x_inicial.grid(row=1, column=1, pady=5)

        tk.Label(frame_entrada, text="x Final:", font=("Consolas", 12), bg="#1E1E1E", fg="#FFFFFF").grid(row=2, column=0, sticky='e', pady=5)
        entrada_x_final = tk.Entry(frame_entrada, font=("Consolas", 14), width=30, bg="#000000", fg="#00FF00")
        entrada_x_final.grid(row=2, column=1, pady=5)

        def plotar():
            func = entrada_func.get()
            x_inicial = entrada_x_inicial.get()
            x_final = entrada_x_final.get()
            try:
                x_vals = np.linspace(float(x_inicial), float(x_final), 400)
                expr = sympify(func)
                f = lambdify(x, expr, modules=['numpy'])
                y_vals = f(x_vals)

                fig, ax = plt.subplots(figsize=(6,4))
                ax.plot(x_vals, y_vals, label=f"f(x) = {func}")
                ax.set_xlabel("x")
                ax.set_ylabel("f(x)")
                ax.set_title("Gráfico da Função")
                ax.legend()
                ax.grid(True)

                # Exibir no Tkinter
                canvas = FigureCanvasTkAgg(fig, master=janela)
                canvas.draw()
                canvas.get_tk_widget().pack()

            except Exception as e:
                messagebox.showerror("Erro", "Erro ao plotar o gráfico.")

        tk.Button(
            janela, text="Plotar", font=("Consolas", 14), command=plotar,
            bg="#2196F3", fg="#FFFFFF", activebackground="#555555", activeforeground="#FFFFFF",
            borderwidth=0, relief="flat"
        ).pack(pady=20)

    def analisar_estatisticas(self):
        # Janela para análise estatística
        janela = tk.Toplevel(self.master)
        janela.title("Análise Estatística")
        janela.geometry("500x500")
        janela.configure(bg="#1E1E1E")

        frame_entrada = tk.Frame(janela, bg="#1E1E1E")
        frame_entrada.pack(pady=10, padx=10)

        tk.Label(frame_entrada, text="Dados (separados por vírgula):", font=("Consolas", 12), bg="#1E1E1E", fg="#FFFFFF").grid(row=0, column=0, sticky='e', pady=5)
        entrada_dados = tk.Entry(frame_entrada, font=("Consolas", 14), width=40, bg="#000000", fg="#00FF00")
        entrada_dados.grid(row=0, column=1, pady=5)

        def calcular_estatisticas():
            dados = entrada_dados.get().split(',')
            try:
                dados = [float(d.strip()) for d in dados]
                media = np.mean(dados)
                mediana = np.median(dados)
                desvio = np.std(dados)
                variancia = np.var(dados)
                minimo = np.min(dados)
                maximo = np.max(dados)

                resultado = (
                    f"Média: {media}\n"
                    f"Mediana: {mediana}\n"
                    f"Desvio Padrão: {desvio}\n"
                    f"Variância: {variancia}\n"
                    f"Mínimo: {minimo}\n"
                    f"Máximo: {maximo}"
                )

                messagebox.showinfo("Estatísticas", resultado)
            except Exception as e:
                messagebox.showerror("Erro", "Erro ao calcular estatísticas.")

        tk.Button(
            janela, text="Calcular", font=("Consolas", 14), command=calcular_estatisticas,
            bg="#2196F3", fg="#FFFFFF", activebackground="#555555", activeforeground="#FFFFFF",
            borderwidth=0, relief="flat"
        ).pack(pady=20)

    def manipular_matriz(self):
        # Placeholder para manipulação de matrizes
        messagebox.showinfo("Matrizes", "Função de manipulação de matrizes ainda não implementada.")

    def programar_calculadora(self):
        # Placeholder para programação da calculadora
        messagebox.showinfo("Programação", "Função de programação ainda não implementada.")

    def usar_ultimo_resultado(self):
        if self.historico:
            ultimo = self.historico[-1].split('=')[1].strip()
            self.display.insert(tk.END, ultimo)
        else:
            messagebox.showinfo("Ans", "Nenhum resultado anterior disponível.")

if __name__ == "__main__":
    root = tk.Tk()
    calculator = TI84Calculator(root)
    root.mainloop()
