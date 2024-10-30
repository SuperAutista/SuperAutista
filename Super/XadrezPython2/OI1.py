# autor: Luiz Tiago Wilcke

import wikipedia
import sympy as sp
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import io
import tkinter as tk
from tkinter import scrolledtext, messagebox
import re

# Código pré-definido para o jogo de xadrez em Python
JOGO_XADREZ_CODIGO = """
# Jogo de Xadrez em Python

import sys

class Peca:
    def __init__(self, nome, cor):
        self.nome = nome
        self.cor = cor

    def __repr__(self):
        return f"{self.cor[0]}{self.nome[0]}"

class Tabuleiro:
    def __init__(self):
        self.tabuleiro = self.criar_tabuleiro()

    def criar_tabuleiro(self):
        tab = [[None for _ in range(8)] for _ in range(8)]
        # Colocar peças brancas
        tab[0][0] = Peca('Torre', 'Branca')
        tab[0][1] = Peca('Cavalo', 'Branca')
        tab[0][2] = Peca('Bispo', 'Branca')
        tab[0][3] = Peca('Rainha', 'Branca')
        tab[0][4] = Peca('Rei', 'Branca')
        tab[0][5] = Peca('Bispo', 'Branca')
        tab[0][6] = Peca('Cavalo', 'Branca')
        tab[0][7] = Peca('Torre', 'Branca')
        for i in range(8):
            tab[1][i] = Peca('Peão', 'Branca')
        # Colocar peças pretas
        tab[7][0] = Peca('Torre', 'Preta')
        tab[7][1] = Peca('Cavalo', 'Preta')
        tab[7][2] = Peca('Bispo', 'Preta')
        tab[7][3] = Peca('Rainha', 'Preta')
        tab[7][4] = Peca('Rei', 'Preta')
        tab[7][5] = Peca('Bispo', 'Preta')
        tab[7][6] = Peca('Cavalo', 'Preta')
        tab[7][7] = Peca('Torre', 'Preta')
        for i in range(8):
            tab[6][i] = Peca('Peão', 'Preta')
        return tab

    def imprimir_tabuleiro(self):
        for row in self.tabuleiro:
            print(' '.join([str(peca) if peca else '--' for peca in row]))
        print()

def main():
    tabuleiro = Tabuleiro()
    tabuleiro.imprimir_tabuleiro()
    print("Jogo de Xadrez Simples. Ainda em desenvolvimento.")

if __name__ == "__main__":
    main()
"""

def obter_resposta(pergunta):
    try:
        # Tentar buscar na Wikipédia
        resumo = wikipedia.summary(pergunta, sentences=2, auto_suggest=False, redirect=True)
        return resumo
    except wikipedia.DisambiguationError as e:
        return f"Várias opções encontradas para '{pergunta}': {', '.join(e.options[:5])}..."
    except wikipedia.PageError:
        return None
    except Exception as e:
        return f"Ocorreu um erro: {e}"

def resolver_equacao(expressao, variavel='x'):
    try:
        var = sp.symbols(variavel)
        eq = sp.sympify(expressao)
        solucao = sp.solve(eq, var)
        return solucao
    except Exception as e:
        return f"Erro ao resolver a equação: {e}"

def integrar(expressao, variavel='x'):
    try:
        var = sp.symbols(variavel)
        expr = sp.sympify(expressao)
        integral = sp.integrate(expr, var)
        return integral
    except Exception as e:
        return f"Erro ao integrar a expressão: {e}"

def renderizar_formula(formula):
    try:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, f"${formula}$", fontsize=20, ha='center')
        ax.axis('off')
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        img = Image.open(buf)
        plt.close(fig)
        return img
    except Exception as e:
        return f"Erro ao renderizar a fórmula: {e}"

