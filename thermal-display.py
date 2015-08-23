#!/etc/bin/python2.7

import pygame, time, sys
from omrond6t import *
from pygame.locals import *

omron = OmronD6T(arraySize=8)

SCREEN_DIMS = [1440, 900]
xSize = 8
ySize = 1
arraySize = xSize * ySize
screen = pygame.display.set_mode(SCREEN_DIMS)
pygame.display.set_caption('Omron D6T Temperature Array')
pygame.mouse.set_visible(False)
pygame.init()
font = pygame.font.Font(None, 36)
font2 = pygame.font.Font(None, 72)

X = []
Y = []
temp_hit = 0
square = []
center = []
rect = [Rect] * arraySize

cellWidth = SCREEN_DIMS[0] / xSize
cellHeight = SCREEN_DIMS[1] / ySize
cellWidthCenter = cellWidth / 2
if cellHeight > cellWidth:
  cellHeight = cellWidth
cellHeightCenter = cellHeight / 2

for x in range(xSize):
    X.append(x * cellWidth)

for y in range(ySize):
    Y.append((y * cellHeight) + (SCREEN_DIMS[1] - cellHeight))

for x in range(xSize):
  for y in range(ySize):
    square.append((X[x], Y[y], cellWidth, cellHeight))
    center.append((X[x] + cellWidthCenter, Y[y] + cellHeightCenter))

def temp_to_rgb(temp):
  if temp < 80:
    return (0, 0, 192)
  elif temp >= 80 and temp < 90:
    return (255, 128, 0)
  elif temp > 90:
    return (255, 0, 0)

hit_start_time = time.time()
hit_time = 11
person_detect = False

text = font.render('Omron D6T Thermal Sensor', 1, (255,255,255))
text_pos = text.get_rect()
text_pos.center = (SCREEN_DIMS[0]/2,SCREEN_DIMS[1] - cellHeight - 18)
screen.blit(text, text_pos)


while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.display.quit()
      sys.exit(0)
    if event.type == KEYDOWN:
      if event.key == K_q or event.key == K_ESCAPE:
        pygame.display.quit()
        sys.exit(0)

  bytes_read, temperature = omron.read()

  temp_hit = 0
  for i in range(arraySize):
    if temperature[i] >= 80:
      temp_hit += 1
    
    screen.fill(temp_to_rgb(temperature[i]), square[i])
    
    text = font.render(str(i+1), 1, (255,255,255))
    text_pos = text.get_rect()
    text_pos.center = (center[i][0], SCREEN_DIMS[1] - cellHeight + 18)
    screen.blit(text, text_pos)
    
    text = font.render(str(int(temperature[i])) + chr(0xb0) + "F", 1, (255,255,255))
    text_pos = text.get_rect()
    text_pos.center = center[i]
    screen.blit(text, text_pos)

  hit_time = time.time() - hit_start_time

  if temp_hit > 3:
    person_detect = True
    hit_start_time = time.time()
  elif temp_hit <= 3 and hit_time > 10:
    person_detect = False

  if person_detect:    
    screen.fill((0,0,0), (0,180,SCREEN_DIMS[0],180))
    screen.fill((255,0,0), (0,0,SCREEN_DIMS[0],180))
    text = font2.render('RESERVED', 1, (255,255,255))
    text_pos = text.get_rect()
    text_pos.center = (SCREEN_DIMS[0]/2,90)
    screen.blit(text, text_pos)
  else:
    screen.fill((0,0,0), (0,180,SCREEN_DIMS[0],180))
    screen.fill((0,192,0), (0,0,SCREEN_DIMS[0],180))
    text = font2.render('AVAILABLE', 1, (255,255,255))
    text_pos = text.get_rect()
    text_pos.center = (SCREEN_DIMS[0]/2,90)
    screen.blit(text, text_pos)

  pygame.display.update()
  time.sleep(0.01)
