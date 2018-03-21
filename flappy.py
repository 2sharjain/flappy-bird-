
from tkinter import *
import random
import time
import os
import json

'''Class GameOver is the class with methods which make the game over window and the present the high scores'''

class GameOver:
    def __init__(self,score,canvas): #make the gameover window and displayes the scores.
        self.score=score
        self.leaderboards={}   #dictionary containing the high scores.
        print (score)
        canvas.destroy()
        
        self.canvas1 = Canvas(root, width=400, height=500, bg='WHITE')
    
        self.canvas1.create_text(200, 200, text='GAME OVER', fill='BLACK',
                        font=('Comic San MS', 50, 'bold'))
    
        self.canvas1.create_text(200, 250, text='YOUR SCORE IS :'
                              + str(score), fill='BLACK',
                              font=('Comic San MS', 25,))
        self.canvas1.pack()
        self.entry = Entry(root)
        self.entry.pack()
        self.button1 = Button(root, text='ENTER', command=self.displayScores)
        self.button1.pack()
        self.button2 = Button(root, text='RESTART', command=self.reStart)
        self.button2.pack()

        root.update()
        root.mainloop()
        

    def displayScores(self):
        name = self.entry.get()
        y = 300
        leaders = self.leaderBoard(name)
        scores=list(leaders.keys())  #scores as strings
        scores=[int(i) for i in scores] #scores as integers
        scores=sorted(scores,reverse=True) #reverse sorting 
        for i in scores:
            self.canvas1.create_text(200, y, text=str(i) + ': '       #displaying scores on the canvas in decreasing order
                                + str(leaders[str(i)]), fill='BLACK',
                                font=('Comic San MS', 20, 'bold'))
            y = y + 50
        self.button1.pack_forget() #removes the enter button once the leaderboard is displayed.
        self.entry.pack_forget()   #removes the text field once the leaderboard is displayed.
        

    def reStart(self):   #restarts the game
        root.destroy()
        os.system("python flappy.py")

        
    def leaderBoard(self,name):   #stores the scores and the corresponding names as a dictionary in a json file.
       t=1                        # t represents if the score is equal to any scores the leaderboars. if t==0, score is already in the leaderboard.
       try:   
         with open('leaderboards.txt', 'r') as f:
           leaderboards = json.load(f)
       except:
         leaderboards={"3":"name","2":"name","1":"name"}  #the scores are the keys and the names are the values.
       scores=list(leaderboards.keys())
       scores=[int(i) for i in scores]        #list of scores in type int.
       
       for i in scores:                       #checks if the score is already in the current leaderboard.
         if self.score==i:
          leaderboards[str(self.score)]=name
          t=0
          
       if t!=0:                               #if the score is not equal to any scores.
         print(scores) 
         scores.append(self.score)            
         print(scores)
         
         scores.sort()
         
         if self.score>scores[0]:
           leaderboards.pop(str(scores[0]))
           
         scores.pop(0)                       #deletes the first element of the appended scores list.
         scores=[str(i) for i in scores]
         
       for i in scores:                      #if the score is not deleted(it is high enough to be on leaderboard or the scores list)
         if str(self.score)==i:
           leaderboards[i]=name              #the score is stored in the dictionary.
           
       with open('leaderboards.txt', 'w') as f:
        json.dump(leaderboards, f)
        
       print (leaderboards)
       return leaderboards     

'''ball object belongs to the class Ball and it defines the actions and parameters of the ball(bird) which is used in the game'''

class Ball:

    def __init__(self, canvas): #makes the ball appear on the canvas
        self.willMove = True    #when ball hits the rectangle this parameter will be False
        self.x = 0             #x co-ordinate speed of the ball. will be always zero.
        self.gravity = 2       #the gravity checks the rate of falling down.  
        self.canvas = canvas
        self.id = self.canvas.create_oval(10, 180, 40, 210, fill='RED') #tkinter id of the oval(ball)
        self.canvas.move(self.id, 30, 0)   #places the ball in the position during the starting of the game.

    def goDown(self):     #ball falls down. it is called in the while loop in the function gameStart

        coords = self.canvas.coords(self.id) #the current co-ordinates of the ball.returns a tuple
        
        if self.willMove == True:
            self.canvas.move(self.id, self.x, self.gravity)
            coords = self.canvas.coords(self.id)

        if coords[3] > 500:   #if it hits the bottom of screen
            self.gravity = 0
            self.willMove = False

    def bounce(self, event): #bounces as the mouse button is clicked
        if self.willMove == True:
            self.canvas.move(self.id, 0, -40)


''' class of rectangle objects created in the game through which the ball bounces'''            

class Rectangle:   

    def __init__(
        self,
        canvas,
        x,
        z,
        y,
        ):
        self.x = x
        self.y = y
        self.z = z
        self.canvas = canvas
        self.id1 = self.canvas.create_rectangle(self.x, 0, self.x + 60,  #the rectangle object consists of two rectangles created in the same x 
                self.z, fill='WHITE')                                    # with the space between them equal to z and the y coord of the lower rect as y
        self.id2 = self.canvas.create_rectangle(self.x, self.y, self.x   #breadth of the rectangle is 60
                + 60, 500, fill='WHITE')

    def move(self):
        self.canvas.move(self.id1, -2.1, 0)
        self.canvas.move(self.id2, -2.1, 0)

    def isHit(self):
        p = []
        coords1 = self.canvas.coords(self.id1)  #coordinates of rectangle(upper)
        coords2 = self.canvas.coords(self.id2)  #coordinates of rectangle(lower)
        p = canvas.coords(ball.id)  #co-ordinates of the ball

        if p[0] - coords1[0] <= 60 and p[0] - coords1[0] >= -60 and p[2] >= coords1[0]:  # if the ball hits the rectangles.     

            if p[1] + 30 >= coords2[1] or p[1] <= coords1[3]: 
                ball.willMove = False
                return True

def gameStart(game, canvas):

    a = 0
    l = 0
    rectObjects = []
    difficulty=85

    while game:
        ball.goDown()
        
        for i in rectObjects:
            i.move()
            
        if a % difficulty == 0:
            z = random.randrange(110, 180)
            w = random.randrange(200, 450)
            rectObjects.append(Rectangle(canvas, 380, w - z, w))  # new Rectangle object stored in the array
            a = 0
        
        if rectObjects[0].isHit():
                game = False
                for i in rectObjects:
                    del i
                    
        canvas.bind('<Button-1>', ball.bounce)
        
        if rectObjects[0].canvas.coords(rectObjects[0].id1)[2] < 0:
            canvas.delete(rectObjects[0].id1)
            canvas.delete(rectObjects[0].id2)
            del rectObjects[0]
            l = l + 1
            if l>10:
                difficulty=80
            if l>20:
                difficulty=75
                
        root.update()
        a = a + 1
        time.sleep(0.01)
    return l  # returns the score i.e the number of deleted rectangles


root = Tk()
root.title('ALPHA')
root.resizable(0, 0)
canvas = Canvas(root, width=400, height=500, bg='ORANGE')
canvas.pack()
ball = Ball(canvas)
score = gameStart(True, canvas)
time.sleep(0.25)
gameOver=GameOver(score,canvas)
