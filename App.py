# TO-DO:-
    # 1. Doesn't predict after refreshing of the dataset.
    # 2. train data on go: collect at least 5-6 data and then train 
    # 3. improve performance
    # 4. More features.
    # 5. test it


from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import Font
from PIL import ImageTk, Image, ImageDraw

import cv2
import threading
import numpy as np
import tensorflow as tf

import Dataset
import Model
import time


# ----------------------------------------------------------------- #

class GuiLoop():
    def __init__(self, root, master, parameters=None, count=True, speed=100):
        self.Brk = False
        self.root = root
        self.master = master
        self.para = parameters
        self.count = count
        self._reset = count
        self.speed = speed
        self.task = ''
        self._Loop()
    
    def __call__(self, root, master, parameters=None, count=True, speed=100):
        self.Brk = False
        self.root = root
        self.master = master
        self.para = parameters
        self.count = count
        self._reset = count
        self.speed = speed
        self.task = ''
        self.StopLoop()
        self._Loop()

    def config(self, **options):
        self.master = options.get('master')
        self.count = options.get('count',True)
        self._reset = options.get('count',True)
        self.speed = options.get('speed')

    def _Loop(self):
        if self.__run__() and self.master!=None and not self.Brk:
            if self.para:self.master(self.para)
            else: self.master()
            self.task = self.root.after(self.speed, self._Loop)

    def __run__(self):
        if self.count==True and type(self.count)==bool:
            return True
        elif self.count==False and type(self.count)==bool:
            return False
        if type(self.count)==int:
            if self.count>0:
                self.count-=1
                return True
            else:
                return False
        else:
            print("\nInvaild Entry count can't be {} ,\
                 Either boolean or int".format(self.count))
            
    def StopLoop(self, evt=None):
        self.root.after_cancel(self.task)
        self.count = self._reset
        self.master = None
        self.para = None

    def Pause(self, evt=None):
        self.Brk=True
        self.root.after_cancel(self.task)
        
    def Play(self, evt=None):
        self.Brk=False
        self._Loop()

# Loadinf animation
class Loading_Ani(Canvas):
    def __init__(self, root=None, speed=100, size=80, color="#333", bg=None):
        Canvas.__init__(self, root, bg=bg)
        self.config(self, highlightthickness=0, width=size, height=size)
        self.create_text(size/2,(size/2), text="◜",fill=color, tags="Loading", font=Font(size=size+8))
        
        self.__ = 0
        self._loop = GuiLoop(self, self.Magic, speed=speed)

    def Magic(self, evt=None):
        if self.__==0:
            self.itemconfig("Loading", text="◜")
            self.__=1
        elif self.__ ==1:
            self.itemconfig("Loading", text="◝")
            self.__=2
        elif self.__ ==2:
            self.itemconfig("Loading", text="◞")
            self.__=3
        elif self.__ ==3:
            self.itemconfig("Loading", text="◟")
            self.__=0
        
    def hide(self):
        self._loop.Pause()
        self.itemconfig('Loading', state='hidden')

    def show(self):
        self._loop.Play()
        self.itemconfig('Loading', state='normal')


# ----------------------------------------------------------------- #

graph = ''
model = ''

def load_model():
    global model, graph
    graph = tf.get_default_graph()
    model = tf.keras.models.load_model("Digit_Reader1.h5")

load_model()