class ChatbotAGI:
    def __init__(self, master):
        self.master = master
        master.title("Chatbot AGI - Luiz Tiago Wilcke")
        master.geometry("600x600")
        master.resizable(False, False)

        # Área de exibição de mensagens
        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, state='disabled', font=("Arial", 12))
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Frame para entrada de texto e botão
        self.input_frame = tk.Frame(master)
        self.input_frame.pack(padx=10, pady=10, fill=tk.X)

        self.input_label = tk.Label(self.input_frame, text="Você:")
        self.input_label.pack(side=tk.LEFT)

        self.input_entry = tk.Entry(self.input_frame, width=50, font=("Arial", 12))
        self.input_entry.pack(side=tk.LEFT, padx=5)
        self.input_entry.bind("<Return>", self.processar_input)

        self.send_button = tk.Button(self.input_frame, text="Enviar", command=self.processar_input)
        self.send_button.pack(side=tk.LEFT)

        # Label do autor
        self.autor_label = tk.Label(master, text="Autor: Luiz Tiago Wilcke", font=("Arial", 10, "italic"))
        self.autor_label.pack(side=tk.BOTTOM, pady=5)

        # Exibir mensagem de boas-vindas
        self.exibir_mensagem("AGI: Olá! Eu sou uma AGI simulada. Como posso ajudar você hoje?\nDigite 'sair' para encerrar a conversa.\n")

    def exibir_mensagem(self, mensagem):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, mensagem + "\n")
        self.text_area.config(state='disabled')
        self.text_area.see(tk.END)

    def processar_input(self, event=None):
        pergunta = self.input_entry.get().strip()
        if not pergunta:
            return
        self.exibir_mensagem(f"Você: {pergunta}")
        self.input_entry.delete(0, tk.END)

        if pergunta.lower() == 'sair':
            self.exibir_mensagem("AGI: Até mais! Autor: Luiz Tiago Wilcke")
            self.master.after(2000, self.master.quit)
            return

        resposta = self.obter_resposta_personalizada(pergunta)
        if resposta:
            self.exibir_mensagem(f"AGI: {resposta}")
        else:
            # Tentar obter resposta da Wikipédia
            resposta_wiki = obter_resposta(pergunta)
            if resposta_wiki:
                self.exibir_mensagem(f"AGI: {resposta_wiki}")
            else:
                self.exibir_mensagem("AGI: Desculpe, não encontrei informações sobre isso.")

    def obter_resposta_personalizada(self, pergunta):
        # Respostas para saudações e frases comuns
        saudações = ['oi', 'ola', 'olá', 'bom dia', 'boa tarde', 'boa noite']
        despedidas = ['tchau', 'até mais', 'até logo', 'adeus']
        solicitar_codigo = ['mostre código em python', 'mostrar código em python', 'gerar código python']

        # Converter pergunta para minúsculas para facilitar a correspondência
        pergunta_lower = pergunta.lower()

        # Verificar saudações
        for saudacao in saudações:
            if re.search(r'\b' + re.escape(saudacao) + r'\b', pergunta_lower):
                return self.responder_saudações(saudacao)

        # Verificar despedidas
        for despedida in despedidas:
            if re.search(r'\b' + re.escape(despedida) + r'\b', pergunta_lower):
                return self.responder_despedidas(despedida)

        # Verificar se a pergunta é sobre equações diferenciais
        if 'resolver equação diferencial' in pergunta_lower:
            self.exibir_mensagem("AGI: Por favor, digite a equação diferencial (ex: y'' + y = 0):")
            self.master.after(100, self.obter_equacao_diferencial)
            return ""

        # Verificar se a pergunta é sobre integrais
        if 'integrar' in pergunta_lower or 'mostrar uma integral' in pergunta_lower:
            self.exibir_mensagem("AGI: Por favor, digite a expressão para integrar (ex: x**2):")
            self.master.after(100, self.obter_integral)
            return ""

        # Verificar se a pergunta requer renderização de fórmula
        if 'mostrar fórmula' in pergunta_lower or 'exibir fórmula' in pergunta_lower:
            self.exibir_mensagem("AGI: Por favor, digite a fórmula em LaTeX (ex: E=mc^2):")
            self.master.after(100, self.obter_formula)
            return ""

        # Verificar se a pergunta é para gerar código Python
        for comando in solicitar_codigo:
            if comando in pergunta_lower:
                self.exibir_mensagem("AGI: Claro! Qual código Python você gostaria de ver? (Ex: jogo de xadrez)")
                self.master.after(100, self.obter_codigo_requisitado)
                return ""

        return None  # Nenhuma resposta personalizada encontrada

    def responder_saudações(self, saudacao):
        respostas = {
            'oi': 'Oi! Como posso ajudar você hoje?',
            'ola': 'Olá! Tudo bem?',
            'olá': 'Olá! Tudo bem?',
            'bom dia': 'Bom dia! Como posso ajudar você?',
            'boa tarde': 'Boa tarde! Em que posso ajudar?',
            'boa noite': 'Boa noite! Como posso ajudar você?'
        }
        return respostas.get(saudacao, 'Olá! Como posso ajudar você hoje?')

    def responder_despedidas(self, despedida):
        respostas = {
            'tchau': 'Tchau! Foi um prazer ajudar você.',
            'até mais': 'Até mais! Volte sempre.',
            'até logo': 'Até logo! Se precisar de mais ajuda, estarei aqui.',
            'adeus': 'Adeus! Foi bom conversar com você.'
        }
        return respostas.get(despedida, 'Até mais! Foi um prazer ajudar você.')

    def obter_equacao_diferencial(self):
        def confirmar():
            expressao = entrada.get().strip()
            if not expressao:
                messagebox.showwarning("Entrada Vazia", "Por favor, insira uma equação diferencial.")
                return
            solucao = resolver_equacao(expressao)
            self.exibir_mensagem(f"AGI: Solução: {solucao}")
            janela.destroy()

        janela = tk.Toplevel(self.master)
        janela.title("Resolver Equação Diferencial")
        janela.geometry("500x150")
        tk.Label(janela, text="Digite a equação diferencial:", font=("Arial", 12)).pack(pady=10)
        entrada = tk.Entry(janela, width=50, font=("Arial", 12))
        entrada.pack(pady=5)
        tk.Button(janela, text="Resolver", command=confirmar, font=("Arial", 12)).pack(pady=10)

    def obter_integral(self):
        def confirmar():
            expressao = entrada.get().strip()
            if not expressao:
                messagebox.showwarning("Entrada Vazia", "Por favor, insira uma expressão para integrar.")
                return
            solucao = integrar(expressao)
            self.exibir_mensagem(f"AGI: Integral: {solucao}")
            janela.destroy()

        janela = tk.Toplevel(self.master)
        janela.title("Integrar Expressão")
        janela.geometry("500x150")
        tk.Label(janela, text="Digite a expressão para integrar:", font=("Arial", 12)).pack(pady=10)
        entrada = tk.Entry(janela, width=50, font=("Arial", 12))
        entrada.pack(pady=5)
        tk.Button(janela, text="Integrar", command=confirmar, font=("Arial", 12)).pack(pady=10)

    def obter_formula(self):
        def confirmar():
            formula = entrada.get().strip()
            if not formula:
                messagebox.showwarning("Entrada Vazia", "Por favor, insira uma fórmula em LaTeX.")
                return
            self.exibir_mensagem("AGI: Renderizando a fórmula...")
            img = renderizar_formula(formula)
            if isinstance(img, Image.Image):
                img = img.resize((400, 150), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(img)
                self.image_label.config(image=photo)
                self.image_label.image = photo
                janela.destroy()
            else:
                self.exibir_mensagem(f"AGI: {img}")
                janela.destroy()

        janela = tk.Toplevel(self.master)
        janela.title("Renderizar Fórmula")
        janela.geometry("500x300")
        tk.Label(janela, text="Digite a fórmula em LaTeX:", font=("Arial", 12)).pack(pady=10)
        entrada = tk.Entry(janela, width=50, font=("Arial", 12))
        entrada.pack(pady=5)
        tk.Button(janela, text="Renderizar", command=confirmar, font=("Arial", 12)).pack(pady=10)

        # Label para exibir a imagem da fórmula
        self.image_label = tk.Label(janela)
        self.image_label.pack(pady=10)

    def obter_codigo_requisitado(self):
        def confirmar():
            codigo_requisitado = entrada.get().strip().lower()
            if not codigo_requisitado:
                messagebox.showwarning("Entrada Vazia", "Por favor, insira o nome do código que deseja ver.")
                return
            codigo = self.obter_codigo_python(codigo_requisitado)
            if codigo:
                self.exibir_mensagem(f"AGI: Aqui está o código solicitado:\n```python\n{codigo}\n```")
            else:
                self.exibir_mensagem(f"AGI: Desculpe, não tenho um código para '{codigo_requisitado}'.")
            janela.destroy()

        janela = tk.Toplevel(self.master)
        janela.title("Selecionar Código Python")
        janela.geometry("500x150")
        tk.Label(janela, text="Digite o nome do código Python que deseja ver:", font=("Arial", 12)).pack(pady=10)
        entrada = tk.Entry(janela, width=50, font=("Arial", 12))
        entrada.pack(pady=5)
        tk.Button(janela, text="Mostrar Código", command=confirmar, font=("Arial", 12)).pack(pady=10)

    def obter_codigo_python(self, codigo_requisitado):
        """
        Retorna o código Python solicitado com base na requisição do usuário.
        Atualmente, suporta a geração do jogo de xadrez.
        """
        if 'jogo de xadrez' in codigo_requisitado:
            return JOGO_XADREZ_CODIGO.strip()
        # Aqui você pode adicionar mais condições para outros códigos Python
        # Exemplo:
        # elif 'jogo da velha' in codigo_requisitado:
        #     return JOGO_DA_VELHA_CODIGO.strip()
        return None

def main():
    root = tk.Tk()
    chatbot = ChatbotAGI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
