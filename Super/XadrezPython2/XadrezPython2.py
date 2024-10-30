import pygame
import sys
import copy

# Inicialização do Pygame
pygame.init()

# Dimensões da janela
LARGURA_TABULEIRO = 640
ALTURA_TABULEIRO = 640
LARGURA_JANELA = 1000  # Aumentada para acomodar a área de informações
ALTURA_JANELA = 640
TAMANHO_QUADRADO = LARGURA_TABULEIRO // 8

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
CINZA = (128, 128, 128)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)
AZUL_LEGENDA = (0, 0, 255)

# Criação da janela
tela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
pygame.display.set_caption('Jogo de Xadrez do Tiago ')

# Fonte para desenhar as peças e textos
pygame.font.init()

# Tentativa de carregar uma fonte que suporte os símbolos de xadrez
fontes_disponiveis = ['Segoe UI Symbol', 'Arial Unicode MS', 'DejaVu Sans', 'FreeSerif', 'Symbola']
for nome_fonte in fontes_disponiveis:
    try:
        FONTE_PECA = pygame.font.SysFont(nome_fonte, TAMANHO_QUADRADO - 10)
        # Teste se a fonte suporta os caracteres de xadrez
        teste_texto = FONTE_PECA.render('\u2654', True, PRETO)
        if teste_texto:
            break
    except:
        continue
else:
    print("Nenhuma fonte adequada encontrada. Certifique-se de ter uma fonte que suporte os símbolos Unicode de xadrez.")
    pygame.quit()
    sys.exit()

# Fontes adicionais para a área de informações e legenda
FONTE_INFO = pygame.font.SysFont(None, 24)
FONTE_LEGENDA = pygame.font.SysFont(None, 30)

# Mapeamento dos símbolos Unicode das peças
SIMBOLOS_PECAS = {
    'rei_azul': '\u2654',     # ♔
    'rainha_azul': '\u2655',  # ♕
    'torre_azul': '\u2656',   # ♖
    'bispo_azul': '\u2657',   # ♗
    'cavalo_azul': '\u2658',  # ♘
    'peao_azul': '\u2659',    # ♙
    'rei_vermelho': '\u265A',     # ♚
    'rainha_vermelho': '\u265B',  # ♛
    'torre_vermelho': '\u265C',   # ♜
    'bispo_vermelho': '\u265D',   # ♝
    'cavalo_vermelho': '\u265E',  # ♞
    'peao_vermelho': '\u265F',    # ♟
}

