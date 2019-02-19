import pygame
import math
from pygame.locals import *

Width = 400
Height = 400
Block_Size = 20

Color = [[255,255,255],[0,0,0],[255,255,255],[224,224,224],[128,128,128],[64,64,64],[255,0,0],[255,96,208],
         [160,32,255],[80,208,255],[0,32,255],[96,255,128],[0,192,0],[255,224,32],[255,160,16],[160,128,96],
         [255,208,160],[100,153,255],[204,153,51],[51,0,152],[102,51,51]]

'''
Black = (0,0,0)
White = (255,255,255)
LightGray = (224,224,224)
Gray = (128,128,128)
DarkGray = (64,64,64)
Red = (255,0,0)
Pink = (255,96,208)
Purple = (160,32,255)
LightBlue = (80,208,255)
Blue = (0,32,255)
LightGreen = (96,255,128)
Green = (0,192,0)
Yellow = (255,224,32)
Orange = (255,160,16)
Brown = (160,128,96)
PalePink = (255,208,160)
'''

def LC(Col, Row, Screen):
    if Row == 0:
        pass
    else:
        pygame.draw.rect(Screen, Color[0], (Col + 1, Row + 1, Block_Size - 1, Block_Size - 1))


def RC(Col, Row, Screen):
    global Color

    if Row != 0:
        pass
    else:
        Color[0] = Screen.get_at((int(Col+2), int(Row+2)))

def Grid(Screen):
    a = Width // Block_Size
    b = Height // Block_Size

    for y in range(a):
        for x in range(b):
            pygame.draw.line(Screen, Color[1], (0, x * Block_Size), (Width, x * Block_Size), 1)
            pygame.draw.line(Screen, Color[1], (y * Block_Size, 0), (y * Block_Size, Height), 1)

def ColorBar(Screen):
    for c in range(20):
        pygame.draw.rect(Screen, Color[c + 1], ((c * Block_Size)+1, 1, Block_Size - 1, Block_Size - 1))

def main():
    pygame.init()
    Screen = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption("Super Paint")

    Screen.fill(Color[2])
    Grid(Screen)
    ColorBar(Screen)

    Ok = True
    base = Block_Size
    clock = pygame.time.Clock()

    while Ok:
        clock.tick(60)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Ok = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Pos = pygame.mouse.get_pos()
                Col = base * math.floor(float(Pos[0])/base)
                Row = base * math.floor(float(Pos[1])/base)
                # print("Click ", Pos, "Coord: ", Row, Col)

                if event.button == 1:
                  LC(Col, Row, Screen)

                if event.button == 3:
                  RC(Col, Row, Screen)

    pygame.quit()

if __name__ == "__main__":
    main()
