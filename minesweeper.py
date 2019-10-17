import math
import random
import pprint
import pygame
from pygame.locals import *                                                 # Required to draw the rectangle
import tkinter as tk
from tkinter import messagebox


class Mine:
    def __init__(self, surface, position):
        self.position = position                                            # Constructor takes the position of mine and surface
        self.surface = surface

    def drawMine(self):
        pygame.draw.circle(self.surface, (255,0,0), self.position, 6)       # This function draws a circle (mine) at specified position, red color and 10 width


def numberMaker(font):
    numbers = []
    for i in range(1,8):
        numbers.append(font.render(str(i), True, (255, 255, 255), (0,0,0))) # This function generates numbers from 1 to 8 and stores in a list
    return numbers


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)                                       # This message code is lifted off internet for user interaction through alert boxes
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def numberMines():
    unique_mines.sort()                                                     # Unique_Mines holds the positions of the mines
    # pprint.pprint(unique_mines)
    for i in range(0,len(unique_mines)):
        zero_array[unique_mines[i][1]+1][unique_mines[i][0]+1] = -1         # Assigns -1 in all the places with a mine in the simulated 2D List
    # pprint.pprint(zero_array)
    print()


def summation(i,j):
    summer = 0
    if(zero_array[i-1][j-1] < 0):
        summer += 1
    if(zero_array[i-1][j] < 0):
        summer += 1                                                         # This function calculates the number of mines in the neighborhood
    if(zero_array[i-1][j+1] < 0):
        summer += 1                                                         
    if(zero_array[i][j-1] < 0):
        summer += 1
    if(zero_array[i][j+1] < 0):
        summer += 1
    if(zero_array[i+1][j-1] < 0):
        summer += 1
    if(zero_array[i+1][j] < 0):
        summer += 1
    if(zero_array[i+1][j+1] < 0):
        summer += 1
    return summer

def locateMines(surface):                                                   # This function calculates neighboring mines for each box
    for i in range(1,21):
        for j in range(1,21):
            if(zero_array[i][j] == -1):                                     # If the box has a mines, continue   
                continue
            else:
                temp = summation(i,j)
                if(temp != 0 or zero_array[i][j] != -1):                    # If the number of mines > 0, put that number in the simulated 2D List
                    zero_array[i][j] = abs(temp)
    # pprint.pprint(zero_array)


def drawGrid(w,rows,surface):
    inBetween = w//rows
    x,y = 0,0                                                               # This function draws the grid on the screen of 'w' width and height and 'rows' number of rows
    for i in range(rows):
        x += inBetween                                                      # inBetween defines the side length of each square of the grid
        y += inBetween
        # pygame.draw.line(surface, (255,255,255), (x,0), (w,x), 1)         # [Cool design] Toggle the comments on these 4 lines to see a lines pattern
        # pygame.draw.line(surface, (255,255,255), (0,y), (y,w), 1)
        pygame.draw.line(surface, (255,255,255), (x,0), (x,w), 1)           # These 2 functions draw a line from left to right
        pygame.draw.line(surface, (255,255,255), (0,y), (w,y), 1)           # and from top to bottom

def putNumbers(surface):                                                    # This function puts the numbers onto corresponding boxes
    for i in range(1,21):
        for j in range(1,21):
            if(zero_array[i][j] != 0 and zero_array[i][j] != -1):           # If it is not empty and not a mine,
                textRect.center = (((j-1)*25)+13, ((i-1)*25)+15)            # Multiply that position with 25 (To locate the centre of the box) and add 13 or 15 for adjustment
                surface.blit(numbers[zero_array[i][j]-1],textRect)          # Shows onto the surface

def drawRect(surface):                                                      # This function adds the overlay over all the boxes
    for i in range(0,20):
        for j in range(0,20):                                               # Repeat for each box on the screen
            temp = [i,j]
            if(temp not in clicked):                                        # If the current box is not clicked yet, add a square on it
                pygame.draw.rect(surface, (255,255,250), Rect(((i*25)+2,(j*25)+2),(20,20)))
            if(temp in right_click and temp not in clicked):                # If it is right-clicked, add an orange square to indicate a found mine
                pygame.draw.rect(surface, (255,153,51), Rect(((i*25)+2,(j*25)+2),(20,20)))

# Kaustubh Eppalapalli
# github.com/akylus
        
def redrawWindow(surface):                                                  # This function continually updates the screen
    surface.fill((0,0,0))                                                   # So here we need to fill the screen with a black color first
    drawGrid(width, rows, surface)                                          # Calling the function to draw the grid
    for i in range(0,num_of_mines):
        m[i].drawMine()                                                     # Calling the Mine class' function to draw the red circle (mine)
    putNumbers(surface)                                                     # Calling the function to put the numbers onto the surface
    drawRect(surface)                                                       # Calling the function to add the squares overlay
    pygame.display.update()                                                 # Update the display

