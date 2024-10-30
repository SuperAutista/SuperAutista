import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import random

# Inicialização do Pygame
pygame.init()

# Configurações da Tela
LARGURA_TELA = 800
ALTURA_TELA = 600
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Jogo de Tênis de Mesa 3D")

# Configurações de OpenGL
gluPerspective(45, (LARGURA_TELA / ALTURA_TELA), 0.1, 100.0)
glTranslatef(0.0, 0.0, -50)

# Cores
BRANCO = (1, 1, 1)
PRETO = (0, 0, 0)
VERDE = (0, 1, 0)
VERMELHO = (1, 0, 0)

# Frames por Segundo
FPS = 60
RELOGIO = pygame.time.Clock()

# Classe Mesa
class Mesa:
    def __init__(self):
        self.largura = 40
        self.profundidade = 20
        self.altura = 1
        self.rede_altura = 5
        self.rede_largura = self.largura
        self.rede_profundidade = self.altura

    def desenhar(self):
        # Desenha a mesa
        glColor3fv(VERDE)
        glBegin(GL_QUADS)
        # Frontal
        glVertex3f(-self.largura / 2, 0, -self.profundidade / 2)
        glVertex3f(self.largura / 2, 0, -self.profundidade / 2)
        glVertex3f(self.largura / 2, 0, self.profundidade / 2)
        glVertex3f(-self.largura / 2, 0, self.profundidade / 2)
        glEnd()

        # Desenha as laterais da mesa
        glColor3fv(PRETO)
        glBegin(GL_LINES)
        # Linhas laterais
        glVertex3f(-self.largura / 2, 0, -self.profundidade / 2)
        glVertex3f(-self.largura / 2, 0, self.profundidade / 2)

        glVertex3f(self.largura / 2, 0, -self.profundidade / 2)
        glVertex3f(self.largura / 2, 0, self.profundidade / 2)
        glEnd()

        # Desenha a rede
        glColor3fv(PRETO)
        glBegin(GL_QUADS)
        glVertex3f(-self.largura / 2, self.rede_altura, 0 - self.rede_profundidade / 2)
        glVertex3f(self.largura / 2, self.rede_altura, 0 - self.rede_profundidade / 2)
        glVertex3f(self.largura / 2, self.rede_altura, 0 + self.rede_profundidade / 2)
        glVertex3f(-self.largura / 2, self.rede_altura, 0 + self.rede_profundidade / 2)
        glEnd()

# Classe Raquete
class Raquete:
    def __init__(self, lado, cor):
        self.largura = 2
        self.altura = 10
        self.profundidade = 2
        self.lado = lado  # 'esquerdo' ou 'direito'
        self.cor = cor
        self.velocidade = 1
        if lado == 'esquerdo':
            self.x = -19
        else:
            self.x = 19
        self.y = 0
        self.z = 0

    def mover_cima(self):
        if self.z < 9:
            self.z += self.velocidade

    def mover_baixo(self):
        if self.z > -9:
            self.z -= self.velocidade

    def desenhar(self):
        glColor3fv(self.cor)
        glPushMatrix()
        glTranslatef(self.x, self.altura / 2, self.z)
        glScalef(self.largura, self.altura, self.profundidade)
        self.cubo()
        glPopMatrix()

    def cubo(self):
        vertices = [
            [1, 1, -1],
            [1, -1, -1],
            [-1, -1, -1],
            [-1, 1, -1],
            [1, 1, 1],
            [1, -1, 1],
            [-1, -1, 1],
            [-1, 1, 1]
        ]

        edges = (
            (0,1),
            (1,2),
            (2,3),
            (3,0),
            (4,5),
            (5,6),
            (6,7),
            (7,4),
            (0,4),
            (1,5),
            (2,6),
            (3,7)
        )

        glBegin(GL_QUADS)
        # Frente
        glVertex3fv(vertices[4])
        glVertex3fv(vertices[5])
        glVertex3fv(vertices[6])
        glVertex3fv(vertices[7])
        # Trás
        glVertex3fv(vertices[0])
        glVertex3fv(vertices[1])
        glVertex3fv(vertices[2])
        glVertex3fv(vertices[3])
        # Cima
        glVertex3fv(vertices[0])
        glVertex3fv(vertices[4])
        glVertex3fv(vertices[7])
        glVertex3fv(vertices[3])
        # Baixo
        glVertex3fv(vertices[1])
        glVertex3fv(vertices[5])
        glVertex3fv(vertices[6])
        glVertex3fv(vertices[2])
        # Direita
        glVertex3fv(vertices[0])
        glVertex3fv(vertices[1])
        glVertex3fv(vertices[5])
        glVertex3fv(vertices[4])
        # Esquerda
        glVertex3fv(vertices[3])
        glVertex3fv(vertices[2])
        glVertex3fv(vertices[6])
        glVertex3fv(vertices[7])
        glEnd()

