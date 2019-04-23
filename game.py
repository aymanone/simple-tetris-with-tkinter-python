import tkinter as tk
from tetris_game import Game
from tetris_shapes import Shapes
root=tk.Tk()
game=Game(root,Shapes)
game.mainloop()
