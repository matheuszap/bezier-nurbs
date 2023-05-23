import pygame
import numpy as np

# Inicialização do Pygame
pygame.init()

# Configurações da janela
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Curva de Bézier")

# Cores
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Função para calcular a curva Bezier
def bezier_curve(points, t):
    n = len(points) - 1
    curve = np.zeros(2)
    
    for i in range(n + 1):
        curve += comb(n, i) * (1 - t) ** (n - i) * t ** i * points[i]
    
    return curve

# Função para calcular os coeficientes binomiais
def comb(n, k):
    return np.math.factorial(n) / (np.math.factorial(k) * np.math.factorial(n - k))

# Pontos de controle da curva Bezier (Grau da curva será núm. de pontos + 1)
points = np.array([[100, 400], [300, 200], [500, 500], [700, 300], [700, 500], [800, 400]])

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(BLACK)
    
    # Desenho dos pontos de controle
    for point in points:
        pygame.draw.circle(screen, RED, point, 5)
    
    # Desenho da curva Bezier
    t = np.linspace(0, 1, 100)
    curve = np.array([bezier_curve(points, i) for i in t])
    pygame.draw.lines(screen, RED, False, curve.astype(int), 2)
    
    pygame.display.flip()

pygame.quit()