# Classe Bolinha
class Bolinha:
    def __init__(self):
        self.raio = 1
        self.x = 0
        self.y = 1  # altura da mesa
        self.z = 0
        self.velocidade_x = random.choice([-0.5, 0.5])
        self.velocidade_z = random.choice([-0.5, 0.5])

    def mover(self):
        self.x += self.velocidade_x
        self.z += self.velocidade_z

        # Limites da mesa
        if self.x > 20 or self.x < -20:
            self.resetar()
        if self.z > 10 or self.z < -10:
            self.velocidade_z *= -1

    def desenhar(self):
        glColor3fv(PRETO)
        glPushMatrix()
        glTranslatef(self.x, self.y + self.raio, self.z)
        glutSolidSphere(self.raio, 20, 20)
        glPopMatrix()

    def resetar(self):
        self.x = 0
        self.z = 0
        self.velocidade_x = random.choice([-0.5, 0.5])
        self.velocidade_z = random.choice([-0.5, 0.5])

    def verificar_colisao(self, raquete_esquerda, raquete_direita):
        # Colisão com a raquete esquerda
        if (self.x - self.raio <= raquete_esquerda.x + 1 and
            raquete_esquerda.z - raquete_esquerda.altura / 2 <= self.z <= raquete_esquerda.z + raquete_esquerda.altura / 2):
            self.velocidade_x *= -1

        # Colisão com a raquete direita
        if (self.x + self.raio >= raquete_direita.x - 1 and
            raquete_direita.z - raquete_direita.altura / 2 <= self.z <= raquete_direita.z + raquete_direita.altura / 2):
            self.velocidade_x *= -1

# Inicialização dos Elementos do Jogo
mesa = Mesa()
raquete_esquerda = Raquete('esquerdo', VERMELHO)
raquete_direita = Raquete('direito', PRETO)
bolinha = Bolinha()

# Função para desenhar texto (opcional, requer configuração adicional)
def desenhar_texto():
    pass  # Implementar se desejar exibir pontuação ou outros textos

# Loop Principal do Jogo
executando = True
while executando:
    RELOGIO.tick(FPS)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

    # Captura de Teclas Pressionadas
    teclas_pressionadas = pygame.key.get_pressed()

    # Movimentação da Raquete Esquerda (Jogador)
    if teclas_pressionadas[pygame.K_w]:
        raquete_esquerda.mover_cima()
    if teclas_pressionadas[pygame.K_s]:
        raquete_esquerda.mover_baixo()

    # Movimentação da Raquete Direita (IA Simples)
    if bolinha.z < raquete_direita.z and raquete_direita.z > -9:
        raquete_direita.z -= raquete_direita.velocidade
    elif bolinha.z > raquete_direita.z and raquete_direita.z < 9:
        raquete_direita.z += raquete_direita.velocidade

    # Movimentação da Bolinha
    bolinha.mover()

    # Verificar Colisões
    bolinha.verificar_colisao(raquete_esquerda, raquete_direita)

    # Desenhar Tudo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    mesa.desenhar()
    raquete_esquerda.desenhar()
    raquete_direita.desenhar()
    bolinha.desenhar()
    desenhar_texto()

    # Atualizar a Tela
    pygame.display.flip()

# Encerrar o Pygame
pygame.quit()
sys.exit()
