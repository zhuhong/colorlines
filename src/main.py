import pygame
import sys
from pygame.locals import *
import time

from Matrix import Matrix

HIGHLIGHTCOLOR = (255, 0, 255) # color of the selected gem's border
BGCOLOR = (170, 190, 255) # background color on the screen
GRIDCOLOR = (0, 0, 255) # color of the game board
GAMEOVERCOLOR = (255, 100, 100) # color of the "Game over" text.
GAMEOVERBGCOLOR = (0, 0, 0) # background color of the "Game over" text.
SCORECOLOR = (85, 65, 0)

#def main():

WINDOWWIDTH = 800  # width of the program's window, in pixels
WINDOWHEIGHT = 600 # height in pixels

GRIDSIZE=64


pygame.init()
FPSCLOCK = pygame.time.Clock()
WINDOWSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
#pygame.display.flip() 

GEMIMAGES = []
for i in range(1,8):
    gemImage = pygame.image.load('%s.png' % i)
#    if gemImage.get_size() != (GEMIMAGESIZE, GEMIMAGESIZE):
#        gemImage = pygame.transform.smoothscale(gemImage, (GEMIMAGESIZE, GEMIMAGESIZE))
    GEMIMAGES.append(gemImage)


#WINDOWSURF.fill(BGCOLOR )
#for i in range(10):
#    pygame.draw.line(WINDOWSURF,GRIDCOLOR,[12+i*64,12],[12+i*64,588],2)
#    pygame.draw.line(WINDOWSURF,GRIDCOLOR,[12,12+64*i],[588,12+64*i],2)

#pygame.image.save(WINDOWSURF,'bg.png')

bg=pygame.image.load('bg.png')
WINDOWSURF.blit(bg,(0,0))

matrix=Matrix()
FIRST_CLICK=False
SECOND_CLICK=False
X1=0
X2=0
Y1=0
Y2=0

def Draw_bolls(WINDOWSURF,GEMIMAGES,matrix):
    rect=(2,2,598,598)
    WINDOWSURF.blit(bg.subsurface(rect),[2,2])

    for i in range(9):
        for j in range(9):
            color=matrix.Main_matrix[i,j]
            if color!=0:
                WINDOWSURF.blit(GEMIMAGES[color-1],[14+i*GRIDSIZE,14+j*GRIDSIZE])
    pygame.display.update()

def Move_balls(WINDOWSURF,GEMIMAGES, matrix, color, trace):
    boll=GEMIMAGES[color-1]
    NOW_X=X1
    NOW_Y=Y1
    NEXT_X=trace[0,0]
    NEXT_Y=trace[1,0]
    # for i in range(trace.shape[1]-1):
    for i in range(trace.shape[1]):
        if NOW_X == NEXT_X:
            for j in range(0,64,8):
                DT=(NEXT_Y-NOW_Y)
                WINDOWSURF.blit(boll,[NOW_X*GRIDSIZE+14,NOW_Y*GRIDSIZE+14+(j+1)*DT])
                pygame.display.update()
                
                rect=(NOW_X*GRIDSIZE+13,NOW_Y*GRIDSIZE+13+(j+1)*DT,56,56)
                WINDOWSURF.blit(bg.subsurface(rect),[NOW_X*GRIDSIZE+13,NOW_Y*GRIDSIZE+13+(j+1)*DT])
                FPSCLOCK.tick(60)
        elif NOW_Y == NEXT_Y:
            for j in range(0,64,8):
                DT=(NEXT_X-NOW_X)
                WINDOWSURF.blit(boll,[NOW_X*GRIDSIZE+14+(j+1)*DT,NOW_Y*GRIDSIZE+14])
                pygame.display.update()
                FPSCLOCK.tick(60)
                rect=(NOW_X*GRIDSIZE+13+(j+1)*DT,NOW_Y*GRIDSIZE+13,56,56)
                WINDOWSURF.blit(bg.subsurface(rect),[NOW_X*GRIDSIZE+13+(j+1)*DT,NOW_Y*GRIDSIZE+13])
        NOW_X=NEXT_X
        NOW_Y=NEXT_Y
        try:
            NEXT_X=trace[0,i+1]
            NEXT_Y=trace[1,i+1]
        except:
            pass

def Boll_jump(WINDOWSURF,GEMIMAGES,color,X,Y):
    START=0
    while True:
        rect=(X*64+13,Y*64+13,56,56)
        WINDOWSURF.blit(bg.subsurface(rect),[X*64+13,Y*64+13])
        pygame.display.update()
        temp=int(abs(25*math.cos(START/25.0*math.pi)))
        im_temp=pygame.transform.smoothscale(GEMIMAGES[color-1], (50,25+temp))
        WINDOWSURF.blit(im_temp,(X*64+14,Y*64+14-temp))
        pygame.display.update()
        START=START+1

