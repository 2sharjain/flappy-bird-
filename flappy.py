from tkinter import *
import random
import time
   
def gameOver(score):
    canvas.destroy()
    canvas1=Canvas(root,width = 400,height = 500,bg = "BLACK",bd = 0, highlightthickness = 0)
    canvas1.create_text(200,200,text="GAME OVER",fill="WHITE",font=("Comic San MS",50,"bold"))
    canvas1.create_text(200,250,text=("YOUR SCORE IS : "+str(score)),fill="WHITE",font=("Comic San MS",20,"bold"))
    ball1=Ball(canvas1)
    canvas1.pack()
    root.update()
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
        self.id2 = self.canvas.create_rectangle(self.x,500,self.x+60,self.w,fill = "WHITE")
        
    def move(self):
        self.canvas.move(self.id1,-2,0)
        self.canvas.move(self.id2,-2,0)
    def isHit(self):
        p=[]
        coords1 = self.canvas.coords(self.id1)
        coords2 = self.canvas.coords(self.id2) 
        p = canvas.coords(ball.id)
        if p[0]-coords1[0]<= 60 and p[0]-coords1[0]>=-60 and p[0]+30>=coords1[0]: #if it hits the rectangles
            if p[1]+30 >= coords2[1] or p[3]-30<=coords1[3]:
                ball.i=False
                return True



            
def gameStart(m):
 a=0
 l=0
 arr=[]
 j=0
 while m:

    x = random.randrange(370,400)
    z = random.randrange(110,180)
    w = random.randrange(250,450)
    if a%110==0:
        arr.append(Rectangle(canvas,x,w-z,w)) #rectangle objects stored in the array
        
    for i in range(len(arr)):
            arr[i].move()
            if(arr[i].isHit()):
              m=0
    if arr[j].canvas.coords(arr[0].id1)[2]<0:
         arr.pop(j)
         print("deleted")
         l=l+1
    canvas.bind("<Button-1>",ball.bounce)
    ball.goDown()
    root.update_idletasks()
    root.update()
    a=a+1  
    time.sleep(0.01)
 return l





root = Tk()
root.title("ALPHA")
root.resizable(0,0)
root.wm_attributes("-topmost",1)
canvas = Canvas(root,width = 400,height = 500,bg = "BLACK",bd = 0, highlightthickness = 0)
canvas.pack()
root.update()    
ball = Ball(canvas)
score=gameStart(m=1)
time.sleep(0.3)
gameOver(score)
