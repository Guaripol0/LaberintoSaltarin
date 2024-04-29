import pygame
from resolucion import *
from draw_arrow_function import draw_arrow
import argparse
import os
import sys

def inicializar(dimension):
    width, height = dimension
    stdout, stderr = sys.stdout, sys.stderr
    null = open(os.devnull, 'w')
    sys.stdout, sys.stderr = null, null

    pygame.init()
    sys.stdout, sys.stderr = stdout, stderr

    return pygame.display.set_mode((width, height))

def leer_matriz_desde_txt(ruta_archivo):
    laberintos = []
    laberinto = {}
    with open(ruta_archivo, 'r') as f:
        for linea in f:
            numeros = [int(num) for num in linea.split()]
            if len(numeros) == 1 and numeros[0] == 0:
                if laberinto:  # Asegurarse de que el laberinto actual no esté vacío
                    laberintos.append(laberinto)
                break
            elif len(numeros) == 6:
                if laberinto:  # Si ya hay un laberinto en construcción, añadirlo a la lista
                    laberintos.append(laberinto)
                laberinto = {
                    'matriz': [],
                    'inicio': (numeros[2], numeros[3]),
                    'destino': (numeros[4], numeros[5])
                }
            else:
                if 'matriz' in laberinto:  # Asegurarse de que 'matriz' existe en el diccionario
                    laberinto['matriz'].append(numeros)
    return laberintos

def imprimir_matriz(maze, path, screen,start,goal, draw_path=False):
    if(len(maze) > 25 or len(maze[0]) > 25):
        print("laberinto muy grande para imprimir en pantalla")
        exit()
    black = (0, 0, 0)
    background = (128, 0, 128)
    red = (255, 255, 0)
    green = (255, 165, 0)
    blue = (0, 255, 255)
    color_arrows = (0, 200, 100)
    text_color = black 
    max_diff = 50
    cell_width = (screen.get_width()-350) // len(maze[0])
    cell_height = screen.get_height() // len(maze)

    if abs(cell_width - cell_height) > max_diff:
        min_dim = min(cell_width, cell_height)
        cell_width = min_dim
        cell_height = min_dim

    maze_width = len(maze[0]) * cell_width
    maze_height = len(maze) * cell_height

    offset_x = screen.get_width() - maze_width - 20
    offset_y = (screen.get_height() - maze_height) // 2

    for i in range(len(maze)):
            for j in range(len(maze[0])):
                rect = pygame.Rect(j * cell_width + offset_x, i * cell_height + offset_y, cell_width, cell_height)
                color = background
                if (i, j) == start: 
                    color = red
                elif (i, j) == goal: 
                    color = blue
                elif draw_path and (i, j) in path:
                    color = green
                pygame.draw.rect(screen, (max(color[0] - 20, 0), max(color[1] - 20, 0), max(color[2] - 20, 0)), (rect.x, rect.y + 5, rect.width, rect.height))  # Draw cell shadow
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, black, rect, 1) 

    if draw_path:
        for i in range(len(path) - 1):
            offset = 10 
            start_x = path[i][1] * cell_width + cell_width // 2 + offset_x
            start_y = path[i][0] * cell_height + cell_height // 2 + offset_y
            end_x = path[i+1][1] * cell_width + cell_width // 2 + offset_x
            end_y = path[i+1][0] * cell_height + cell_height // 2 + offset_y

            if start_x < end_x:  
                start_x += offset
            elif start_x > end_x: 
                start_x -= offset
            if start_y < end_y:  
                start_y += offset
            elif start_y > end_y:  
                start_y -= offset

            if end_x > start_x: 
                end_x -= offset
            elif end_x < start_x: 
                end_x += offset
            if end_y > start_y:  
                end_y -= offset
            elif end_y < start_y:  
                end_y += offset

            start = pygame.Vector2(start_x, start_y)
            end = pygame.Vector2(end_x, end_y)
            draw_arrow(screen, start, end, color_arrows, body_width=5, head_width=10, head_height=10)
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            rect = pygame.Rect(j * cell_width + offset_x, i * cell_height + offset_y, cell_width, cell_height)
            font = pygame.font.Font(None, 36)
            text = font.render(str(maze[i][j]), True, text_color)  
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    pygame.display.flip()