# Classe para representar uma peça
class Peca:
    def __init__(self, tipo, cor):
        self.tipo = tipo  # 'rei', 'rainha', 'bispo', 'cavalo', 'torre', 'peao'
        self.cor = cor    # 'azul' ou 'vermelho'
        self.simbolo = SIMBOLOS_PECAS[f'{tipo}_{cor}']
        self.movimentos_realizados = 0  # Para roque e en passant

    def movimentos_validos(self, x, y, tabuleiro, roque_disponivel):
        movimentos = []
        direcoes = []

        if self.tipo == 'peao':
            direcao = -1 if self.cor == 'azul' else 1
            # Movimento simples
            novo_y = y + direcao
            if 0 <= novo_y < 8:
                if tabuleiro[novo_y][x] is None:
                    movimentos.append((x, novo_y))
                    # Movimento duplo no primeiro movimento
                    if (self.cor == 'azul' and y == 6) or (self.cor == 'vermelho' and y == 1):
                        novo_y2 = y + 2 * direcao
                        if 0 <= novo_y2 < 8 and tabuleiro[novo_y2][x] is None:
                            movimentos.append((x, novo_y2))
                # Captura diagonal
                for dx in [-1, 1]:
                    novo_x = x + dx
                    if 0 <= novo_x < 8:
                        peca_destino = tabuleiro[novo_y][novo_x]
                        if peca_destino and peca_destino.cor != self.cor:
                            movimentos.append((novo_x, novo_y))
                        # En Passant
                        elif peca_destino is None:
                            # Implementação simplificada, pode ser expandida com histórico de movimentos
                            pass
        elif self.tipo == 'torre':
            # Movimentos horizontais e verticais
            direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in direcoes:
                nx, ny = x + dx, y + dy
                while 0 <= nx < 8 and 0 <= ny < 8:
                    peca_destino = tabuleiro[ny][nx]
                    if peca_destino is None:
                        movimentos.append((nx, ny))
                    elif peca_destino.cor != self.cor:
                        movimentos.append((nx, ny))
                        break
                    else:
                        break
                    nx += dx
                    ny += dy
            # Roque
            if self.movimentos_realizados == 0:
                # Implementar condições de roque
                pass
        elif self.tipo == 'bispo':
            # Movimentos diagonais
            direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dx, dy in direcoes:
                nx, ny = x + dx, y + dy
                while 0 <= nx < 8 and 0 <= ny < 8:
                    peca_destino = tabuleiro[ny][nx]
                    if peca_destino is None:
                        movimentos.append((nx, ny))
                    elif peca_destino.cor != self.cor:
                        movimentos.append((nx, ny))
                        break
                    else:
                        break
                    nx += dx
                    ny += dy
        elif self.tipo == 'rainha':
            # Combinação de torre e bispo
            direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1),
                        (-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dx, dy in direcoes:
                nx, ny = x + dx, y + dy
                while 0 <= nx < 8 and 0 <= ny < 8:
                    peca_destino = tabuleiro[ny][nx]
                    if peca_destino is None:
                        movimentos.append((nx, ny))
                    elif peca_destino.cor != self.cor:
                        movimentos.append((nx, ny))
                        break
                    else:
                        break
                    nx += dx
                    ny += dy
        elif self.tipo == 'rei':
            # Movimentos para todas as direções, mas apenas uma casa
            direcoes = [(-1, -1), (-1, 0), (-1, 1),
                        (0, -1),         (0, 1),
                        (1, -1),  (1, 0),  (1, 1)]
            for dx, dy in direcoes:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    peca_destino = tabuleiro[ny][nx]
                    if peca_destino is None or peca_destino.cor != self.cor:
                        movimentos.append((nx, ny))
            # Roque
            if self.movimentos_realizados == 0:
                # Implementar condições de roque
                pass
        elif self.tipo == 'cavalo':
            # Movimentos em 'L'
            movimentos_cavalo = [
                (x + 1, y + 2), (x + 1, y - 2),
                (x - 1, y + 2), (x - 1, y - 2),
                (x + 2, y + 1), (x + 2, y - 1),
                (x - 2, y + 1), (x - 2, y - 1)
            ]
            for nx, ny in movimentos_cavalo:
                if 0 <= nx < 8 and 0 <= ny < 8:
                    peca_destino = tabuleiro[ny][nx]
                    if peca_destino is None or peca_destino.cor != self.cor:
                        movimentos.append((nx, ny))
        return movimentos

# Classe para representar o estado do jogo
class Jogo:
    def __init__(self):
        self.tabuleiro = [[None for _ in range(8)] for _ in range(8)]
        self.jogador_atual = 'azul'
        self.historico = []  # Lista para armazenar o histórico de movimentos
        self.roque_disponivel = {
            'azul': {'roque_menos': True, 'roque_mais': True},
            'vermelho': {'roque_menos': True, 'roque_mais': True}
        }
        self.iniciar_tabuleiro()

    def iniciar_tabuleiro(self):
        # Peças azuis (jogador humano)
        self.tabuleiro[6] = [Peca('peao', 'azul') for _ in range(8)]
        self.tabuleiro[7][0] = Peca('torre', 'azul')
        self.tabuleiro[7][1] = Peca('cavalo', 'azul')
        self.tabuleiro[7][2] = Peca('bispo', 'azul')
        self.tabuleiro[7][3] = Peca('rainha', 'azul')
        self.tabuleiro[7][4] = Peca('rei', 'azul')
        self.tabuleiro[7][5] = Peca('bispo', 'azul')
        self.tabuleiro[7][6] = Peca('cavalo', 'azul')
        self.tabuleiro[7][7] = Peca('torre', 'azul')

        # Peças vermelhas (IA)
        self.tabuleiro[1] = [Peca('peao', 'vermelho') for _ in range(8)]
        self.tabuleiro[0][0] = Peca('torre', 'vermelho')
        self.tabuleiro[0][1] = Peca('cavalo', 'vermelho')
        self.tabuleiro[0][2] = Peca('bispo', 'vermelho')
        self.tabuleiro[0][3] = Peca('rainha', 'vermelho')
        self.tabuleiro[0][4] = Peca('rei', 'vermelho')
        self.tabuleiro[0][5] = Peca('bispo', 'vermelho')
        self.tabuleiro[0][6] = Peca('cavalo', 'vermelho')
        self.tabuleiro[0][7] = Peca('torre', 'vermelho')

    def desenhar_tabuleiro(self):
        # Desenhar o tabuleiro
        for y in range(8):
            for x in range(8):
                cor = BRANCO if (x + y) % 2 == 0 else CINZA
                pygame.draw.rect(tela, cor, (x * TAMANHO_QUADRADO, y * TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO))
                peca = self.tabuleiro[y][x]
                if peca:
                    # Desenhar o símbolo da peça
                    texto = FONTE_PECA.render(peca.simbolo, True, PRETO)
                    pos_texto = texto.get_rect(center=(x * TAMANHO_QUADRADO + TAMANHO_QUADRADO//2, y * TAMANHO_QUADRADO + TAMANHO_QUADRADO//2))
                    tela.blit(texto, pos_texto)

    def desenhar_info(self):
        # Desenhar a área de informações ao lado do tabuleiro
        # Desenhar uma linha vertical separando o tabuleiro da área de informações
        pygame.draw.line(tela, PRETO, (LARGURA_TABULEIRO, 0), (LARGURA_TABULEIRO, ALTURA_TABULEIRO), 2)

        # Título
        titulo = FONTE_INFO.render('Histórico de Movimentos:', True, PRETO)
        tela.blit(titulo, (LARGURA_TABULEIRO + 20, 10))

        # Exibir os movimentos
        y_offset = 40
        for index, movimento in enumerate(self.historico[-25:]):  # Exibir apenas os últimos 25 movimentos
            cor_jogador, descricao = movimento
            # Dividir a descrição em múltiplas linhas se necessário
            linhas = self.dividir_texto(descricao, 300, FONTE_INFO)
            for linha in linhas:
                texto = FONTE_INFO.render(linha, True, AZUL if cor_jogador == 'azul' else VERMELHO)
                tela.blit(texto, (LARGURA_TABULEIRO + 20, y_offset))
                y_offset += 20
                if y_offset > ALTURA_TABULEIRO - 60:
                    break  # Evita ultrapassar a área de informações

        # Legenda do Autor
        legenda = FONTE_LEGENDA.render('autor: Luiz Tiago Wilcke', True, AZUL_LEGENDA)
        tela.blit(legenda, (LARGURA_TABULEIRO + 20, ALTURA_TABULEIRO - 40))

    def dividir_texto(self, texto, largura_max, fonte):
        # Função para dividir o texto em múltiplas linhas
        palavras = texto.split(' ')
        linhas = []
        linha_atual = ""
        for palavra in palavras:
            teste_linha = linha_atual + palavra + " "
            largura, _ = fonte.size(teste_linha)
            if largura < largura_max:
                linha_atual = teste_linha
            else:
                linhas.append(linha_atual)
                linha_atual = palavra + " "
        if linha_atual:
            linhas.append(linha_atual)
        return linhas

    def mover_peca(self, origem, destino, is_ai_move=False, eval_score=None):
        x1, y1 = origem
        x2, y2 = destino
        peca = self.tabuleiro[y1][x1]
        destino_peca = self.tabuleiro[y2][x2]
        self.tabuleiro[y2][x2] = peca
        self.tabuleiro[y1][x1] = None
        peca.movimentos_realizados += 1

        # Promoção de peão
        if peca.tipo == 'peao' and (y2 == 0 or y2 == 7):
            self.promocao_peao(x2, y2, peca.cor)

        # Atualizar roque disponibilidade
        if peca.tipo == 'rei':
            self.roque_disponivel[peca.cor]['roque_mais'] = False
            self.roque_disponivel[peca.cor]['roque_menos'] = False
        if peca.tipo == 'torre':
            if x1 == 0:
                self.roque_disponivel[peca.cor]['roque_menos'] = False
            elif x1 == 7:
                self.roque_disponivel[peca.cor]['roque_mais'] = False

        # Adicionar movimento ao histórico
        if is_ai_move:
            descricao = f"IA move {peca.tipo.capitalize()} de ({x1},{y1}) para ({x2},{y2}) | Eval: {eval_score}"
            self.historico.append(('vermelho', descricao))
        else:
            descricao = f"Jogador move {peca.tipo.capitalize()} de ({x1},{y1}) para ({x2},{y2})"
            self.historico.append(('azul', descricao))

    def promocao_peao(self, x, y, cor):
        # Prompt para o jogador escolher a peça de promoção
        promovido = False
        while not promovido:
            tela.fill(BRANCO)
            fonte_promocao = pygame.font.SysFont(None, 40)
            texto = fonte_promocao.render('Escolha a peça para promoção (R, B, C, T):', True, PRETO)
            tela.blit(texto, (20, ALTURA_JANELA//2 - 50))
            pygame.display.flip()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r:
                        nova_peca = Peca('rainha', cor)
                        promovido = True
                    elif evento.key == pygame.K_b:
                        nova_peca = Peca('bispo', cor)
                        promovido = True
                    elif evento.key == pygame.K_c:
                        nova_peca = Peca('cavalo', cor)
                        promovido = True
                    elif evento.key == pygame.K_t:
                        nova_peca = Peca('torre', cor)
                        promovido = True
                    if promovido:
                        self.tabuleiro[y][x] = nova_peca

    def esta_em_xeque(self, cor):
        # Verifica se o rei da cor especificada está em xeque
        rei_pos = None
        for y in range(8):
            for x in range(8):
                peca = self.tabuleiro[y][x]
                if peca and peca.tipo == 'rei' and peca.cor == cor:
                    rei_pos = (x, y)
                    break
            if rei_pos:
                break

        if not rei_pos:
            return False  # Rei foi capturado

        # Verifica se alguma peça adversária pode capturar o rei
        cor_oponente = 'vermelho' if cor == 'azul' else 'azul'
        for y in range(8):
            for x in range(8):
                peca = self.tabuleiro[y][x]
                if peca and peca.cor == cor_oponente:
                    movimentos = peca.movimentos_validos(x, y, self.tabuleiro, self.roque_disponivel)
                    if rei_pos in movimentos:
                        return True
        return False

    def esta_em_xeque_mate(self, cor):
        if not self.esta_em_xeque(cor):
            return False
        # Verifica se há algum movimento que tira o rei do xeque
        movimentos = self.obter_movimentos_validos(cor)
        for movimento in movimentos:
            copia_jogo = copy.deepcopy(self)
            copia_jogo.mover_peca(*movimento)
            if not copia_jogo.esta_em_xeque(cor):
                return False
        return True

    def obter_movimentos_validos(self, cor):
        movimentos = []
        for y in range(8):
            for x in range(8):
                peca = self.tabuleiro[y][x]
                if peca and peca.cor == cor:
                    movimentos_possiveis = peca.movimentos_validos(x, y, self.tabuleiro, self.roque_disponivel)
                    for destino in movimentos_possiveis:
                        movimentos.append(((x, y), destino))
        # Filtrar movimentos que não deixam o rei em xeque
        movimentos_legais = []
        for origem, destino in movimentos:
            copia_jogo = copy.deepcopy(self)
            copia_jogo.mover_peca(origem, destino)
            if not copia_jogo.esta_em_xeque(cor):
                movimentos_legais.append((origem, destino))
        return movimentos_legais

    def avaliar_tabuleiro(self):
        # Função de avaliação para a IA
        valor = 0
        for y in range(8):
            for x in range(8):
                peca = self.tabuleiro[y][x]
                if peca:
                    if peca.cor == 'vermelho':
                        valor += self.valor_peca(peca)
                    else:
                        valor -= self.valor_peca(peca)
        return valor

    def valor_peca(self, peca):
        valores = {'peao': 10, 'cavalo': 30, 'bispo': 30, 'torre': 50, 'rainha': 90, 'rei': 900}
        return valores.get(peca.tipo, 0)

    def minimax(self, profundidade, maximizando, alpha=float('-inf'), beta=float('inf')):
        cor = 'vermelho' if maximizando else 'azul'
        if profundidade == 0 or self.esta_em_xeque_mate('azul') or self.esta_em_xeque_mate('vermelho'):
            return self.avaliar_tabuleiro(), None

        movimentos = self.obter_movimentos_validos(cor)
        if not movimentos:
            return self.avaliar_tabuleiro(), None

        melhor_movimento = None

        if maximizando:
            max_eval = float('-inf')
            for movimento in movimentos:
                copia_jogo = copy.deepcopy(self)
                copia_jogo.mover_peca(*movimento)
                eval_atual, _ = copia_jogo.minimax(profundidade - 1, False, alpha, beta)
                if eval_atual > max_eval:
                    max_eval = eval_atual
                    melhor_movimento = movimento
                alpha = max(alpha, eval_atual)
                if beta <= alpha:
                    break
            return max_eval, melhor_movimento
        else:
            min_eval = float('inf')
            for movimento in movimentos:
                copia_jogo = copy.deepcopy(self)
                copia_jogo.mover_peca(*movimento)
                eval_atual, _ = copia_jogo.minimax(profundidade - 1, True, alpha, beta)
                if eval_atual < min_eval:
                    min_eval = eval_atual
                    melhor_movimento = movimento
                beta = min(beta, eval_atual)
                if beta <= alpha:
                    break
            return min_eval, melhor_movimento

# Função principal do jogo
def main():
    jogo = Jogo()
    selecionado = None
    rodando = True
    fim_de_jogo = False

    while rodando:
        jogo.desenhar_tabuleiro()
        jogo.desenhar_info()  # Desenhar a área de informações
        pygame.display.flip()

        if fim_de_jogo:
            fonte_fim = pygame.font.SysFont(None, 50)
            texto_fim = fonte_fim.render('Xeque-mate!', True, PRETO)
            pos_texto = texto_fim.get_rect(center=(LARGURA_TABULEIRO//2, ALTURA_TABULEIRO//2))
            tela.blit(texto_fim, pos_texto)
            pygame.display.flip()
            pygame.time.wait(3000)
            rodando = False
            continue

        if jogo.jogador_atual == 'vermelho':
            # Turno da IA
            eval_score, melhor_movimento = jogo.minimax(3, True)
            if melhor_movimento:
                jogo.mover_peca(*melhor_movimento, is_ai_move=True, eval_score=eval_score)
                print(f"IA move de {melhor_movimento[0]} para {melhor_movimento[1]} | Eval: {eval_score}")
            if jogo.esta_em_xeque_mate('azul'):
                fim_de_jogo = True
            jogo.jogador_atual = 'azul'
            continue

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x >= LARGURA_TABULEIRO or y >= ALTURA_TABULEIRO:
                    # Click fora do tabuleiro
                    continue
                x = x // TAMANHO_QUADRADO
                y = y // TAMANHO_QUADRADO
                if selecionado:
                    if (x, y) in selecionado[2]:
                        jogo.mover_peca((selecionado[0], selecionado[1]), (x, y))
                        if jogo.esta_em_xeque_mate('vermelho'):
                            fim_de_jogo = True
                        jogo.jogador_atual = 'vermelho'
                        selecionado = None
                    else:
                        selecionado = None
                else:
                    peca = jogo.tabuleiro[y][x]
                    if peca and peca.cor == 'azul':
                        movimentos = peca.movimentos_validos(x, y, jogo.tabuleiro, jogo.roque_disponivel)
                        movimentos_legais = []
                        for mov in movimentos:
                            copia_jogo = copy.deepcopy(jogo)
                            copia_jogo.mover_peca((x, y), mov)
                            if not copia_jogo.esta_em_xeque('azul'):
                                movimentos_legais.append(mov)
                        if movimentos_legais:
                            selecionado = (x, y, movimentos_legais)
                            # Destacar movimentos possíveis
                            jogo.desenhar_tabuleiro()
                            jogo.desenhar_info()
                            pygame.draw.rect(tela, AMARELO, (x*TAMANHO_QUADRADO, y*TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO), 3)
                            for mov in movimentos_legais:
                                pygame.draw.circle(tela, VERDE, (mov[0]*TAMANHO_QUADRADO + TAMANHO_QUADRADO//2, mov[1]*TAMANHO_QUADRADO + TAMANHO_QUADRADO//2), 10)
                            pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
