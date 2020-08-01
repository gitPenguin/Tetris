import pygame, random
from tetris import board

display_width = 800
display_height = 600

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('pog')

surface_width = 200
surface_height = 480

cell_width = surface_width / 10
cell_height = surface_height / 24

grid_surface = pygame.Surface((surface_width + 2, surface_height + 2))
grid_surface.set_colorkey((255, 255, 255))
pixel_surface = pygame.Surface((surface_width, surface_height))
#pixel_surface.set_colorkey((0, 0, 0))

black = (0, 0, 0)
white = (255, 255, 255)
light_gray = (200, 200, 200)
background = light_gray

colors = {'aqua': (0, 204, 255),
          'blue': (0, 102, 255),
          'orange': (255, 153, 51),
          'yellow': (255, 204, 0),
          'green': (0, 204, 0),
          'purple': (204, 0, 204),
          'red': (255, 0, 0),
          None: white}


board = board()
board.init()

clock = pygame.time.Clock()
crashed = False
game_cycle = 0
default_cooldown = 1
move_cooldown = 7
cooldown_map = {97: move_cooldown, 
                100: move_cooldown,
                115: move_cooldown, 
                119: 15,
                32: 15}
cooldowns = [0 for i in range(323)]

def draw_grid():
    grid_surface.fill(white)

    for i in range(0, 11):
        pygame.draw.line(grid_surface, light_gray, (i * cell_width, 0), (i * cell_width, surface_height), 2)

    for i in range(0, 25):
        pygame.draw.line(grid_surface, light_gray, (0, i * cell_height), (surface_width, i * cell_height), 2)

    screen.blit(grid_surface, (display_width / 2 - surface_width / 2, display_height / 2 - surface_height / 2))

def draw_game():
    pixel_surface.fill(background)
    terrain = board.get_board()[0]
    piece = board.get_board()[1]

    for i in range(0, 10):
        for j in range(0, 24):
            rectangle = pygame.Rect((i * cell_width, j * cell_height), (cell_width, cell_height))
            pixel_color = black
            if (piece[i][j] == None):
                pixel_color = colors[terrain[i][j]]
            else:
                pixel_color = colors[piece[i][j]]
            
            pygame.draw.rect(pixel_surface, pixel_color, rectangle)
    
    screen.blit(pixel_surface, (display_width / 2 - surface_width / 2, display_height / 2 - surface_height / 2))

def controller(keys):
    if keys[97] == 1 and cooldown(97, keys): #a
        board.move((-1, 0))

    if keys[115] == 1 and cooldown(115, keys): #s
        board.move((0, 1))

    if keys[100] == 1 and cooldown(100, keys): #d - fast drop
        board.move((1, 0))

    if keys[119] == 1 and cooldown(119, keys): #w - hard drop
        board.hard_drop()

    if keys[32] == 1 and cooldown(32, keys): #space - rotate clockwise
        board.rotate(True)

def cooldown(id, keys):
    if cooldowns[id] > 0:
        cooldowns[id] -= 1
        return False
    else:
        cooldowns[id] = cooldown_map[id] if id in cooldown_map else default_cooldown
        return True

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    screen.fill(background)
    #pygame.key.get_pressed()

    game_cycle += 1

    controller(pygame.key.get_pressed())

    if game_cycle % 60 == 0:
        board.cycle()

    draw_game()
    draw_grid()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()