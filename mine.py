import pygame
import random
import sys
from tkinter import *
from tkinter import messagebox

#easy          size = 9   mines = 10
#intermediate  size = 16  mines = 40
#expert        size = 22  mines = 100

size = 10
window_size = 600
grid_size = window_size//size
mines = 10


white = (255,255,255)
black = (0,0,0)
green = (20,200,20)
gray = (140,140,140)


def main():
    global screen,clock
    pygame.init()
    pygame.font.init()
    global num_font
    num_font = pygame.font.SysFont("Helvetica",round(grid_size*0.75))
    #myfont = pygame.font.SysFont('Comic Sans MS', round(grid_size*0.75))
    
    screen = pygame.display.set_mode((window_size,window_size))
    pygame.display.set_caption("Minesweeper")
    clock = pygame.time.Clock()
    screen.fill(white)
    

    global shown,full,remaining
    start = [[0]*size for i in range(size)]
    shown = [["-"]*size for i in range(size)]
    full = addnums(addmines(start,mines))
    remaining = size*size - mines
    #printmatrix(shown)
    boardOverlay()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                #printmatrix(shown)
                
                if event.button == 1:
                    gridPos(x//grid_size,y//grid_size)
                    
                elif event.button == 3:
                    addFlag(x//grid_size,y//grid_size)

                    
                
                
        #a,b = input().split()
        #printmatrix(reveal(shown,full,int(a),int(b)))
            '''   
            if full[int(a)][int(b)] == -1:
                print("you lose")
                break
            remaining -= 1
            if remaining == 0:
                print("you win")
                break
            '''
        pygame.display.flip()
        clock.tick(60)


def boardOverlay():
    for x in range(window_size//grid_size):
        for y in range(window_size//grid_size):
            rect = pygame.Rect(x*grid_size,y*grid_size,
                               grid_size,grid_size)
            pygame.draw.rect(screen,gray,rect)
            pygame.draw.rect(screen,black,rect,1)
            

def valid(x,y):
    return (x>=0 and x<size and y>=0 and y<size)

def addmines(matrix,mines):
    while (mines>0):
        x = random.randint(0,size-1)
        y = random.randint(0,size-1)
        if matrix[x][y] != -1:
            matrix[x][y] = -1
            mines -= 1
    return matrix
            
def addnums(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == -1:
                pass
            else:
                count = 0
                for a in range (-1,2):
                    for b in range (-1,2):
                        if valid(i+a,j+b):
                            if matrix[i+a][j+b] == -1:
                                count +=1
                matrix[i][j] = count
    return matrix


def printmatrix(matrix):
    for i in range(len(matrix)):
        string = ""
        for j in range(len(matrix[i])):
            x = str(matrix[i][j])
            if len(x) < 2:
                string += " "
            string += " " + str(matrix[i][j])
        print(string)
    print("\n\n\n")


def reveal(matrix,new,x,y):
    square = new[x][y]
    if square == 0 and matrix[x][y] == "-":
        matrix[x][y] = square
        for i in range (-1,2):
            for j in range (-1,2):
                if valid(x+i,y+j):
                  #  if new[x+i][y+j] == 0 and matrix[x+i][y+j] == "-":
                     matrix = reveal(matrix,new,x+i,y+j)
    elif matrix[x][y] == "-":
        matrix[x][y] = square
    return matrix


def gridPos(x,y):
    square = full[x][y]
    drawNum(x,y,square)
    
    if square == 0 and shown[x][y] == "-":
        shown[x][y] = square
        for i in range (-1,2):
            for j in range (-1,2):
                if valid(x+i,y+j):
                    gridPos(x+i,y+j)
    elif shown[x][y] == "-":
        shown[x][y] = square
    if noSquaresLeft(shown):
        winningScreen()
                    

def drawNum(x,y,square):
    if square == 0:
        num = " "
    elif square == -1:
        showMines()
    else:
        num = str(square)
        
    rect = pygame.Rect(x*grid_size+1,y*grid_size+1,
                        grid_size-2,grid_size-2)
    pygame.draw.rect(screen,white,rect)
    
    textsurface = num_font.render(num, False, black)
    screen.blit(textsurface,((x+0.3)*grid_size,(y+0.1)*grid_size))
    pygame.display.update()
    #pygame.time.delay(50)


def addFlag(x,y):
    if shown[x][y] == "-":
        textsurface = num_font.render("F", False, black)
        screen.blit(textsurface,((x+0.3)*grid_size,(y+0.1)*grid_size))

def noSquaresLeft(screen):
    count = 0
    for i in range(len(screen)):
        for j in range(len(screen[i])):
            if screen[i][j] == "-":
                count += 1
    if count <= mines:
        return True


def winningScreen():
    root = Tk().wm_withdraw()
    MsgBox = messagebox.askquestion(
        'You Won!', 'Do you want to play again?', icon='question')
    if MsgBox == 'yes':
        main()
    else:
        pygame.quit()
        #sys.exit()


def showMines():
    for i in range(len(full)):
        for j in range(len(full[i])):
            if full[i][j] == -1:
                
                r = pygame.Rect(i*grid_size,j*grid_size,grid_size,grid_size)
                pygame.draw.rect(screen,gray,r)
                pygame.draw.rect(screen,black,r,1)
                
                textsurface = num_font.render("*", False, black)
                screen.blit(textsurface,((i+0.3)*grid_size,(j+0.1)*grid_size))
                pygame.display.update()
                pygame.time.wait(250)
    losingScreen()
                

def losingScreen():
    root = Tk().wm_withdraw()
    MsgBox = messagebox.askquestion(
        'OOPS YOU BLEW UP THE MINES!', 'Do you want to play again?', icon='question')
    if MsgBox == 'yes':
        main()
    else:
        pygame.quit()
        #sys.exit()
                    
if __name__ == "__main__":
    main()



        
