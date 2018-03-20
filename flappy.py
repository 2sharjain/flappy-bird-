from tkinter import *
import random
import time
import os
import json


def reStart():
    root.destroy()
    os.system('python ut.pyw')
    exit()


def gameOver(score):
    print (score)
    canvas.destroy()
    canvas1 = Canvas(root, width=400, height=500, bg='WHITE')
    canvas1.create_text(200, 200, text='GAME OVER', fill='BLACK',
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
        leaders = leaderboards(name, score)

        for i in leaders:
            canvas1.create_text(200, y, text=i + ': '
                                + str(leaders[i]), fill='BLACK',
                                font=('Comic San MS', 20, 'bold'))
            y = y + 50
        button2.pack_forget()
        entry.pack_forget()

    button1 = Button(root, text='restart', command=reStart)
    button1.pack()
    button2 = Button(root, text='ENTER', command=setName)
    button2.pack()

    root.update()
    root.mainloop()


class Ball:

    def __init__(self, canvas):
        self.i = True
        self.x = 0
        self.y = 1.25
        self.canvas = canvas
        self.id = self.canvas.create_oval(10, 180, 40, 210, fill='RED')
        self.canvas.move(self.id, 30, 0)

    def goDown(self):

        coords = self.canvas.coords(self.id)
        if self.i == True:
            self.canvas.move(self.id, self.x, self.y)
            coords = self.canvas.coords(self.id)

        if coords[3] > 500:
            self.y = 0
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
        self.canvas.move(self.id1, -2, 0)
        self.canvas.move(self.id2, -2, 0)

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


def leaderboards(name, score):
    with open('leaderboards.txt', 'r') as f:
        leaderboards = json.load(f)
    score = int(score)
    print (score)
    arr = []
    for i in leaderboards:
        arr.append(leaderboards[i])
    arr.append(score)

    arr.sort()
    print (arr)
    if score > arr[0]:
        for i in leaderboards:
            if arr[0] == leaderboards[i]:
                m = i
        leaderboards.pop(m)
        scr = arr
        scr.pop(0)
        print (scr)

        leaderboards[name] = score

    with open('leaderboards.txt', 'w') as f:
        json.dump(leaderboards, f)
    print (leaderboards)
    return leaderboards


def gameStart(m, canvas):

    a = 0
    l = 0
    arr = []

    canvas.bind('<Button-1>', ball.bounce)
    while m:
        if a % 110 == 0:
            x = random.randrange(370, 400)
            z = random.randrange(110, 180)
            w = random.randrange(250, 450)
            arr.append(Rectangle(canvas, x, w - z, w))  # new Rectangle object stored in the array
            a = 0
        for i in arr:
            i.move()
            if i.isHit():
                m = 0
                for i in arr:
                    del i

        if arr[0].canvas.coords(arr[0].id1)[2] < 0:
            del arr[0]
            l = l + 1
        ball.goDown()
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
