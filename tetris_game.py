import tkinter as tk
import time
from random import randrange
from Board import Board
from tetris_peace import Peace
from tetris_shapes import Shapes
class Game(tk.Frame):
    def __init__(self,master=None,shapes_list=None):
        """ shapes list like
        list of shapes
        shape is list of rotations
        rotation is list of lists of x and y
        item =[  [shape rotation 0],[shapre rotation 1]]
        and the shape rotation is [[x,y],...]
        for x y is not numbers but rows 
        according to the base location * len of len_of_cell"""
        super().__init__(master)
        self.master=master
        self.shapes_list=shapes_list
        self.rows=40#every row is  like 4*4 list
        self.columns=40
        self.len_of_cell=self.columns//4
        self.base_location=[(self.columns*self.len_of_cell)//2,0]
        self.curr_state=tk.StringVar()
        self.curr_state.set("start game")
        self.info=tk.StringVar()
        self.info.set(""" 
            up for rotate 
 right for right                          left for left

                down for drop """)
        self.pack()
        self.board_color="white"
        self.peace_color="orange"
        self.peace=None#the beace
        self.play_area=None
        self.start_play=False
        self.pause=False
        self.drop_peace=False
        self.score=0
        self.delay=900
        self.cancel_drop=None#to avoid the fallen peace following another peace reach the end
        self.create_widgets()
    def create_widgets(self):
        self.control_area=tk.PanedWindow()
        self.control_area.pack(side=tk.RIGHT,expand=True)
        self.game_state=tk.Label(master=self.control_area,textvariable=self.curr_state)
        self.game_state.pack(fill=tk.X)
        self.game_info=tk.Label(master=self.control_area,textvariable=self.info)
        self.game_info.pack(fill=tk.X)
        self.start=tk.Button(self.control_area,text="start",command=self.play)
        self.start.pack(fill=tk.X)
        self.stop=tk.Button(self.control_area,text="stop play",command=self.stop)
        self.stop.pack(fill=tk.X)
        self.reset=tk.Button(self.control_area,text="reset",command=self.reset)
        self.reset.pack(fill=tk.X)
        self.board=Board(self)
        self.master.bind("<Right>",self.move_peace_right)
        self.master.bind("<Left>",self.move_peace_left)
        self.master.bind("<Up>",self.rotate_peace)
        self.master.bind("<Down>",self.hard_down)
    def move_peace_down(self):
        return self.peace.move_peace(0,1,0)
    def rotate_peace(self,event):
        if not self.peace or (not self.start_play) or self.pause:
            return
        self.peace.move_peace(0,0,1)
    def move_peace_right(self,event):
        if not self.peace or (not self.start_play) or self.pause:
            return
        self.peace.move_peace(1,0,0)
    def move_peace_left(self,event):
        if not self.peace or(not self.start_play) or self.pause:
            return
        self.peace.move_peace(-1,0,0)
    def delete_peace(self):
        self.peace.delete()
    def play(self):
        self.start_play=True
        self.curr_state.set(f"score: {self.score} level : {self.score//100}")
        self.run_game()
    def stop(self):
        if not self.start_play:
            return
        self.pause=not self.pause
    def reset(self):
        self.start_play=False
        self.pause=False
        self.drop_peace=False
        self.delete_peace()
        self.peace=None
        self.delay=900
        self.score=0
        self.cancel_drop=None
        self.board.reset_the_board()
        self.curr_state.set("start game")

    def run_game(self):
        if not self.start_play :
            return
        if self.pause or  self.drop_peace:
            pass
        elif self.peace==None:
            self.peace=self.get_peace()
            first_move=self.peace.move_peace(0,0,0)
            if not first_move:
                self.start_play=False
                self.curr_state.set("end of game")
                self.delete_peace()
                self.peace=None

                return 
        elif not self.move_peace_down():
            
            self.board.fill_cells(self.peace.coords)
            self.board.remove_full_rows()
            self.score+=10
            self.curr_state.set(f"score: {self.score} level : {self.score//100}")
            self.delete_peace()
            self.peace=None
            if self.cancel_drop:
                self.master.after_cancel(self.cancel_drop)
                self.cancel_drop=None
            self.delay=max(self.delay-(2*(self.score//100)),300)
        else:
            self.move_peace_down()
            
        self.master.after(self.delay,self.run_game)

    def get_peace(self):
        shape=self.shapes_list[randrange(len(self.shapes_list))]
        return Peace(self.board,shape)
    def hard_down(self,event):
        """tp move peace to the bottom"""
        if (not self.peace )or (not self.start_play) or self.pause :
            return
        self.drop_peace=True
        
        if not self.peace.move_peace(0,1,0):
            self.board.fill_cells(self.peace.coords)
            self.board.remove_full_rows()
            self.score+=10
            self.curr_state.set(f"score: {self.score} level : {self.score//100}")
            self.delete_peace()
            self.peace=None
            self.drop_peace=False
            return
        else:
            self.peace.move_peace(0,1,0)#don't use movee_peace_down problems with None
            self.cancel_drop=self.master.after(250,lambda:self.hard_down(event=None))

if __name__=="__main__":
    root=tk.Tk()
    app=Game(root,Shapes)
    app.mainloop()
        