class Draw_Pad(Canvas):
    def __init__(self, master, Width = 20, color = "white" ,*ag, **kw):
        Canvas.__init__(self, master, *ag, **kw)
    
        self.config(bg="#333", highlightthickness=1)
        self.master = master
        self.width = Width
        self.color = color
        self.train_count = 0
        self.ThreadsL = []
        self.Loading = False

        self.Img = Image.new( "RGB", ( 300,300 ), (0,0,0) )
        self.get_draw = ImageDraw.Draw( self.Img )

        self.model = model

        self.display_win()

        self.master.bind("<Shift-Return>", self.Delete)
        self.master.bind("<Button-2>", self.Delete)
        self.master.bind("<Return>", self.predict)
        self.bind("<B1-Motion>", self.draw)

        self.Load_ani = Loading_Ani(self.master, speed=50, color="white", size=40, bg="#333")
        self.Load_ani.place(relx=0.85, rely=0.9)
        self.Load_ani.hide()
        
        self.master.update()
        self.after(100, self.details_help)

    def details_help(self, evt=None):
        messagebox.showinfo("Important Information", 
        """
        This is a Meachine Learning Model 
        based on Keras algorithm.

        What does this do?
          We can Recognise Hand-Written 
          digits from this model and can 
          also Train more.

        How do I use?
          1.  Draw the digit on blank space.
          2.  Press Enter / Return key to predict.
          3.  Press Shift + Enter / Return key or 
                the Right Mouse Click to clear 
                the drawing.


            Developed By :- Saad Mairaj
                (Saadmairaj@yahoo.in)
                    (6 February 2019)
        """)

        self.master.grab_set()

    def Reser_Data(self, evt):
        self.Load_ani.show()
        Dataset.dataset_1()
        Dataset.dataset_2()
        self.after(200)
        def Load():
            self.master.bind("<Return>", lambda _: messagebox.showinfo("Message", 
                "Cannot predict while the model is traing or refreshing"))
            acc = Model.Train_Digit()
            self.Acc.config(text="Acc: {}".format(acc))
            self.update()
            tf.keras.backend.clear_session()
            load_model()
            self.Load_ani.hide()
            self.master.bind("<Return>", self.predict)

        self.Thread2 = threading.Thread(target=Load)
        self.Thread2.start()
        
    def display_win(self, evt=None):
        self.display = Canvas(self.master, bg="#333", width=300, 
          height=100, highlightthickness=0)
        self.display.pack_propagate(0)
        self.display.pack(side=BOTTOM)

        self.L1 = Label(self.display, text = "Prediction: ", 
          font=("","15", "bold"), bg="#333", fg="white")
        self.L1.pack(pady=5)

        self.Ent = Entry(self.display, bg="#333", fg="white")
        self.Ent.unbind_class("Entry", "<Key>")
        def Check_charlimit(evt):
            if evt.char in "0123456789":
                self.Ent.delete(0, END)
                self.Ent.insert(0, evt.char)
            if evt.keysym == "backspace":
                self.Ent.delete(0, END)

        self.EntHide = Label(self.display, width=22, height=22, bg="#333")
        self.EntHide.place(relx = 0.8, rely=0.1, height=20, width=20)
        self.Ent.bind("<Key>", Check_charlimit)

        self.style = ttk.Style()
        self.style.configure('TCheckbutton', font=("","10"))
        self.CkCmd = IntVar()
        self.CkCmd.set(0)
        def CkFun():
            if self.CkCmd.get():
                messagebox.showwarning("Warning", 
            """Training the model is a Beta Version.

            Usage:

            1)  Draw the digit and predict.
            2)  If the prediction is not correct, 
                    then enter the right digit in the 
                    entry box.
            3)  If the prediction is correct, 
                    then leave the entry box #333.
            """)

                self.EntHide.place_forget()
                self.Ent.place(relx = 0.8, rely=0.1, height=20, width=20)
                self.Ent.lift()
                self.display.update_idletasks()
                self.display.update()
            
            else:
                self.Ent.place_forget()
                self.display.update()
                self.display.update_idletasks()
                self.EntHide.place(relx = 0.8, rely=0.1, height=20, width=20)

        self.Ckb = ttk.Checkbutton(self.display, style="TCheckbutton", 
          text="Train The Model", variable=self.CkCmd, onvalue=1, 
          offvalue=0, command=CkFun)
        self.Ckb.pack(pady=5)

        self.Acc = Label(self, text="Acc: {}".format(97.22), 
            fg="white", bg="#333", font=("", 10))
        self.Acc.place(x=10, y=10)

        self.Restart = Label(self, text="⟲", bg="#333", fg="white", 
            font=("","16"))
        self.Restart.place(x=260, y=10)

        self.Restart.bind("<Enter>", lambda _: self.Restart.config(fg="red"))
        self.Restart.bind("<Leave>", lambda _: self.Restart.config(fg="white"))
        self.Restart.bind("<Button-1>", self.Reser_Data)

        self.HelpL = Label(self.display, text="ⓘ", fg="white", bg="#333")
        self.HelpL.place(x=10, y=10)

        self.HelpL.bind("<Enter>", lambda _: self.HelpL.config(fg="red"))
        self.HelpL.bind("<Leave>", lambda _: self.HelpL.config(fg="white"))
        self.HelpL.bind("<Button-1>", lambda _: self.HelpL.config(fg="white"))
        self.HelpL.bind("<Button-1>", self.details_help, "+")

    def draw(self, evt): 
        x1 = evt.x
        y1 = evt.y 
        x2 = evt.x + self.width
        y2 = evt.y + self.width

        self.create_oval(   x1, y1, x2, y2, 
            fill=self.color, outline=self.color )
        self.get_draw.ellipse( [x1,y1, x2,y2], fill="white" )

    def predict(self, evt):

        self.Img.save("Yo.png")
        self.Img_arr = cv2.imread("Yo.png", cv2.IMREAD_GRAYSCALE)
        self.Img_arr = cv2.resize( self.Img_arr, (28,28) )
        self.New_arr = self.Img_arr.reshape(-1, 28, 28, 1)

        with graph.as_default():
            pre = self.model.predict( [self.New_arr] )
            pre = np.argmax(pre[0])
            print("\n", pre, "\n")
        
        self.L1.config( text="Prediction: {}".format(pre) )
        self.master.update()

        if self.Ent.get():
            pre = int(self.Ent.get())
            print(pre)

        if self.CkCmd.get():
            Dataset.add(self.Img_arr, pre)
            self.train_count+=1

            if self.train_count >= 6 :
                def Train():
                    self.Restart.bind("<Button-1>", lambda _: messagebox.showinfo("Message", 
                     "Cannot perform this action while the model is already training"))
                    self.Load_ani.show()
                    acc = Model.Train_Digit()
                    self.Acc.config(text="Acc: {}".format(acc))
                    self.Load_ani.hide()
                    self.Restart.bind("<Button-1>", self.Reser_Data)
                    self.master.update()

                self.Thread = threading.Thread(target=Train)
                self.ThreadsL.append(self.Thread)

                if not self.ThreadsL[0].isAlive():
                    self.Thread.start()
                    self.train_count = 0
                    self.ThreadsL.clear()
                    self.ThreadsL.append(self.Thread)
                    self.Loading = True

                self.train_count = 0

            if self.ThreadsL and self.Loading:
                if not self.ThreadsL[0].isAlive():
                    self.master.bind("<Return>", lambda _: messagebox.showinfo("Message", 
                     "Please wait while the model is still loading"))
                    load_model()
                    self.model = model
                    self.master.bind("<Return>", self.predict)
                    self.Loading = False
                    self.master.update()
                    self.master.update_idletasks()
                
    def Delete(self, evt):
        self.delete("all")
        self.Img = Image.new( "RGB", ( 300,300 ), (0,0,0) )
        self.get_draw = ImageDraw.Draw( self.Img )


if __name__ == "__main__":

    root = Tk()
    root.resizable(0,0)
    root.title("Digit Recognition")
    root.config(bg="#333", highlightthickness=2)
    
    root.update_idletasks()
    x_cord = int( (root.winfo_screenwidth() / 2) - 150 )
    y_cord = int( (root.winfo_screenheight() / 2) - 250 )

    root.geometry("300x400+{}+{}".format(x_cord, y_cord))

    win = Draw_Pad(root, width=300, height=300)
    win.pack(side=TOP)

    root.mainloop()