import pygame
import sys
from pygame.locals import *
import time

from Matrix import Matrix

HIGHLIGHTCOLOR = (255, 0, 255) # color of the selected gem's border
BGCOLOR = (170, 190, 255) # background color on the screen
GRIDCOLOR = (0, 0, 255) # color of the game board
CHOOSECOLOR = (200,0,0) #c color of the choosing grid
GAMEOVERCOLOR = (255, 100, 100) # color of the "Game over" text.
GAMEOVERBGCOLOR = (0, 0, 0) # background color of the "Game over" text.
SCORECOLOR = (85, 65, 0)


WINDOWWIDTH = 800  # width of the program's window, in pixels
WINDOWHEIGHT = 600 # height in pixels

GRIDSIZE=64


class ColorGame():
    def __init__(self):
        pygame.init()
        self.FPSCLOCK = pygame.time.Clock()
        self.WINDOWSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

        self.GEMIMAGES = list()
        for i in range(1,8):
            gemImage = pygame.image.load('%s.png' % i)
            self.GEMIMAGES.append(gemImage)

        self.X1=0
        self.Y1=0
        self.X2=0
        self.Y2=0
        self.FIRST_CLICK = False
        self.SECOND_CLICK = False
        self.matrix=Matrix()
        self.bg=pygame.image.load('bg.png')
        self.WINDOWSURF.blit(self.bg,(0,0))

    def Draw_bolls(self):
        rect=(2,2,598,598)
        self.WINDOWSURF.blit(self.bg.subsurface(rect),[2,2])

        for i in range(9):
            for j in range(9):
                color=self.matrix.Main_matrix[i,j]
                if color!=0:
                    self.WINDOWSURF.blit(self.GEMIMAGES[color-1],[14+i*GRIDSIZE,14+j*GRIDSIZE])
        pygame.display.update()

    def Move_balls(self,color, trace):
        boll=self.GEMIMAGES[color-1]
        NOW_X=self.X1
        NOW_Y=self.Y1
        NEXT_X=trace[0,0]
        NEXT_Y=trace[1,0]
        # for i in range(trace.shape[1]-1):
        for i in range(trace.shape[1]):
            if NOW_X == NEXT_X:
                for j in range(0,64,4):
                    DT=(NEXT_Y-NOW_Y)
                    self.WINDOWSURF.blit(boll,[NOW_X*GRIDSIZE+14,NOW_Y*GRIDSIZE+14+(j+1)*DT])
                    pygame.display.update()
                    
                    rect=(NOW_X*GRIDSIZE+13,NOW_Y*GRIDSIZE+13+(j+1)*DT,56,56)
                    self.WINDOWSURF.blit(self.bg.subsurface(rect),[NOW_X*GRIDSIZE+13,NOW_Y*GRIDSIZE+13+(j+1)*DT])
                    # FPSCLOCK.tick(60)
            elif NOW_Y == NEXT_Y:
                for j in range(0,64,4):
                    DT=(NEXT_X-NOW_X)
                    self.WINDOWSURF.blit(boll,[NOW_X*GRIDSIZE+14+(j+1)*DT,NOW_Y*GRIDSIZE+14])
                    pygame.display.update()
                    # FPSCLOCK.tick(60)
                    rect=(NOW_X*GRIDSIZE+13+(j+1)*DT,NOW_Y*GRIDSIZE+13,56,56)
                    self.WINDOWSURF.blit(self.bg.subsurface(rect),[NOW_X*GRIDSIZE+13+(j+1)*DT,NOW_Y*GRIDSIZE+13])
            NOW_X=NEXT_X
            NOW_Y=NEXT_Y
            try:
                NEXT_X=trace[0,i+1]
                NEXT_Y=trace[1,i+1]
            except:
                pass

    def highlight_boll(self,X,Y):
        # rect=(X*64+13,Y*64+13,56,56)
        pygame.draw.line(self.WINDOWSURF,CHOOSECOLOR,[X*64+14,Y*64+14],[X*64+14,Y*64+74],4)
        pygame.draw.line(self.WINDOWSURF,CHOOSECOLOR,[X*64+14,Y*64+14],[X*64+74,Y*64+14],4)
        pygame.draw.line(self.WINDOWSURF,CHOOSECOLOR,[X*64+74,Y*64+14],[X*64+74,Y*64+74],4)
        pygame.draw.line(self.WINDOWSURF,CHOOSECOLOR,[X*64+14,Y*64+74],[X*64+74,Y*64+74],4)
        # WINDOWSURF.blit(bg.subsurface(rect),[X*64+13,Y*64+13])
        pygame.display.update()

    def dis_highlight_boll(self,X,Y):
        rect=(X*GRIDSIZE+13,Y*64+13,64,64)
        self.WINDOWSURF.blit(self.bg.subsurface(rect),[X*GRIDSIZE+13,Y*GRIDSIZE+13])
        color=self.matrix.Main_matrix[X,Y]
        self.WINDOWSURF.blit(self.GEMIMAGES[color-1],[14+X*GRIDSIZE,14+Y*GRIDSIZE])
        pygame.display.update()

    def Boll_appear(self,new_bolls):
        #appear 3 bolls in the same time.
        for i in range(0,58,1):
            for j in range(3):
                rect=(new_bolls[j][0]*GRIDSIZE+13,new_bolls[j][1]*GRIDSIZE+13,56,56)
                self.WINDOWSURF.blit(self.bg.subsurface(rect),[new_bolls[j][0]*GRIDSIZE+13,new_bolls[j][1]*GRIDSIZE+13])
                im_temp=pygame.transform.smoothscale(self.GEMIMAGES[new_bolls[j][2]-1],(i,i))
                self.WINDOWSURF.blit(im_temp,(new_bolls[j][0]*GRIDSIZE+14+29-i/2,new_bolls[j][1]*GRIDSIZE+14+29-i/2))
            pygame.display.update()

            # FPSCLOCK.tick(60)

    def Boll_disappear(self,new_bolls):
        #disappear bolls in the same time.
        for i in range(48,0,-1):
            for j in range(len(new_bolls)):
                rect=(new_bolls[j][0]*GRIDSIZE+13,new_bolls[j][1]*GRIDSIZE+13,56,56)
                self.WINDOWSURF.blit(self.bg.subsurface(rect),[new_bolls[j][0]*GRIDSIZE+13,new_bolls[j][1]*GRIDSIZE+13])
                im_temp=pygame.transform.smoothscale(self.GEMIMAGES[new_bolls[j][2]-1],(i,i))
                self.WINDOWSURF.blit(im_temp,(new_bolls[j][0]*GRIDSIZE+16+25-i/2,new_bolls[j][1]*GRIDSIZE+16+25-i/2))
            pygame.display.update()

            # FPSCLOCK.tick(60)

    def Draw_score(self):
        BASICFONT = pygame.font.Font('freesansbold.ttf', 50)
        scoreImg = BASICFONT.render(str(self.matrix.score), 1, SCORECOLOR) 
        scoreRect = scoreImg.get_rect()
        scoreRect.bottomleft = (660, 480 )
        rect=(630,400,120,100)
        self.WINDOWSURF.blit(self.bg.subsurface(rect),[630,400])
        self.WINDOWSURF.blit(scoreImg, scoreRect)

    def Draw_label(self):
        BASICFONT = pygame.font.Font('freesansbold.ttf', 50)
        titleImg=BASICFONT.render("SCORE",True,SCORECOLOR)
        nextImg=BASICFONT.render("NEXT",True,SCORECOLOR)
        titleRect=titleImg.get_rect()
        nextRect=nextImg.get_rect()
        titleRect.bottomleft = (610, 400 )
        nextRect.bottomleft= (630,100)
        self.WINDOWSURF.blit(titleImg, titleRect)
        self.WINDOWSURF.blit(nextImg, nextRect)


    def Draw_nextcolors(self):
        rect=(610,120,190,80)
        self.WINDOWSURF.blit(self.bg.subsurface(rect),[610,120])
        for j in range(3):
            color=self.matrix.next_colors[j]
            self.WINDOWSURF.blit(self.GEMIMAGES[color-1],(610+j*64,120))