def winChecker():                                                           # This function checks if the player found all the mines correctly
    right_click.sort()
    if(right_click == unique_mines):
        return 1
    else:
        return 0

def cleanup(x,y):                                                           # When an empty space is clicked, this function clears all the nearby empty spaces
    #print(zero_array[y+1][x+1])
    #print(clicked)
    if([x,y] in clicked):                                                   # It's a recursive function
        return
    clicked.append([x,y])                                                   # Add x,y position to list of clicked boxes
    if(zero_array[y+1][x+1] != 0):                                          # Base case: Return if that element is not a zero
        return
    #print(clicked)
    # print(clicked[-1])
    if(x > 0):                                                              # If extreme left is not reached, call to the same function for the box on left
        cleanup(x-1,y)
    if(y > 0):
        cleanup(x,y-1)
    if(x < len(zero_array[1])-3):                                           # Similar condition for all 4 directions
        cleanup(x+1,y)
    if(y < len(zero_array[1])-3):
        cleanup(x,y+1)


def main():
    pygame.init()                                                           # Making below variables global so that they can be accessible everywhere
    global width, rows, num_of_mines, m, textRect, numbers, zero_array, unique_mines, clicked, right_click
    num_of_mines = 40                                                       # Change to alter the number of mines in game
    width = 500
    rows = 20
    zero_array = []                                                         # 2D List simulation of the boxes
    temp = []
    m = []
    unique_mines = []                                                       # Mine positions
    clicked = []                                                            # List to store left-clicks
    right_click = []                                                        # List to store the positions where right-click was pressed
    win = pygame.display.set_mode((width, width))                           # Here, we're setting the display height and width (both of size width)
    pygame.display.set_caption('Mynsweepa')                                 # Set the name
    font = pygame.font.Font('Timea.ttf', 16)
    numbers = numberMaker(font)
    textRect = font.render('1', True, (255, 255, 255), (0,0,0)).get_rect()  # Rendering the font needed for the text
    for i in range(0,22):
        temp = [0]*22
        zero_array.append(temp)                                             # Initialize zero_array with completely zeros

    flag = True                                                             # This flag helps in continually updating the screen

    clock = pygame.time.Clock()                                             # Not necessary, per se.. but meh. Used to set the render speed of screen
    

    for i in range (0,num_of_mines):
        k = random.randint(0,19)
        l = random.randint(0,19)
        temp = [k,l]
        while(temp in unique_mines):                                        # This loop runs to get unique positions for specified number of mines
            k = random.randint(0,19)                                        # and append to list 'm'
            l = random.randint(0,19)
            temp = [k,l]
        unique_mines.append(temp)                                           # Mine(surface_to_be_updated, a tuple with the position of mine) -> This initializes the mine
        temp = Mine(win,((k*25)+13,(l*25)+13))                              # k & l are random numbers generated. Multiply with 25 to go to that corresponding box in the grid
        m.append(temp)                                                      # and the addition of 13 is the caliberation so that the mine is exactly in the box
    # pprint.pprint(unique_mines)
    numberMines()                                                           # Number the mines in the zero_array
    locateMines(win)                                                        # And then locate them on the screen
    while flag:
        pygame.time.delay(50)                                               # not necessary for this program, but still it stays
        clock.tick(10)                                                      # Set clock tick to 10. Controls render speed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                   # If you click X button, window closes gracefully
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:                          # When a button click is observed
                pos = pygame.mouse.get_pos()                                # Get the positon where the click was observed
                x = pos[0]//25
                y = pos[1]//25                                              # Divide by 25 to calculate the box number
                if(event.button == 1):                                      # Check if it is a left-click
                    if(zero_array[y+1][x+1] == -1):                         # Check if it is a mine.
                        clicked.append([x,y])
                        redrawWindow(win)                                   # If mine, bye bye
                        message_box('Uh-Oh!', 'You hit a mine! Play again.')
                        main()                                              # Call to the main function to restart the game
                    if(zero_array[y+1][x+1] == 0):                          # If clicked on an empty space, clear all neighboring empty spaces
                        cleanup(x,y)
                    else:
                        clicked.append([x,y])                               # If a number, just add it to clicked list
                elif(event.button == 3):
                    print([x,y])
                    if([x,y] not in right_click):                           # If not in right_click, add it. Else, remove it
                        right_click.append([x,y])                           # Used to keep track of right clicks and toggle
                    else:
                        right_click.remove([x,y])
            if winChecker():                                                # Check if won
                redrawWindow(win)
                message_box('Yaay!','Congratulations! You found all the mines. Play again!')
                main()
        redrawWindow(win)                                                   # Call to the redraw function to redraw the screen repeatedly
        #drawLayer(win)
main()                                                                      # Call to main function to start the program.