class Button:
    def __init__(self, color, position, size, text=''):
        self.color = color
        self.position = position
        self.size = size
        self.text = text

    def draw(self, screen, outline=None):
        # Draw button with shadow effect
        pygame.draw.rect(screen, self._darker_color(), (*self.position, *self.size))
        pygame.draw.rect(screen, self.color, (self.position[0], self.position[1] - 5, *self.size))

        if self.text:
            font = pygame.font.SysFont('Arial', 30)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (self.position[0] + (self.size[0]/2 - text.get_width()/2), self.position[1] + (self.size[1]/2 - text.get_height()/2)))

    def is_over(self, pos):
        # Returns True if pos is inside the button
        x, y = self.position
        width, height = self.size
        return x < pos[0] < x + width and y < pos[1] < y + height

    def _darker_color(self):
        return (max(self.color[0] - 20, 0), max(self.color[1] - 20, 0), max(self.color[2] - 20, 0))
    
def argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interfaz", action='store_true', help="Enable Pygame drawing")
    parser.add_argument("--ruta_matriz", type=str, help="Path to the .txt file containing the matrix")

    args = parser.parse_args()

    mazes = []
    starts = []
    goals = []

    if args.ruta_matriz:
        with open(args.ruta_matriz, 'r') as f:
            while True:
                line = f.readline().strip()
                if line == '0' or line == '':
                    break
                matrixM, matrixN, start_x, start_y, goal_x, goal_y = map(int, line.split())
                starts.append((start_x, start_y))
                goals.append((goal_x, goal_y))
                matrix = []
                for _ in range(matrixM):
                    matrix.append(list(map(int, f.readline().strip().split())))
                mazes.append(matrix)
    else:
        matrix = verificar_matriz(10, 10)
        start_point = (0, 0)
        ending_point = (len(matrix) - 1, len(matrix[0]) - 1)
        mazes.append(matrix)
        starts.append(start_point)
        goals.append(ending_point)

    return mazes, starts, goals, args.interfaz

def casos(mazes, starts, goals, interfaz_enabled):
    start = None
    goal = None
    maze = None
    if interfaz_enabled:
        maze = mazes[0]
        start = starts[0]
        goal = goals[0]

        pygame.init()
        screen_width, screen_height = 1366, 768
        screen = pygame.display.set_mode((screen_width, screen_height))
        background_color = (0, 0, 0)  # Change background color to black
        screen.fill(background_color)
        button_width, button_height = 300, 50
        position_x_buttons = 10
        button_y = 10  # Set the y position of the buttons to 10 pixels from the top of the screen
        solve_button = Button((0, 255, 0), (position_x_buttons, button_y), (button_width, button_height), 'Resolver')
        dfs_button = Button((0, 255, 0), (position_x_buttons, button_y + 60), (button_width, button_height), 'DFS')  
        ucs_button = Button((0, 255, 0), (position_x_buttons, button_y + 120), (button_width, button_height), 'UCS') 
        jumps_button = Button((0, 255, 0), (position_x_buttons, button_y + 180), (button_width, button_height), 'Mostrar Saltos')  
        imprimir_matriz(maze, [], screen, draw_path=False,start=start,goal=goal)

        draw_maze = False
        running = True
        solution = None
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if draw_maze:
                if solution is not None:
                    path = solution['path']
                    imprimir_matriz(maze, path, screen, draw_path=True,start=start,goal=goal)
                else:
                    imprimir_matriz(maze, [], screen, draw_path=False,start=start,goal=goal)
            pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if solve_button.is_over(pos):
                    draw_maze = True
                    solution = resolver_juego(maze, start, goal)
                elif dfs_button.is_over(pos):
                    draw_maze = True
                    solution = resolver_juego_dfs(maze, start, goal)
                elif ucs_button.is_over(pos):
                    draw_maze = True
                    solution = resolver_juego_ucs(maze, start, goal)
                elif jumps_button.is_over(pos):
                    draw_maze = True
                    if solution is not None:
                        jumps = solution['jumps']
                        font=pygame.font.SysFont('Arial', 30)
                        text =  font.render("Saltos: " + str(jumps), True, (255, 255, 255))
                        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(position_x_buttons, button_y + 240, text.get_width(), text.get_height()))
                        screen.blit(text, (position_x_buttons, button_y + 240))
            for button in [solve_button, dfs_button, ucs_button, jumps_button]:
                if button.is_over(pos):
                    button.color = (200, 200, 200)
                else:
                    button.color = (255, 255, 255)
            for button in [solve_button, dfs_button, ucs_button, jumps_button]:
                button.draw(screen, (0, 0, 0))

            pygame.display.update() 

        pygame.quit()
    else:
        solutions = resolver_juego_completo(mazes, starts, goals)
        for solution in solutions:
            if solution:
                print(solution['jumps'])
            else:
                print('No hay solucion')


if __name__ == '__main__':
    mazes, starts, goals, interfaz_enabled = argumentos()
    casos(mazes, starts, goals, interfaz_enabled)