def main():
    game=ColorGame()
    game.Draw_score()
    game.Draw_label()
    game.Draw_nextcolors()
    game.Draw_bolls()

    while True: 
        events=pygame.event.get()
        for event in events: 
            if event.type == QUIT: 
                pygame.quit()
                sys.exit(0) 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    pos=event.pos
                    x=(pos[0]-12)/GRIDSIZE
                    y=(pos[1]-12)/GRIDSIZE
                    if x>8 or y> 8:
                        break
                    if game.matrix.Main_matrix[x,y]!=0:
                        if game.FIRST_CLICK == True:
                            game.dis_highlight_boll(game.X1,game.Y1)
                        game.FIRST_CLICK=True
                        game.X1=x
                        game.Y1=y
#                       print x,y
                        game.highlight_boll(game.X1,game.Y1)
                    if game.matrix.Main_matrix[x,y]==0 and game.FIRST_CLICK==True: 
                        game.SECOND_CLICK=True
                        game.X2=x
                        game.Y2=y
                    if game.FIRST_CLICK==True and game.SECOND_CLICK==True:
                        trace=game.matrix.move(game.X1,game.Y1,game.X2,game.Y2)
#                       print trace
                        if type(trace)!=bool:
                            color=game.matrix.Main_matrix[game.X1,game.Y1]
                            game.matrix.Main_matrix[game.X1,game.Y1]=0
#                           print color
                            game.Draw_bolls()

                            game.matrix.Main_matrix[game.X2,game.Y2]=color

                            game.Move_balls(color,trace)
#                           while True:
#                                pass

                            game.Draw_bolls()

                            disappear_bolls=game.matrix.Check()
                            game.Draw_score()
                            if len(disappear_bolls)>0:
                                game.Boll_disappear(disappear_bolls)

                            else:
                                if game.matrix.get_space()>3:
                                    new_bolls=game.matrix.update()
                                    game.Boll_appear(new_bolls)
    
                                    disappear_bolls=game.matrix.Check()
                                    game.Draw_score()
                                    game.Draw_nextcolors()

                                    if len(disappear_bolls)>0:
                                        game.Boll_disappear(disappear_bolls)
                                else:
                                    game.matrix=Matrix()

#                        print matrix.Main_matrix

                            game.FIRST_CLICK=False
                            game.SECOND_CLICK=False

                            game.Draw_bolls()
                    pass
            else: 
                pass
#            print event 

        game.FPSCLOCK.tick(15)


if __name__=="__main__":
   main()



