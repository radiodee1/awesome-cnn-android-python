import kivy
#kivy.require('1.9.1') # replace with your current kivy version !



import math

##import cnn_both as nn


import enum_local as LOAD

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import *
from kivy.graphics.texture import Texture



class IMEApp(App):

    def __init__(self):
        App.__init__(self)

        self.cols = 28
        self.rows = 28

        self.pos_top = int(Window.height * 0.35)
        self.but_height = float(Window.height / float(6))/float(Window.height)
        self.but_width = float( ((Window.width - ( Window.height / 2))/2)/float(Window.width))
        self.pos_right_but = int(Window.width - (Window.width* self.but_width ) - 10)

        self.outtext = "0"
        self.outheight = 40
        self.bottom = Label(text = self.outtext, size_hint_y = None, height = self.outheight)

        self.list_txt = str("")
        self.label_top = Label(text=self.list_txt, halign="left", valign="top", pos=(10 , 10))

        self.mag = 1    # 5
        self.stride = 32 #256
        #self.project = 20

        self.grid = [ -1 for i in range (self.stride * self.stride) ]
        self.input_grid = [ 0 for i in range (self.cols * self.rows) ]

        self.still_looping = True
        self.load_type = LOAD.ALPHA
        self.load_letter = "A"
        self.touched_screen = False
        self.pos = (0,0)

        self.process = False
        
        ##self.cnn =  nn.DualCNN()
        ##self.cnn.load_file()
        
        self.letter = ""


    def build(self):

        #self.label = [ None for i in range (self.cols * self.rows)]
        self.bottom.text_size = (500,50)
        self.bottom.font_size = (50)
        self.bottom.valign = "bottom"
        self.outerlayout = RelativeLayout(pos = (0, self.pos_top), size=(Window.width, self.pos_top))
        self.largelayout = FloatLayout(cols=3, pos = (0, 0),
                                      #row_force_default=True,
                                      #row_default_height = 40,
                                      size=(Window.width, self.pos_top),
                                      padding=[0,Window.height - self.pos_top,0,0])

        pos1 = 10
        pos2 = self.but_height * Window.height * 1
        pos3 = self.but_height * Window.height * 2

        self.project = Window.height // (self.rows * 2)
        self.screenpos = ((Window.width - (self.cols * self.project)) // 2 , 10)

        self.bottom = Label(text = "[]", size_hint_y = self.but_width, height = self.outheight )

        self.button_enter = Button(text="enter", size_hint=( self.but_width, self.but_height),width= self.but_width, pos=(10,pos1))
        self.button_enter.bind(on_press=self.button_enter_callback)

        self.button_clear = Button(text="clear", size_hint=(self.but_width , self.but_height),width = self.but_width, pos=(10,pos2))
        self.button_clear.bind(on_press=self.button_clear_callback)

        self.button_input_type = Button(text=self.load_letter, size_hint=( self.but_width , self.but_height), pos=(self.pos_right_but,pos3))
        self.button_input_type.bind(on_press=self.button_input_type_callback)

        self.button_next_pos = Button(text=">>>>", size_hint=(self.but_width , self.but_height), pos=(self.pos_right_but,pos2))
        self.button_last_pos = Button(text="<<<<", size_hint=(self.but_width , self.but_height), pos=(self.pos_right_but,pos1))

        self.button_blank = Button( size_hint=(self.but_width , self.but_height), pos=(10,pos3))

        self.largelayout.add_widget(self.button_enter)

        self.largelayout.add_widget(self.button_clear)
        self.largelayout.add_widget(self.button_input_type)

        self.largelayout.add_widget(self.button_last_pos)
        self.largelayout.add_widget(self.button_next_pos)

        self.largelayout.add_widget(self.bottom)
        self.largelayout.add_widget(self.label_top)

        self.largelayout.add_widget(self.button_blank)

        self.texture = Texture.create( size = (self.stride, self.stride))
        self.texture.mag_filter = "nearest"

        with self.largelayout.canvas :
            Color(1.0, 1.0, 1.0)
            Rectangle(texture=self.texture, pos=self.screenpos, size=(self.cols * self.project, self.cols *self.project))

        Window.bind(on_motion=self.on_motion)

        ##Clock.schedule_interval(self.check_clock, 1.0 / 30.0)

        self.update_texture()
        return self.largelayout

    '''
    def check_clock(self, x):
        try:
            if (android.check_pause()) :
                self.process = False
                Clock.unschedule(self.check_clock)
                android.wait_for_resume()
                Clock.schedule_interval(self.check_clock, 1.0 / 30.0)

        except:
            pass
        return
    '''

    def on_motion(self, window, etype, motionevent):
        
        if motionevent.pos[0] + motionevent.pos[1] != 0 :
            self.pos = motionevent.pos
            x = math.ceil((self.pos[0] - (self.screenpos[0] - self.project ))/   self.project)
            y = math.ceil((self.pos[1] - (self.screenpos[1] - self.project ))/   self.project)

            if x < self.cols and y < self.rows and x >= 0 and y >= 0 :
                self.grid[ int(y * self.stride + x) ] = 1
                self.touched_screen = True

        self.update_texture()
        ##self.run_cnn()
        self.bottom.text = str(str(self.pos[0]) + " - " + str(self.pos[1]) +
                               "  " + str(self.load_letter) + " [" + str(self.letter) + "]")
        self.label_top.text = self.list_txt


    def button_enter_callback(self, value):
        self.process = True

    def button_clear_callback(self , value):
        self.process = False
        self.touched_screen = False
        self.clear_array_pos()

    def button_input_type_callback(self, value):
        self.shift_load_type()

        self.button_input_type.text = str(self.load_letter)

    def update_texture(self):

        buf = []

        for i in range (self.cols * self.rows) :
            y =   ( i // (self.cols ))
            x = i - (y * self.cols)
            c = 0

            if self.grid[  y * self.stride + x ] > 0 : c = 1

            self.input_grid[(self.rows - y -1 ) * self.cols + x] = c


        for i in range(self.stride * self.stride) :
            if self.grid[i] > 0 :
                buf.extend([255, 255, 255, 255])
            elif self.grid[i] < 0 :
                buf.extend([120, 120, 120, 120])
            else:
                buf.extend([200, 200, 200, 200])

        buf = b''.join(map(chr,buf))
        self.texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')



    def run_cnn(self):
        '''
        if self.process == True and self.touched_screen == True:
            self.normalize()
            self.cnn.set_input_type(self.load_type)
            self.cnn.set_x_in(self.input_grid)

            self.cnn.game_loop()
            self.letter = self.cnn.get_prediction()
            #print(self.letter)

            self.list_txt = self.list_txt + " " + str(self.letter)
            self.clear_array_pos()
            self.process = False
            self.update_texture()
            return
        '''
        pass

    def normalize(self):
        grid2 = [0 for j in range(28*28)]
        for i in range(len(self.input_grid)):
            if self.input_grid[i] == 1 and i - 1 >= 0 :
                grid2[i-1] = 1
            if self.input_grid[i] == 1 and i + 28 < 28*28 :
                grid2[i+28] = 1
        for i in range(len(self.input_grid)) :
            if grid2[i] == 1 : self.input_grid[i] = 1.0

        #self.mag_vert() ## THIS METHOD DOES NOT WORK WELL ENOUGH TO USE!!
        return

    def mag_vert(self):
        points = []
        first_y_found = False
        first_y = (0,0)
        #last_found = False
        last_y = (0,0)
        for i in range(len(self.input_grid)) :
            y = i // self.cols
            x = i - ((i // self.cols) * self.cols)
            if self.input_grid[i] == 1:
                points.append(( x, y))
                if not first_y_found:
                    first_y = (x,y)
                    first_y_found = True
                elif first_y_found:
                    last_y = (x,y)

        first_x = (0,0)
        first_x_found = False
        last_x = (0,0)
        for i in range(self.cols):
            for j in range(self.cols) :
                newx = i
                newy = j * self.cols
                if self.input_grid[newx + newy] == 1 :
                    if not  first_x_found:
                        first_x = (i,j)
                        first_x_found = True
                    elif first_x_found:
                        last_x = (i,j)

        mag_x = (self.cols ) / float(last_x[0] - first_x[0] + 0.1)
        mag  =  (self.cols ) / float(last_y[1] - first_y[1] + 0.1)
        if mag_x < mag :
            mag = mag_x
            #print("special mag")

        width = min(self.cols , last_x[0] - first_x[0])

        x_space = - int ( ((self.cols -  (( width ) )   ) / 2) ) + int(first_x[0] * math.ceil(mag) )

        x_space = int (first_x[0] * mag)

        newpts = []

        for i in range(len(points)):
            newpts.append( (points[i][0] * mag, points[i][1] * mag)   )

        self.input_grid = [float(0) for i in range(self.cols* self.cols)]
        for i in range(len(newpts)):
            x = int(newpts[i][0])
            y = int(newpts[i][1])
            for j in range(int(math.ceil(mag))):
                for k in range(int(math.ceil(mag))):
                    newx = x + j - x_space
                    newy = int(y + k ) - int (first_y[1] /   mag)
                    if (newx<  self.cols) and (newx >= 0) and (newy < self.cols) and (newy >= 0) :
                        self.input_grid [newx + (newy * self.cols)] = 1.0
        #print(self.input_grid)

    def clear_array_pos(self) :
        self.grid = [int(-1) for i in range (self.stride*self.stride)]
        self.input_grid = [float(0) for i in range (28*28)]
        self.touched_screen = False

    def shift_load_type(self):
        '''
        if self.load_type == LOAD.ALPHA:
            self.load_type = LOAD.NUMERIC
            self.load_letter = "#"
            self.cnn.set_input_type(self.load_type)
            return
        if self.load_type == LOAD.NUMERIC:
            self.load_type = LOAD.ALPHA
            self.load_letter = "A"
            self.cnn.set_input_type(self.load_type)
            return

        if self.load_type != LOAD.ALPHA and self.load_type != LOAD.NUMERIC :
            self.load_type = LOAD.ALPHA
            self.load_letter = "A"
            self.cnn.set_input_type(self.load_type)
            return
        '''
        pass

if __name__ == '__main__':
    IMEApp().run()
    


