import tkinter as tk
from tkinter import messagebox
import cmath
import numpy as np

def resolver_equacao():
    grau = int(var_grau.get())
    try:
        if grau == 2:
            a = float(entrada_a.get())
            b = float(entrada_b.get())
            c = float(entrada_c.get())
            delta = b**2 - 4*a*c
            raiz_delta = cmath.sqrt(delta)
            x1 = (-b + raiz_delta) / (2*a)
            x2 = (-b - raiz_delta) / (2*a)
            resultado = f"Raízes: x₁ = {x1}, x₂ = {x2}"
        
        elif grau == 3:
            a = float(entrada_a.get())
            b = float(entrada_b.get())
            c = float(entrada_c.get())
            d = float(entrada_d.get())
            # Usando a fórmula de Cardano para equações cúbicas
            f = ((3*b/a) - ((c**2)/(a**2))) / 3
            g = ((2*(c**3)/(a**3)) - (9*b*c)/(a**2) + (27*d)/a) / 27
            h = (g**2)/4 + (f**3)/27
            if h > 0:
                R = -(g/2) + cmath.sqrt(h)
                S = R**(1/3)
                T = -(g/2) - cmath.sqrt(h)
                U = T**(1/3)
                x1 = S + U - (b / (3*a))
                resultado = f"Raízes: x₁ = {x1}"
            elif f == 0 and g == 0 and h == 0:
                x = - (d/a)**(1/3)
                resultado = f"Raízes múltiplas: x = {x}"
            else:
                i = cmath.sqrt((g**2)/4 - h)
                j = i**(1/3)
                k = cmath.acos(-(g)/(2*i))
                L = -j
                M = cmath.cos(k/3)
                N = cmath.sqrt(3) * cmath.sin(k/3)
                P = -b / (3*a)
                x1 = 2*j*cmath.cos(k/3) - (b / (3*a))
                x2 = L*(M + N) + P
                x3 = L*(M - N) + P
                resultado = f"Raízes: x₁ = {x1}, x₂ = {x2}, x₃ = {x3}"
        
        elif grau == 5:
            a = float(entrada_a.get())
            b = float(entrada_b.get())
            c = float(entrada_c.get())
            d = float(entrada_d.get())
            e = float(entrada_e.get())
            f_coef = float(entrada_f.get())
            coeficientes = [a, b, c, d, e, f_coef]
            # Usando numpy para encontrar as raízes
            raizes = np.roots(coeficientes)
            resultado = "Raízes:\n"
            for i, raiz in enumerate(raizes, start=1):
                resultado += f"x{i} = {raiz}\n"
        else:
            resultado = "Grau inválido. Por favor, selecione 2, 3 ou 5."
        
        label_resultado.config(text=resultado)
    
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira coeficientes válidos.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Criando a janela principal
janela = tk.Tk()
janela.title("Resolutor de Equações")
janela.geometry("400x500")

# Variável para o grau da equação
var_grau = tk.StringVar(value="2")

# Seleção do grau da equação
frame_grau = tk.Frame(janela)
frame_grau.pack(pady=10)

tk.Label(frame_grau, text="Grau da Equação:").pack(side=tk.LEFT, padx=5)
for grau in [2, 3, 5]:
    tk.Radiobutton(frame_grau, text=str(grau), variable=var_grau, value=str(grau), command=lambda: atualizar_campos()).pack(side=tk.LEFT)

# Função para atualizar os campos de entrada conforme o grau selecionado
def atualizar_campos():
    grau = int(var_grau.get())
    campos = [label_a, entrada_a, label_b, entrada_b]
    
    # Remover campos d, e, f se não forem necessários
    if grau < 3:
        label_d.pack_forget()
        entrada_d.pack_forget()
    else:
        label_d.pack(pady=2)
        entrada_d.pack(pady=2)
    
    if grau == 5:
        label_e.pack(pady=2)
        entrada_e.pack(pady=2)
        label_f.pack(pady=2)
        entrada_f.pack(pady=2)
    else:
        label_e.pack_forget()
        entrada_e.pack_forget()
        label_f.pack_forget()
        entrada_f.pack_forget()

# Labels e entradas para os coeficientes
label_a = tk.Label(janela, text="a:")
label_a.pack()
entrada_a = tk.Entry(janela)
entrada_a.pack()

label_b = tk.Label(janela, text="b:")
label_b.pack()
entrada_b = tk.Entry(janela)
entrada_b.pack()

label_c = tk.Label(janela, text="c:")
label_c.pack()
entrada_c = tk.Entry(janela)
entrada_c.pack()

label_d = tk.Label(janela, text="d:")
entrada_d = tk.Entry(janela)

label_e = tk.Label(janela, text="e:")
entrada_e = tk.Entry(janela)

label_f = tk.Label(janela, text="f:")
entrada_f = tk.Entry(janela)

# Botão para resolver
botao_resolver = tk.Button(janela, text="Resolver", command=resolver_equacao)
botao_resolver.pack(pady=10)

# Label para exibir o resultado
label_resultado = tk.Label(janela, text="", justify=tk.LEFT)
label_resultado.pack(pady=10)

# Atualizar campos inicialmente
atualizar_campos()

# Label de autor
label_autor = tk.Label(janela, text="Autor: Luiz Tiago Wilcke", font=("Arial", 10, "italic"))
label_autor.pack(side=tk.BOTTOM, pady=10)

# Iniciando o loop da interface
janela.mainloop()
