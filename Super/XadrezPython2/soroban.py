import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da Tela
LARGURA_TELA = 1600
ALTURA_TELA = 600
TITULO = "Simulador de Soroban"
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption(TITULO)

# Cores
COR_FUNDO = (240, 230, 214)
COR_TRAVE = (139, 69, 19)
COR_COLUNA = (198, 156, 109)
COR_BOLINHA = (45, 106, 79)

# Parâmetros do Soroban
NUM_COLUNAS = 13
LARGURA_COLUNA = 70
ALTURA_COLUNA = 400
ESPACAMENTO_COLUNAS = 10
ESPACAMENTO_BOLINHAS = 15
TAMANHO_BOLINHA = 40
POSICAO_TRAVE_Y = 200

# Classe para Bolinha
class Bolinha:
    def __init__(self, x, y, tipo, coluna):
        self.x = x
        self.y = y
        self.raio = TAMANHO_BOLINHA // 2
        self.tipo = tipo  # 'superior' ou 'inferior'
        self.coluna = coluna
        self.posicao = 'up' if tipo == 'superior' else 'down'
        # Posições possíveis
        if self.tipo == 'superior':
            self.posicoes = {'up': self.y, 'down': POSICAO_TRAVE_Y - ESPACAMENTO_BOLINHAS - TAMANHO_BOLINHA}
        else:
            self.posicoes = {'up': self.y - TAMANHO_BOLINHA - ESPACAMENTO_BOLINHAS, 'down': self.y}
        self.atualizar_posicao()

    def desenhar(self, tela):
        pygame.draw.circle(tela, COR_BOLINHA, (self.x, self.y_atual), self.raio)

    def atualizar_posicao(self):
        self.y_atual = self.posicoes[self.posicao]

    def clicar(self, pos_mouse):
        distancia = ((self.x - pos_mouse[0]) ** 2 + (self.y_atual - pos_mouse[1]) ** 2) ** 0.5
        return distancia <= self.raio

    def alternar_posicao(self):
        self.posicao = 'down' if self.posicao == 'up' else 'up'
        self.atualizar_posicao()

# Classe para Coluna
class Coluna:
    def __init__(self, indice, x):
        self.indice = indice
        self.x = x
        self.y = (ALTURA_TELA - ALTURA_COLUNA) // 2
        self.bolinhas = []
        self.criar_bolinhas()

    def criar_bolinhas(self):
        # Bolinha superior (valor 5)
        bolinha_sup = Bolinha(self.x + LARGURA_COLUNA // 2, self.y + POSICAO_TRAVE_Y - TAMANHO_BOLINHA - ESPACAMENTO_BOLINHAS, 'superior', self)
        self.bolinhas.append(bolinha_sup)

        # Bolinhas inferiores (valem 1 cada)
        for j in range(4):
            y_inicial = self.y + POSICAO_TRAVE_Y + ESPACAMENTO_BOLINHAS + j * (TAMANHO_BOLINHA + ESPACAMENTO_BOLINHAS)
            bolinha_inf = Bolinha(self.x + LARGURA_COLUNA // 2, y_inicial, 'inferior', self)
            self.bolinhas.append(bolinha_inf)

    def desenhar(self, tela):
        # Desenhar coluna
        pygame.draw.rect(tela, COR_COLUNA, (self.x, self.y, LARGURA_COLUNA, ALTURA_COLUNA))

        # Desenhar trave
        pygame.draw.rect(tela, COR_TRAVE, (self.x, self.y + POSICAO_TRAVE_Y, LARGURA_COLUNA, 15))

        # Desenhar bolinhas
        for bolinha in self.bolinhas:
            bolinha.desenhar(tela)

    def verificar_clique(self, pos_mouse):
        for bolinha in self.bolinhas:
            if bolinha.clicar(pos_mouse):
                bolinha.alternar_posicao()
                return True
        return False

    def obter_valor_coluna(self):
        valor_coluna = 0
        # Bolinha superior (vale 5 se está em 'down')
        if self.bolinhas[0].posicao == 'down':
            valor_coluna += 5
        # Bolinhas inferiores (valem 1 cada quando em 'up')
        for bolinha_inf in self.bolinhas[1:]:
            if bolinha_inf.posicao == 'up':
                valor_coluna += 1
        return valor_coluna * (10 ** (NUM_COLUNAS - self.indice - 1))

# Classe para Soroban
class Soroban:
    def __init__(self):
        self.colunas = []
        self.criar_colunas()

    def criar_colunas(self):
        inicio_x = 50
        for i in range(NUM_COLUNAS):
            x = inicio_x + i * (LARGURA_COLUNA + ESPACAMENTO_COLUNAS)
            coluna = Coluna(i, x)
            self.colunas.append(coluna)

    def desenhar(self, tela):
        for coluna in self.colunas:
            coluna.desenhar(tela)

    def verificar_clique(self, pos_mouse):
        for coluna in self.colunas:
            if coluna.verificar_clique(pos_mouse):
                return True
        return False

    def calcular_valor_total(self):
        total = 0
        for coluna in self.colunas:
            total += coluna.obter_valor_coluna()
        return total

# Função principal
def main():
    soroban = Soroban()
    clock = pygame.time.Clock()
    executando = True

    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_mouse = pygame.mouse.get_pos()
                soroban.verificar_clique(pos_mouse)

        # Preencher a tela
        tela.fill(COR_FUNDO)

        # Desenhar o soroban
        soroban.desenhar(tela)

        # Atualizar a tela
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
