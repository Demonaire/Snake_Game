# Extra Credit
#2 No Direction reversal implemented (2 Points)
#3 Restart Functionality added (5 Points)
#4 Optimize the game speed (1 Point)
#6 Multispeed  (2 Points)
# Scoring added  (Points to be decided)

#Problem A

import turtle
import random
class Game:
    '''
    Purpose: Main Game class resposible for display, controls and gameplay
    Instance variables: speed: Speed of snake
                        pen_score: Score display turtle object
                        pen_display: Controls display turtle object
                        player: Snake class object, reposible for player snake interaction with game
                        pellet: Food class object, resposible for food interaction with snake

    Methods: 
            __init__: main game method that is resposible for initiating display screen, monitoring key presses and keeping the gameloop running
            gameloop: main game loop that ensures game keeps running
             score_display: Displays score of player
             low_speed: makes refresh rate 300 ms, lowest snake movement
             med_speed: makes refresh rate 200 ms, keepind snake movement medium
             high_speed: makes refresh rate 100 ms, highest snake movement
             restart: restarts the game, resetting all parameters
             game_over: Displays Game Over message
             menu_display: Displays controls and game title
    '''
    def __init__(self):
        #Setup 700x700 pixel window (changed to put my menu in the game)
        turtle.setup(800, 800)
        #Bottom left of screen is (-40, -40), top right is (640, 640) (Changed to put my menu ingame)
        turtle.setworldcoordinates(-90, -90, 690, 690)
        cv = turtle.getcanvas()
        cv.adjustScrolls()
        #Ensure turtle is running as fast as possible
        turtle.hideturtle()       
        turtle.delay(0)
        turtle.tracer(0,0) 
        turtle.speed(0)
        #Draw the board as a square from (0,0) to (600,600)
        for i in range(4):
            turtle.forward(600)
            turtle.left(90)
        self.speed=200
        self.pen_score=turtle.Turtle()
        self.pen_score.goto(0,600)
        self.pen_display=turtle.Turtle()
        self.player=Snake(x = 315, y = 315, color = 'green')
        self.pellet=Food()
        self.menu_display()

        self.gameloop()
        turtle.onkeypress(self.restart, 'r')
        turtle.onkeypress(self.player.go_down, 'Down')
        turtle.onkeypress(self.player.go_up, 'Up')
        turtle.onkeypress(self.player.go_right, 'Right')
        turtle.onkeypress(self.player.go_left, 'Left')
        turtle.onkeypress(self.low_speed, '1')
        turtle.onkeypress(self.med_speed, '2')
        turtle.onkeypress(self.high_speed, '3')
        turtle.listen()
        turtle.mainloop()

    def gameloop(self):
        if self.player.snake_dead()==False:
            self.player.move(self.pellet)
            self.score_display()
            turtle.ontimer(self.gameloop,self.speed)
            turtle.update()
        elif self.player.snake_dead()==True:
            self.game_over()


    #Display Score
    def score_display(self):
        self.pen_score.clear()
        self.pen_score.write(f'Score: {(len(self.player.segments)-1)}')

    #Speed Functions
    def low_speed(self):
        self.speed=300
    
    def med_speed(self):
        self.speed=200
    
    def high_speed(self):
        self.speed=100

    #Restart Function

    def restart(self):
        self.player.restart()
        self.pellet.restart()
        self.pen_score.clear()
        turtle.clearscreen()

        #Ensure turtle is running as fast as possible
        turtle.hideturtle()       
        turtle.delay(0)
        turtle.tracer(0,0) 
        turtle.speed(0)
        #Draw the board as a square from (0,0) to (600,600)
        for i in range(4):
            turtle.forward(600)
            turtle.left(90)
        self.speed=200
        self.pen_score=turtle.Turtle()
        self.pen_score.goto(0,600)
        self.player=Snake(x = 315, y = 315, color = 'green')
        self.pellet=Food()
        self.menu_display()
        self.gameloop()
        turtle.onkeypress(self.restart, 'r')
        turtle.onkeypress(self.player.go_down, 'Down')
        turtle.onkeypress(self.player.go_up, 'Up')
        turtle.onkeypress(self.player.go_right, 'Right')
        turtle.onkeypress(self.player.go_left, 'Left')
        turtle.onkeypress(self.low_speed, '1')
        turtle.onkeypress(self.med_speed, '2')
        turtle.onkeypress(self.high_speed, '3')
        turtle.listen()
        turtle.mainloop()

    #Display Game Over Message 
    def game_over(self):
        pen_over=turtle.Turtle()
        pen_over.goto(315,315)
        pen_over.write('Game Over', move=False, align='center', font=('Arial', 30, 'bold'))

    def menu_display(self):
        self.pen_display.setpos(315,600)
        self.pen_display.clear()
        self.pen_display.write('Snake Game', move=False, align='center', font=('Arial', 15, 'bold'))
        self.pen_display.setpos(500,680)
        self.pen_display.write('Menu', move=False, align='left', font=('Arial', 12, 'bold'))
        self.pen_display.setpos(500,660)
        self.pen_display.write('1: Slow Speed Snake', move=False, align='left', font=('Arial', 8, 'normal'))  
        self.pen_display.setpos(500,640)
        self.pen_display.write('2: Medium Speed Snake', move=False, align='left', font=('Arial', 8, 'normal'))
        self.pen_display.setpos(500,620)
        self.pen_display.write('3: Fast Speed Snake', move=False, align='left', font=('Arial', 8, 'normal'))
        self.pen_display.setpos(500,600)
        self.pen_display.write('R: Restart Game', move=False, align='left', font=('Arial', 8, 'normal')) 

