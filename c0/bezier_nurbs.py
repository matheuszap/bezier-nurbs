import pygame
import numpy as np

pygame.init()

# Configurações da janela
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Continuidade C0 (Bézier e NURBS)")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Função para calcular a curva Bezier
def curva_bezier(pontosControle, t):
    n = len(pontosControle) - 1
    curva = np.zeros(2)
    
    for i in range(n + 1):
        curva += comb(n, i) * (1 - t) ** (n - i) * t ** i * pontosControle[i]
    
    return curva

# Função para calcular a curva NURBS
def curva_nurbs(pontosControle, pesos, t):
    n = len(pontosControle) - 1
    p = 5  # Grau da curva NURBS

    numPontos = len(t)
    curva = np.zeros((numPontos, 2))

    for i in range(n + 1):
        blend = comb(p, i) * (1 - t[:, np.newaxis]) ** (p - i) * t[:, np.newaxis] ** i  # Coeficiente binomial
        curva += blend * pesos[i] * pontosControle[i, :]
    
    return curva

# Função para calcular os coeficientes binomiais
def comb(n, k):
    return np.math.factorial(n) / (np.math.factorial(k) * np.math.factorial(n - k))

# Pontos de controle da curva Bezier (Grau da curva será núm. de pontos + 1)
pontosControleBezier = np.array([[100, 400], [200, 200], [300, 500], [500, 200], [700, 100], [800, 300]])
pontosControleNurbs = np.array([[800, 300], [900, 200], [1000, 400], [1100, 200], [1200, 100], [1300, 300]])
pesosNurbs = np.array([1, 1, 1, 1, 1, 1])

zoom = 0.5
zoom_in = False
zoom_out = False

bezier = True
while bezier:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bezier = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                zoom_in = True
            elif event.key == pygame.K_x:
                zoom_out = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_z:
                zoom_in = False
            elif event.key == pygame.K_x:
                zoom_out = False
    
    if zoom_in:
        zoom *= 1.01  # Aumenta o zoom em 10%
    elif zoom_out:
        zoom /= 1.01  # Diminui o zoom em 10%
    
    screen.fill(BLACK)
    
    # Ajuste da escala dos pontos de controle para o zoom
    pontosControleBezier_scaled = pontosControleBezier * zoom
    pontosControleNurbs_scaled = pontosControleNurbs * zoom

    # Desenho dos pontos de controle Bézier
    for ponto in pontosControleBezier_scaled:
        pygame.draw.circle(screen, GREEN, (int(ponto[0]), int(ponto[1])), 5)

    # Desenho dos pontos de controle Nurbs
    for ponto in pontosControleNurbs_scaled:
        pygame.draw.circle(screen, BLUE, (int(ponto[0]), int(ponto[1])), 5)

    # Desenho das retas entre os pontos de controle Bézier  
    pygame.draw.lines(screen, GREEN, False, pontosControleBezier_scaled.astype(int), 1)

    # Desenho das retas entre os pontos de controle NURBS
    pygame.draw.lines(screen, BLUE, False, pontosControleNurbs_scaled.astype(int), 1)
    
    # Definir o último ponto de controle da curva Bezier igual ao primeiro ponto de controle da curva NURBS
    pontosControleBezier[-1] = pontosControleNurbs[0]

    # Desenhar uma linha reta conectando os dois pontos
    pygame.draw.line(screen, GREEN, pontosControleBezier_scaled[-1].astype(int), pontosControleNurbs_scaled[0].astype(int), 1)

    # Desenho da curva Bezier
    t = np.linspace(0, 1, 100)
    curvaBezier = np.array([curva_bezier(pontosControleBezier, i) for i in t])

    # Ajuste da escala da curva Bezier para o zoom
    curvaBezier_scaled = curvaBezier * zoom

    # Desenho da curva Bezier
    pygame.draw.lines(screen, RED, False, curvaBezier_scaled.astype(int), 2)

    # Desenho da curva NURBS
    curvaNurbs = curva_nurbs(pontosControleNurbs, pesosNurbs, t)

    # Normalização das coordenadas da curva NURBS para o intervalo (0, 1)
    min_x = np.min(curvaNurbs[:, 0])
    max_x = np.max(curvaNurbs[:, 0])
    min_y = np.min(curvaNurbs[:, 1])
    max_y = np.max(curvaNurbs[:, 1])
    curvaNurbs[:, 0] = (curvaNurbs[:, 0] - min_x) / (max_x - min_x)
    curvaNurbs[:, 1] = (curvaNurbs[:, 1] - min_y) / (max_y - min_y)

    # Multiplicação pelo tamanho da janela e pelo fator de zoom
    curvaNurbs[:, 0] = curvaNurbs[:, 0] * (width * zoom)
    curvaNurbs[:, 1] = curvaNurbs[:, 1] * (height * zoom)

    # Desenho da curva NURBS
    curvaNurbs = curva_nurbs(pontosControleNurbs, pesosNurbs, t)

    # Escalonamento da curva NURBS
    curvaNurbs_scaled = curvaNurbs * zoom

    # Desenho da curva NURBS
    pygame.draw.lines(screen, RED, False, curvaNurbs_scaled.astype(int), 2)

    pygame.display.flip()

pygame.quit()
