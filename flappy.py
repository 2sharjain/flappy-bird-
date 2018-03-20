from tkinter import *
import random
import time
import os
import json

def reStart():
    root.destroy()
    os.system('python ll.py')
    
def sortedDict(score,name):
 t=1
 try:   
  with open('leaderboards.txt', 'r') as f:
        leaderboards = json.load(f)
 except:
     leaderboards={"3":"name","2":"name","1":"name"}
 scores=list(leaderboards.keys())
 scores=[int(i) for i in scores]
 for i in scores:
     if score==i:
         leaderboards[str(score)]=name
         t=0
 if t!=0:        
  print(scores)
  scores.append(score)
  print(scores)
  scores.sort()
  if score>scores[0]:
    leaderboards.pop(str(scores[0]))   
  scores.pop(0)
  scores=[str(i) for i in scores]
  for i in scores:
        if str(score)==i:
          leaderboards[i]=name
           
 with open('leaderboards.txt', 'w') as f:
        json.dump(leaderboards, f)
 print (leaderboards)
 return leaderboards        

    


def gameOver(score):
    print (score)
    canvas.destroy()
    canvas1 = Canvas(root, width=400, height=500, bg='WHITE')
    txt1 = canvas1.create_text(200, 200, text='GAME OVER', fill='BLACK',
                        font=('Comic San MS', 50, 'bold'))
    txt = canvas1.create_text(200, 250, text='YOUR SCORE IS :'
                              + str(score), fill='BLACK',
                              font=('Comic San MS', 25, 'bold'))
    canvas1.pack()
    entry = Entry(root)
    entry.pack()

    def setName():
        name = entry.get()
        y = 300
        leaders = sortedDict(score,name)
        scores=list(leaders.keys())
        scores=[int(i) for i in scores]
        scores=sorted(scores,reverse=True)
        for i in scores:
            canvas1.create_text(200, y, text=str(i) + ': '
                                + str(leaders[str(i)]), fill='BLACK',
                                font=('Comic San MS', 20, 'bold'))
            y = y + 50
        button1.pack_forget()
        canvas1.delete(txt)
        entry.pack_forget()

    button1 = Button(root, text='ENTER', command=setName)
    button1.pack()
    button2 = Button(root, text='RESTART', command=reStart)
    button2.pack()

    root.update()
    root.mainloop()


class Ball:

    def __init__(self, canvas):
        self.i = True
        self.x = 0
        self.gravity = 2
        self.canvas = canvas
        self.id = self.canvas.create_oval(10, 180, 40, 210, fill='RED')
        self.canvas.move(self.id, 30, 0)

    def goDown(self):

        coords = self.canvas.coords(self.id)
        if self.i == True:
            self.canvas.move(self.id, self.x, self.gravity)
            coords = self.canvas.coords(self.id)

        if coords[3] > 500:
            self.gravity = 0
            self.i = False

    def bounce(self, event):
        if self.i == True:
            self.canvas.move(self.id, 0, -40)

class Rectangle:

    def __init__(
        self,
        canvas,
        x,
        z,
        w,
        ):
        self.x = x
        self.w = w
        self.z = z
        self.canvas = canvas
        self.id1 = self.canvas.create_rectangle(self.x, 0, self.x + 60,
                self.z, fill='WHITE')
        self.id2 = self.canvas.create_rectangle(self.x, self.w, self.x
                + 60, 500, fill='WHITE')

    def move(self):
        self.canvas.move(self.id1, -2.5, 0)
        self.canvas.move(self.id2, -2.5, 0)

    def isHit(self):
        p = []
        coords1 = self.canvas.coords(self.id1)  # for the rectangle the coordinates are the end points of the diagonal
        coords2 = self.canvas.coords(self.id2)
        p = canvas.coords(ball.id)  # p=[x1,y1,x2,y2]

        if p[0] - coords1[0] <= 60 and p[0] - coords1[0] >= -60 \
            and p[2] >= coords1[0]:  # if it hits the rectangles.    #for the oval(ball) the coordinates are as x1  x2

            if p[1] + 30 >= coords2[1] or p[1] <= coords1[3]:  #                                            y2
                ball.i = False
                return True

def gameStart(m, canvas):

    a = 0
    l = 0
    arr = []
    difficulty=85

    while m:
        ball.goDown()
        for i in arr:
            i.move()        
        if a % difficulty == 0:
            z = random.randrange(110, 180)
            w = random.randrange(200, 450)
            arr.append(Rectangle(canvas, 380, w - z, w))  # new Rectangle object stored in the array
            a = 0
        
        if arr[0].isHit():
                m = 0
                for i in arr:
                    del i
        canvas.bind('<Button-1>', ball.bounce)
        if arr[0].canvas.coords(arr[0].id1)[2] < 0:
            canvas.delete(arr[0].id1)
            canvas.delete(arr[0].id2)
            del arr[0]
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
score = gameStart(1, canvas)
time.sleep(0.25)

gameOver(score)