class Snake:

    '''
    Purpose: Snake object of the game, in control of a human player
    Instance variables: x: x coordinate of head of snake
                        y: y coordinate of head of snake
                        color: color of snake
                        segments: length of snake represented by a list in which each item is a turtle object
                        cord: list maintaining coordinates of each segment. Vital to see if snake hit itself
                        vx: x direction vilocity of snake, +ive is right, -ive is left
                        vy: y direction velocity of snake, +iv is upward, -ive is downward
    Methods: 
            __init__: intializes snake with one segment, and horizontal speed of one box per refresh cycle
            grow: increases size of snake by one segment
            move: head moves in direction of velocity depending on values of vx & vy. Also each segment gets coordinates of the segment infront of it
                    simulating snake movement. Incase head comes on food coordinate, spawn a new food at random place and assign previous food coordinates
                    to head
            go_down: makes snake go down if down key is pressed,  only executes when snake is traveling on x axis
            go_up: makes snake go up if up key is pressed,  only executes when snake is traveling on x axis
            go_right: makes snake go right if right key is pressed,  only executes when snake is traveling on y axis
            go_left: makes snake go left if left key is pressed,  only executes when snake is traveling on y axis

            restart:reiniialize snake parameters for restart in Game class
            snake_dead: return True if snake hit itself ot collides with wall, else returns False
    '''
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        self.color=color
        self.segments=[]
        #Keeps record of all snake segments coordinates
        self.cord=[]
        self.vx=30
        self.vy=0
        
        self.grow()

    def grow(self):
        #code to append segments list with new turtle objects
        self.t=turtle.Turtle()
        self.t.speed(0)
        self.t.fillcolor(self.color)
        self.t.shape("square")
        self.t.shapesize(1.5,1.5,1)
        self.t.penup()
        self.t.setpos(x=self.x,y=self.y)
        self.segments.append(self.t)
        self.cord.append(self.t.pos())
    
    def move(self,pellet):
        self.x+=self.vx
        self.y+=self.vy

        #if eat food, grow in size and spawn a new food pellet
        if (self.x==pellet.x and self.y==pellet.y):
            self.grow()
            pellet.spawn()
        else:
            i=0
            for point in self.segments:
                if i==(len(self.segments)-1):
                    point.setpos(self.x,self.y)
                else:
                    point.setpos(self.segments[i+1].pos()[0],self.segments[i+1].pos()[1])
                self.cord[i]=point.pos()
                i+=1

    #Ensured Snake no direction reversal
    def go_down(self):
        if self.vy==0:
            self.vx=0
            self.vy=-30
    
    def go_up(self):
        if self.vy==0:
            self.vx=0
            self.vy=30
    
    def go_right(self):
        if self.vx==0:
            self.vx=30
            self.vy=0
    
    def go_left(self):
        if self.vx==0:
            self.vx=-30
            self.vy=0

    #clear on restart
    def restart(self):
        self.x=315
        self.y=315
        self.color="green"
        self.segments=[]
        self.cord=[]
        self.grow()
        self.t.clear()

    def snake_dead(self):
        if self.segments[-1].xcor()>585 or self.segments[-1].xcor()<15:
            return True
        elif self.segments[-1].ycor()>585 or self.segments[-1].ycor()<15:
            return True
        elif len(self.segments)>4 and self.segments[-1].pos() in self.cord[0:len(self.cord)-2]:
            return True
        else:
            return False

#Problem B
class Food:

    '''
    Purpose: Food object that snake eats to grow
    Instance variables: x: x coordinate of food
                        y: y coordinate of food
                        t: turtle object representing food on turtle screen

    Methods: __init__: initializes a food pellet at random location of turtle screen
            spawn: food spawns at a new random location in turtle screen
            restart: reinitializes food to facilitate Game class restart
    '''
    def __init__(self):
        self.x=15+30*random.randint(0,19)
        self.y=15+30*random.randint(0,19)
        self.t=turtle.Turtle()
        self.t.speed(0)
        self.t.fillcolor('red')
        self.t.shape("circle")
        self.t.shapesize(1,1,1)
        self.t.penup()
        self.t.setpos(self.x,self.y)
    
    def spawn(self):
        self.x=15+30*random.randint(0,19)
        self.y=15+30*random.randint(0,19)
        self.t.setpos(self.x,self.y)

    #clear on restart
    def restart(self):
        self.t.clear()
Game()