def Boll_appear(WINDOWSURF,GEMIMAGES,new_bolls):
#appear 3 bolls in the same time.
    for i in range(0,58,2):
        for j in range(3):
            rect=(new_bolls[j][0]*GRIDSIZE+13,new_bolls[j][1]*GRIDSIZE+13,56,56)
            WINDOWSURF.blit(bg.subsurface(rect),[new_bolls[j][0]*GRIDSIZE+13,new_bolls[j][1]*GRIDSIZE+13])
            im_temp=pygame.transform.smoothscale(GEMIMAGES[new_bolls[j][2]-1],(i,i))
            WINDOWSURF.blit(im_temp,(new_bolls[j][0]*GRIDSIZE+14+29-i/2,new_bolls[j][1]*GRIDSIZE+14+29-i/2))
        pygame.display.update()

        FPSCLOCK.tick(60)

def Boll_disappear(WINDOWSURF,GEMIMAGES,new_bolls):
#disappear bolls in the same time.
    for i in range(48,0,-2):
        for j in range(len(new_bolls)):
            rect=(new_bolls[j][0]*GRIDSIZE+13,new_bolls[j][1]*GRIDSIZE+13,56,56)
            WINDOWSURF.blit(bg.subsurface(rect),[new_bolls[j][0]*GRIDSIZE+13,new_bolls[j][1]*GRIDSIZE+13])
            im_temp=pygame.transform.smoothscale(GEMIMAGES[new_bolls[j][2]-1],(i,i))
            WINDOWSURF.blit(im_temp,(new_bolls[j][0]*GRIDSIZE+16+25-i/2,new_bolls[j][1]*GRIDSIZE+16+25-i/2))
        pygame.display.update()

        FPSCLOCK.tick(60)

def Draw_score(WINDOWSURF,score):
    BASICFONT = pygame.font.Font('freesansbold.ttf', 50)
    scoreImg = BASICFONT.render(str(score), 1, SCORECOLOR) 
    scoreRect = scoreImg.get_rect()
    scoreRect.bottomleft = (660, 480 )
    rect=(630,400,120,100)
    WINDOWSURF.blit(bg.subsurface(rect),[630,400])
    WINDOWSURF.blit(scoreImg, scoreRect)

def Draw_label(WINDOWSURF):
    BASICFONT = pygame.font.Font('freesansbold.ttf', 50)
    titleImg=BASICFONT.render("SCORE",True,SCORECOLOR)
    nextImg=BASICFONT.render("NEXT",True,SCORECOLOR)
    titleRect=titleImg.get_rect()
    nextRect=nextImg.get_rect()
    titleRect.bottomleft = (610, 400 )
    nextRect.bottomleft= (630,100)
    WINDOWSURF.blit(titleImg, titleRect)
    WINDOWSURF.blit(nextImg, nextRect)


def Draw_nextcolors(WINDOWSURF,GEMIMAGES,next_colors):
    rect=(610,120,190,80)
    WINDOWSURF.blit(bg.subsurface(rect),[610,120])
    for j in range(3):
        color=next_colors[j]
        WINDOWSURF.blit(GEMIMAGES[color-1],(610+j*64,120))




Draw_bolls(WINDOWSURF,GEMIMAGES,matrix)
Draw_score(WINDOWSURF,matrix.score)
Draw_label(WINDOWSURF)
Draw_nextcolors(WINDOWSURF,GEMIMAGES,matrix.next_colors)

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
                if matrix.Main_matrix[x,y]!=0:
                    FIRST_CLICK=True
                    X1=x
                    Y1=y
#                    print x,y
                if matrix.Main_matrix[x,y]==0 and FIRST_CLICK==True: 
                    SECOND_CLICK=True
                    X2=x
                    Y2=y
                if FIRST_CLICK==True and SECOND_CLICK==True:
                    trace=matrix.move(X1,Y1,X2,Y2)
#                    print trace
                    if type(trace)!=bool:
                        color=matrix.Main_matrix[X1,Y1]
                        matrix.Main_matrix[X1,Y1]=0
#                        print color
                        Draw_bolls(WINDOWSURF,GEMIMAGES,matrix)

                        matrix.Main_matrix[X2,Y2]=color

                        Move_balls(WINDOWSURF,GEMIMAGES,matrix,color,trace)
#                        while True:
#                            pass

                        Draw_bolls(WINDOWSURF,GEMIMAGES,matrix)

                        disappear_bolls=matrix.Check()
                        Draw_score(WINDOWSURF,matrix.score)
                        if len(disappear_bolls)>0:
                            Boll_disappear(WINDOWSURF,GEMIMAGES,disappear_bolls)

                        else:
                            if matrix.get_space()>3:
                                new_bolls=matrix.update()
                                Boll_appear(WINDOWSURF,GEMIMAGES,new_bolls)
    
                                disappear_bolls=matrix.Check()
                                Draw_score(WINDOWSURF,matrix.score)
                                Draw_nextcolors(WINDOWSURF,GEMIMAGES,matrix.next_colors)

                                if len(disappear_bolls)>0:
                                    Boll_disappear(WINDOWSURF,GEMIMAGES,disappear_bolls)
                            else:
                                matrix=Matrix()

#                        print matrix.Main_matrix

                        FIRST_CLICK=False
                        SECOND_CLICK=False

                        Draw_bolls(WINDOWSURF,GEMIMAGES,matrix)
                pass
        else: 
            pass
#            print event 

    FPSCLOCK.tick(30)


#if __name__=="__main__":
#    main()



