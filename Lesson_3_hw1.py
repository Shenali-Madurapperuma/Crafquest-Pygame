import pygame
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pirate')

BG = (144, 201, 120)
RED = (255, 0, 0)

scale = 0.3

img = pygame.image.load("img/pirate/Idle/0.png")

# Get the original size of the image
img_width, img_height = img.get_size()

# Scale the image
new_size = (int(img_width * scale), int(img_height * scale))
image = pygame.transform.scale(img, new_size)

def draw_bg():
  screen.fill(BG)
  pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))
  
run = True

while run:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
      
  # draw_bg()
  pygame.display.update()
  screen.blit(image, (100,200))
  
pygame.quit()