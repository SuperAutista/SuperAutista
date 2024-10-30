import pygame
import sys
import math
import copy
import time

# Inicialização do Pygame
pygame.init()

# Configurações da janela
TAMANHO_JANELA = 800
TAMANHO_TABULEIRO = 19
TAMANHO_CELULA = TAMANHO_JANELA // TAMANHO_TABULEIRO
MARGEM = 40  # Margem para um design mais estilizado

# Cores Futuristas
CINZA_FUNDO = (30, 30, 30)
LINHA_TABULEIRO = (50, 50, 50)
PONTOS_REFERENCIA = (100, 100, 100)
PECA_PRETA = (0, 0, 0)
PECA_BRANCA = (255, 255, 255)
EFEITO_LUZ = (0, 255, 255)
TEXTURA_TABULEIRO = (70, 130, 180)  # Azul Steel

# Fonte para mensagens
FONTE = pygame.font.SysFont(None, 24)

# Configura a janela
tela = pygame.display.set_mode((TAMANHO_JANELA + MARGEM * 2, TAMANHO_JANELA + MARGEM * 2))
pygame.display.set_caption("Jogo de Go - Estilo Futurista")

# Clock para controlar FPS
clock = pygame.time.Clock()

# Estado inicial do tabuleiro (0 = vazio, 1 = branca, 2 = preta)
tabuleiro_inicial = [[0 for _ in range(TAMANHO_TABULEIRO)] for _ in range(TAMANHO_TABULEIRO)]


