from tkinter import *
import random
import time
   
def gameOver(score,best):
    canvas.destroy()
    canvas1=Canvas(root,width = 400,height = 500,bg = "BLACK",bd = 0, highlightthickness = 0)
    canvas1.create_text(200,200,text="GAME OVER",fill="WHITE",font=("Comic San MS",50,"bold"))
    canvas1.create_text(200,250,text=("YOUR SCORE IS : "+str(score)),fill="WHITE",font=("Comic San MS",20,"bold"))
    canvas1.create_text(200,450,text=("BEST : "+str(best)),fill="WHITE",font=("Comic San MS",15,"bold"))
    canvas1.pack()
    #root.update()
    root.mainloop()

    
class Ball:
    def __init__(self,canvas):
        self.i = True
        self.x=0
        self.y=1.25
        self.canvas = canvas
        self.id = self.canvas.create_oval(10,180,40,210,fill = "RED")
        self.canvas.move(self.id,30,0)
    def goDown(self):
        coords = self.canvas.coords(self.id)
        if self.i == True:
            self.canvas.move(self.id,self.x,self.y)
            coords = self.canvas.coords(self.id)
        if coords[3]>500:
            self.y=0
            self.i = False

    def bounce(self,event):
        if (self.i== True) :
          self.canvas.move(self.id,0,-40)      


        
class Rectangle:
    def __init__(self,canvas,x,z,w):
        self.x = x
        self.w = w
        self.z = z
        self.canvas = canvas
        self.id1 = self.canvas.create_rectangle(self.x,0,self.x+60,self.z,fill ="WHITE")
        self.id2 = self.canvas.create_rectangle(self.x,self.w,self.x+60,500,fill = "WHITE")
        
    def move(self):
        self.canvas.move(self.id1,-2,0)
        self.canvas.move(self.id2,-2,0)
    def isHit(self):
        p=[]
        coords1 = self.canvas.coords(self.id1)   # for the rectangle the coordinates are the end points of the diagonal  
        coords2 = self.canvas.coords(self.id2)   
        p = canvas.coords(ball.id) #p=[x1,y1,x2,y2]                                                                                                        y1
        if p[0]-coords1[0]<= 60 and p[0]-coords1[0]>=-60 and p[2]>=coords1[0]: #if it hits the rectangles.    #for the oval(ball) the coordinates are as x1  x2
            if p[1]+30 >= coords2[1] or p[1]<=coords1[3]:                                                     #                                            y2
                ball.i=False
                return True



            
def gameStart(m):
 a=0
 l=0
 arr=[]
 while m:
    if a%110==0:
        x = random.randrange(370,400)
        z = random.randrange(110,180)
        w = random.randrange(250,450)        
        arr.append(Rectangle(canvas,x,w-z,w)) #new Rectangle object stored in the array
        a=0
    for i in arr:
            i.move()
            if(i.isHit()):
              m=0
    if arr[0].canvas.coords(arr[0].id1)[2]<0:
         del arr[0]
         l=l+1
    canvas.bind("<Button-1>",ball.bounce)
    ball.goDown()
    root.update_idletasks()
    root.update()
    a=a+1  
    time.sleep(0.01)
 return l #returns the score i.e the number of deleted rectangles


with open("bestscore.txt","r") as bs:
   try: 
    best=int(bs.readline())
   except:
    best=0
root = Tk()
root.title("ALPHA")
root.resizable(0,0)
canvas = Canvas(root,width = 400,height = 500,bg = "BLACK",bd = 0, highlightthickness = 0)
canvas.pack()   
ball = Ball(canvas)
score=gameStart(m=1)
time.sleep(0.25)
if score>best:
    best=score
    with open("bestscore.txt","w") as bs:
     bs.truncate()
     bs.write(str(best))
gameOver(score,best)
