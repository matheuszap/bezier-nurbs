import pygame
import numpy as np

pygame.init()

# Configurações da janela
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Curva de Bézier")

# Cores
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fórmula para calcular a posição na curva de Bézier de um determinado valor t:
#
# B(t) = Σ [P(i) * B(i,n)(t)], para i = 0 até n
#
# t é um parâmetro variando de 0 a 1, representando o ponto na curva de Bézier
# n é o grau da curva de Bézier (número de pontos de controle - 1)
# P(i) são os pontos de controle da curva de Bézier
# B(i,n)(t) são os coeficientes binomiais dados por B(i,n)(t) = C(n,i) * t^i * (1 - t)^(n-i), onde C(n,i) é o coeficiente binomial que representa o número de combinações de n elementos tomados i a i
# A fórmula calcula a posição B(t) na curva de Bézier com base nos pontos de controle e nos coeficientes binomiais
#
# Calculando o ponto na curva para t = 0.5:
#
# B(0,5)(t) = C(5,0) * t^0 * (1 - t)^(5-0) = 1 * 1 * 0.5^5 = 0.03125
# B(1,5)(t) = C(5,1) * t^1 * (1 - t)^(5-1) = 5 * 0.5 * 0.5^4 = 0.15625
# B(2,5)(t) = C(5,2) * t^2 * (1 - t)^(5-2) = 10 * 0.5^2 * 0.5^3 = 0.3125
# B(3,5)(t) = C(5,3) * t^3 * (1 - t)^(5-3) = 10 * 0.5^3 * 0.5^2 = 0.3125
# B(4,5)(t) = C(5,4) * t^4 * (1 - t)^(5-4) = 5 * 0.5^4 * 0.5^1 = 0.15625
# B(5,5)(t) = C(5,5) * t^5 * (1 - t)^(5-5) = 1 * 0.5^5 * 1 = 0.03125
#
# P0 = (100, 400)
# P1 = (200, 200)
# P2 = (300, 500)
# P3 = (500, 200)
# P4 = (700, 100)
# P5 = (800, 300)
#
# B(t) = P0 * 0.03125 + P1 * 0.15625 + P2 * 0.3125 + P3 * 0.3125 + P4 * 0.15625 + P5 * 0.03125 = (319.375, 287.5)

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
points = np.array([[100, 400], [200, 200], [300, 500], [500, 200], [700, 100], [800, 300]])

bezier = True
while bezier:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bezier = False
    
    screen.fill(BLACK)
    
    # Desenho dos pontos de controle
    for point in points:
        pygame.draw.circle(screen, GREEN, point, 5)

    # Desenho das retas entre os pontos de controle
    pygame.draw.lines(screen, GREEN, False, points, 1)
    
    # Desenho da curva Bezier
    t = np.linspace(0, 1, 100)
    curve = np.array([bezier_curve(points, i) for i in t])
    pygame.draw.lines(screen, RED, False, curve.astype(int), 2)
    
    pygame.display.flip()

pygame.quit()