def desenhar_tabuleiro(tabuleiro):
    tela.fill(CINZA_FUNDO)

    # Desenhar linhas do tabuleiro
    for i in range(TAMANHO_TABULEIRO):
        # Linhas horizontais
        pygame.draw.line(tela, LINHA_TABULEIRO,
                         (MARGEM, MARGEM + i * TAMANHO_CELULA),
                         (MARGEM + (TAMANHO_TABULEIRO - 1) * TAMANHO_CELULA, MARGEM + i * TAMANHO_CELULA), 2)
        # Linhas verticais
        pygame.draw.line(tela, LINHA_TABULEIRO,
                         (MARGEM + i * TAMANHO_CELULA, MARGEM),
                         (MARGEM + i * TAMANHO_CELULA, MARGEM + (TAMANHO_TABULEIRO - 1) * TAMANHO_CELULA), 2)

    # Desenhar pontos de referência (hoshi)
    pontos = [3, 9, 15]
    for i in pontos:
        for j in pontos:
            centro = (MARGEM + i * TAMANHO_CELULA, MARGEM + j * TAMANHO_CELULA)
            pygame.draw.circle(tela, PONTOS_REFERENCIA, centro, 5)

    # Desenhar peças
    for linha in range(TAMANHO_TABULEIRO):
        for coluna in range(TAMANHO_TABULEIRO):
            if tabuleiro[linha][coluna] != 0:
                cor = PECA_BRANCA if tabuleiro[linha][coluna] == 1 else PECA_PRETA
                pos = (MARGEM + coluna * TAMANHO_CELULA, MARGEM + linha * TAMANHO_CELULA)
                pygame.draw.circle(tela, cor, pos, TAMANHO_CELULA // 2 - 4)
                # Efeito de luz
                pygame.draw.circle(tela, EFEITO_LUZ, pos, TAMANHO_CELULA // 2 - 8, 2)


def get_vizinhos(linha, coluna):
    vizinhos = []
    if linha > 0:
        vizinhos.append((linha - 1, coluna))
    if linha < TAMANHO_TABULEIRO - 1:
        vizinhos.append((linha + 1, coluna))
    if coluna > 0:
        vizinhos.append((linha, coluna - 1))
    if coluna < TAMANHO_TABULEIRO - 1:
        vizinhos.append((linha, coluna + 1))
    return vizinhos


def obter_grupo(tabuleiro, linha, coluna, visitados=None):
    if visitados is None:
        visitados = set()
    cor = tabuleiro[linha][coluna]
    grupo = set()
    grupo.add((linha, coluna))
    visitados.add((linha, coluna))
    for viz in get_vizinhos(linha, coluna):
        if tabuleiro[viz[0]][viz[1]] == cor and viz not in visitados:
            grupo |= obter_grupo(tabuleiro, viz[0], viz[1], visitados)
    return grupo


def tem_liberdades(tabuleiro, grupo):
    for (linha, coluna) in grupo:
        for viz in get_vizinhos(linha, coluna):
            if tabuleiro[viz[0]][viz[1]] == 0:
                return True
    return False


def remover_grupos_sem_liberdade(tabuleiro, cor):
    removidos = []
    for linha in range(TAMANHO_TABULEIRO):
        for coluna in range(TAMANHO_TABULEIRO):
            if tabuleiro[linha][coluna] == cor:
                grupo = obter_grupo(tabuleiro, linha, coluna)
                if not tem_liberdades(tabuleiro, grupo):
                    removidos.append(grupo)
    for grupo in removidos:
        for (linha, coluna) in grupo:
            tabuleiro[linha][coluna] = 0
    return len(removidos) > 0


def jogada_valida(tabuleiro, linha, coluna, cor):
    if tabuleiro[linha][coluna] != 0:
        return False
    temp_tabuleiro = copy.deepcopy(tabuleiro)
    temp_tabuleiro[linha][coluna] = cor
    # Remover grupos do adversário
    adversario = 1 if cor == 2 else 2
    remover_grupos_sem_liberdade(temp_tabuleiro, adversario)
    # Verificar se a própria jogada não captura sem ter liberdades
    grupo = obter_grupo(temp_tabuleiro, linha, coluna)
    if not tem_liberdades(temp_tabuleiro, grupo):
        return False
    # Implementar regra de Ko poderia ser adicionado aqui
    return True


def obter_movimentos_validos(tabuleiro, cor):
    movimentos = []
    for linha in range(TAMANHO_TABULEIRO):
        for coluna in range(TAMANHO_TABULEIRO):
            if jogada_valida(tabuleiro, linha, coluna, cor):
                movimentos.append((linha, coluna))
    return movimentos


def avaliar_tabuleiro(tabuleiro):
    # Avaliação simples: diferença entre peças
    brancas = sum(row.count(1) for row in tabuleiro)
    pretas = sum(row.count(2) for row in tabuleiro)
    return brancas - pretas


def minimax(tabuleiro, profundidade, maximizando, cor_atual, alpha=-math.inf, beta=math.inf):
    if profundidade == 0:
        return avaliar_tabuleiro(tabuleiro), None
    movimentos = obter_movimentos_validos(tabuleiro, cor_atual)
    if not movimentos:
        return avaliar_tabuleiro(tabuleiro), None

    melhor_mov = None
    if maximizando:
        max_eval = -math.inf
        for mov in movimentos:
            temp_tabuleiro = copy.deepcopy(tabuleiro)
            temp_tabuleiro[mov[0]][mov[1]] = cor_atual
            remover_grupos_sem_liberdade(temp_tabuleiro, 1 if cor_atual == 2 else 2)
            eval, _ = minimax(temp_tabuleiro, profundidade - 1, False, 1 if cor_atual == 2 else 2, alpha, beta)
            if eval > max_eval:
                max_eval = eval
                melhor_mov = mov
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, melhor_mov
    else:
        min_eval = math.inf
        for mov in movimentos:
            temp_tabuleiro = copy.deepcopy(tabuleiro)
            temp_tabuleiro[mov[0]][mov[1]] = cor_atual
            remover_grupos_sem_liberdade(temp_tabuleiro, 1 if cor_atual == 2 else 2)
            eval, _ = minimax(temp_tabuleiro, profundidade - 1, True, 1 if cor_atual == 2 else 2, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                melhor_mov = mov
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, melhor_mov


def ia_jogada(tabuleiro):
    # Profundidade ajustada para equilíbrio entre desempenho e inteligência
    profundidade = 2
    _, mov = minimax(tabuleiro, profundidade, True, 1)  # 1 = IA (Brancas)
    return mov


def exibir_mensagem(mensagem, pos):
    texto = FONTE.render(mensagem, True, EFEITO_LUZ)
    tela.blit(texto, pos)


def main():
    tabuleiro = copy.deepcopy(tabuleiro_inicial)
    rodando = True
    turno = 2  # 1 = Brancas (IA), 2 = Pretas (Humano)
    ultima_jogada = None
    vencedor = None

    while rodando:
        desenhar_tabuleiro(tabuleiro)

        # Exibir mensagens de status
        if vencedor:
            exibir_mensagem(f"Vencedor: {'Brancas (IA)' if vencedor == 1 else 'Pretas (Humano)'}",
                            (MARGEM, TAMANHO_JANELA + MARGEM + 10))
        else:
            exibir_mensagem(f"Turno: {'Brancas (IA)' if turno == 1 else 'Pretas (Humano)'}",
                            (MARGEM, TAMANHO_JANELA + MARGEM + 10))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and turno == 2 and not vencedor:
                x, y = pygame.mouse.get_pos()
                # Converter posição do mouse para coordenadas do tabuleiro
                coluna = round((x - MARGEM) / TAMANHO_CELULA)
                linha = round((y - MARGEM) / TAMANHO_CELULA)
                if 0 <= linha < TAMANHO_TABULEIRO and 0 <= coluna < TAMANHO_TABULEIRO:
                    if jogada_valida(tabuleiro, linha, coluna, 2):
                        tabuleiro[linha][coluna] = 2
                        remover_grupos_sem_liberdade(tabuleiro, 1)
                        turno = 1  # Passa para a IA
                        ultima_jogada = (linha, coluna)
                        # Verificação simples de vitória (pode ser melhorada)
                        # Aqui poderia ser implementada a contagem de território
                        # ou outra lógica de término de jogo

        if turno == 1 and not vencedor:
            pygame.time.delay(300)  # Pequena pausa para a IA
            mov = ia_jogada(tabuleiro)
            if mov:
                tabuleiro[mov[0]][mov[1]] = 1
                remover_grupos_sem_liberdade(tabuleiro, 2)
                ultima_jogada = mov
            turno = 2  # Passa para o humano
            # Verificação simples de vitória (pode ser melhorada)

        clock.tick(60)


if __name__ == "__main__":
    main()
