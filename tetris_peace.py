import tkinter as tk
from rot_for_tetris import r,l
class Peace:
    def __init__(self,board,shapes=None):
        self.board=board
        self.shapes=shapes
        self.play_area=board.play_area
        self.color=board.peace_color
        self.base_location=board.base_location+[]#to avoid aliasing
        self.peace_len=board.len_of_cell
        self.current_shape=0
        self.board_width=int(self.play_area["width"])
        self.board_height=int(self.play_area["height"])
        self.coords=self.get_coords(self.shapes[self.current_shape%len(self.shapes)],self.base_location)   
    def move_peace(self,x,y,rotate):
        x_move=x*self.peace_len
        y_move=y*self.peace_len
        r_move=(self.current_shape+rotate)%len(self.shapes)
        rotate_move=self.current_shape+rotate
        coords=self.get_coords(self.shapes[r_move],[self.base_location[0]+x_move,self.base_location[1]+y_move])
        if  not self.valid_move(coords):return False

        self.play_area.delete("peace_cell")
        self.base_location[0]+=x_move
        self.base_location[1]+=y_move
        self.current_shape+=rotate
        self.coords=coords
        self.draw_shape()
        return True
    def get_coords(self,shape,location):
        """ shape is array detect the x and y for every square
        in the peace relative to bse location"""
        return [ [location[0]+(x*self.peace_len),location[1]+(y*self.peace_len)] for (x,y) in shape]
    def valid_move(self,coords):
        if  self.in_the_board(coords) :
            return self.empty_cells(coords)
        return False
    def empty_cells(self,coords):
        for (x,y) in coords:
            if self.board.cells[y//self.peace_len][x//self.peace_len]==self.color:
                return False
        return True
    def in_the_board(self,coords):
        for (x,y) in coords:
            if x<0 or y <0 :return False
            if x>self.board_width-self.peace_len or y >self.board_height-self.peace_len:return False
        return True

    def draw_shape(self):
        for (x,y) in self.coords:
            self.play_area.create_rectangle(x,y,x+self.peace_len,y+self.peace_len,fill=self.color,tags=f"peace_cell")
    def delete(self):
        self.play_area.delete("peace_cell")
        del self
    
