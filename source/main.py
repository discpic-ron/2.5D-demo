import pygame
import math
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# constants
running = True
FOV = math.radians(60)
NUM_RAYS = 200
MAX_DEPTH = 8
map = [
  [0,0,0,0,0],
  [0,0,1,0,0],
  [0,0,0,0,0]
]
MAP_H, MAP_W = len(map), len(map[0])

# Player
player_x, player_y = 1.5, 1.5
player_angle = 0
speed = 2.0
rot_speed = 1.5

# functions 
def cast_rays():
  start_angle = player_angle - FOV / 2
  delta_angle = FOV / NUM_RAYS

  for ray in range(NUM_RAYS):
    angle = start_angle + ray * delta_angle
    sin_a = math.sin(angle)
    cos_a = math.cos(angle)
    depth = 0
    hit = False

    while not hit and depth < MAX_DEPTH:
      depth += 0.02
      test_x = int(player_x + cos_a * depth)
      test_y = int(player_y + sin_a * depth)

      if test_x < 0 or test_x >= MAP_W or test_y < 0 or test_y >= MAP_H:
        hit = True
        depth = MAX_DEPTH

      elif world_map[test_y][test_x] == 1:
        hit = True

    # Wall height
    wall_height = min(HEIGHT, int(HEIGHT / (depth + 0.0001)))

    # Shade based on distance
    shade = max(50, 255 - int(depth * 40))
    color = (shade, shade // 2, shade // 2)

    # Draw vertical slice
    x = int(ray * (WIDTH / NUM_RAYS))
    pygame.draw.rect(screen, color, (x, HEIGHT//2 - wall_height//2, WIDTH/NUM_RAYS + 1, wall_height))
    
while running:
  clock.tick(60)/1000.0
  move_dt = speed * dt
  rot_dt = rot_speed * dt
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      
  keys = pygame.key.get_pressed()
  if keys[pygame.K_LEFT] or keys[pygame.K_a]:
    player_angle -= rot_dt
  if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
    player_angle += rot_dt
    
  # movement
  old_x, old_y = player_x, player_y
  if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_x += math.cos(player_angle) * move_dt
        player_y += math.sin(player_angle) * move_dt
  if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_x -= math.cos(player_angle) * move_dt
        player_y -= math.sin(player_angle) * move_dt
    
  gx, gy = player_x,player_y
  if gy < 0 or gy >= MAP_H or gx < 0 or gx >= MAP_W or world_map[gy][gx] == 1:
    player_x, player_y = old_x, old_y
    
  screen.fill((0,0,0))
  pygame.draw.rect(screen, (60, 60, 60), (0, HEIGHT//2, WIDTH, HEIGHT//2))
  cast_rays()  # Raycast walls
  
  pygame.display.flip()
pygame.quit()
