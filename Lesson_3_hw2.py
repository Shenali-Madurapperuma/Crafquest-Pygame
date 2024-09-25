import pygame
import os

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.6)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pirate')

clock = pygame.time.Clock()
FPS = 60

GRAVITY = 0.75

moving_left = False
moving_right = False

BG = (176, 224, 230)
RED = (255, 0, 0)

def draw_bg():
  screen.fill(BG)
  pygame.draw.line(screen, RED, (0, 500), (SCREEN_WIDTH, 500))
  
class Pirate(pygame.sprite.Sprite):
  def __init__(self, char_type, x, y, scale, speed):
    pygame.sprite.Sprite.__init__(self)
    self.alive = True
    self.char_type = char_type
    self.speed = speed
    self.direction = 1
    self.vel_y = 0
    self.jump = False
    self.in_air = True
    self.flip = False
    self.animation_list = []
    self.frame_index = 0
    self.action = 0
    self.update_time = pygame.time.get_ticks()
    
    animation_types = ['Idle', 'Run', "Jump"]
    
    for animation in animation_types:
      temp_list = []
      num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
      
      for i in range(num_of_frames):
        img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png')
        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        temp_list.append(img)
        
      self.animation_list.append(temp_list)
      
    self.image = self.animation_list[self.action][self.frame_index]
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    
  def move(self, moving_left, moving_right):
    dx = 0
    dy = 0
    
    if moving_left:
      dx = -self.speed
      self.flip = True
      self.direction = -1
      
    if moving_right:
      dx = self.speed
      self.flip = False
      self.direction = 1
      
    if self.jump == True and self.in_air == False:
      self.vel_y = -11
      self.jump = False
      self.in_air = True
      
    self.vel_y += GRAVITY
    
    if self.vel_y > 10:
      self.vel_y = 10

    dy += self.vel_y
    
    if self.rect.bottom + dy > 500:
      dy = 500 - self.rect.bottom
      self.in_air = False
      
    self.rect.x += dx
    self.rect.y += dy
    
  def update_animation(self):
    ANIMATION_COOLDOWN = 100
    self.image = self.animation_list[self.action][self.frame_index]
    
    if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
      self.update_time = pygame.time.get_ticks()
      self.frame_index += 1
      
    if self.frame_index >= len(self.animation_list[self.action]):
      self.frame_index = 0
      
  def update_action(self, new_action):
    if new_action != self.action:
      self.action = new_action
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks()
      
  def draw(self):
    screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
    
GRAVITY = 0.75

pirate = Pirate('pirate', 200, 200, 0.2, 5)

run = True
while run:
  clock.tick(FPS)
  
  draw_bg()
  
  pirate.update_animation()
  pirate.draw()
  
  if pirate.alive:
    if pirate.in_air:
      pirate.update_action(2)
    elif moving_left or moving_right:
      pirate.update_action(1)
    else:
      pirate.update_action(0)
      
    pirate.move(moving_left, moving_right)
    
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
      
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_a:
        moving_left = True
      if event.key == pygame.K_d:
        moving_right = True
      if event.key == pygame.K_w and pirate.alive:
        pirate.jump = True
      if event.key == pygame.K_ESCAPE:
        run = False
        
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_a:
        moving_left = False
      if event.key == pygame.K_d:
        moving_right = False
        
  pygame.display.update()
  
pygame.quit()