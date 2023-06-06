import pygame
import numpy as np

pygame.init()

# Configurações da janela
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Curva de Bézier")

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
    
    curva /= np.sum(curva, axis=0)  # Normalização dos pontos
    
    return curva


# Função para calcular os coeficientes binomiais
def comb(n, k):
    return np.math.factorial(n) / (np.math.factorial(k) * np.math.factorial(n - k))


# Pontos de controle da curva Bezier (Grau da curva será núm. de pontos + 1)
pontosControleBezier = np.array([[100, 400], [200, 200], [300, 500], [500, 200], [700, 100], [800, 300]])
pontosControleNurbs = np.array([[800, 300], [900, 200], [1000, 400], [1100, 200], [1200, 100], [1300, 300]])
pesosNurbs = np.array([20, 30, 50, 10, 35, 20])

bezier = True
while bezier:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bezier = False
    
    screen.fill(BLACK)
    
    # Desenho dos pontos de controle Bézier
    for ponto in pontosControleBezier:
        pygame.draw.circle(screen, GREEN, ponto, 5)

    # Desenho dos pontos de controle Nurbs
    for ponto in pontosControleNurbs:
        pygame.draw.circle(screen, BLUE, ponto, 5)

    # Desenho das retas entre os pontos de controle Bézier
    pygame.draw.lines(screen, GREEN, False, pontosControleBezier, 1)

    # Desenho das retas entre os pontos de controle Nurbs
    pygame.draw.lines(screen, BLUE, False, pontosControleNurbs, 1)
    
    # Desenho da curva Bezier
    t = np.linspace(0, 1, 100)
    curvaBezier = np.array([curva_bezier(pontosControleBezier, i) for i in t])
    pygame.draw.lines(screen, RED, False, curvaBezier.astype(int), 2)

    curvaNurbs = curva_nurbs(pontosControleNurbs, pesosNurbs, t)
    min_x = np.min(curvaNurbs[:, 0])
    max_x = np.max(curvaNurbs[:, 0])
    min_y = np.min(curvaNurbs[:, 1])
    max_y = np.max(curvaNurbs[:, 1])

    # Normalização das coordenadas para o intervalo (0, 1)
    curvaNurbs[:, 0] = (curvaNurbs[:, 0] - min_x) / (max_x - min_x)
    curvaNurbs[:, 1] = (curvaNurbs[:, 1] - min_y) / (max_y - min_y)

    # Multiplicação pelo tamanho da janela
    curvaNurbs[:, 0] *= width
    curvaNurbs[:, 1] *= height

    pygame.draw.lines(screen, RED, False, curvaNurbs.astype(int), 2)

    
    pygame.display.flip()

pygame.quit()
