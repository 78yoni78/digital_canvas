import PIL
import PIL.Image
import PIL.ImageDraw
from tkinter import *
from tkinter.colorchooser import askcolor

from model import DigitClassifier

class Paint(object):

    PEN_SIZE = 30
    DEFAULT_COLOR = 'black'
    LIGHT_COLOR = '#f0f1f5'
    HUE_COLOR = '#ba131e'
    HUE_LIGHT_COLOR = '#eb4334'
    DARK_COLOR = '#0f1012'

    def __init__(self):
        self.model = DigitClassifier()       
        self.root = Tk()
        self.root.configure(width=700, height=700, bg=self.DARK_COLOR)
        self.root.resizable(False, False)

        button_options = {
            'bg': self.HUE_COLOR,
            'fg': self.LIGHT_COLOR,
            'activebackground': self.HUE_LIGHT_COLOR,
            'borderwidth': 0,
        }

        self.pen_button = Button(self.root, text='pen', command=self.use_pen, **button_options)
        self.pen_button.grid(row=0, column=1)

        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser, **button_options)
        self.eraser_button.grid(row=0, column=2)

        self.clear_button = Button(self.root, text='clear', command=self.clear, **button_options)
        self.clear_button.grid(row=0, column=3)

        self.label = Label(self.root, text='', font=("Courier bold", 44), bg=self.DARK_COLOR, fg=self.HUE_COLOR)
        self.label.grid(row=4, column=4)

        self.c = Canvas(self.root,
                        bg=self.LIGHT_COLOR,
                        width=600, height=600,
                        borderwidth=1, relief='flat')
        self.c.place(relx=.5, rely=.5,anchor= CENTER)
        self.c.grid(row=1, columnspan=5)
        
        self.image = PIL.Image.new('L', size=(600, 600))
        self.draw: PIL.ImageDraw.ImageDraw = PIL.ImageDraw.Draw(self.image)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.draw.rectangle([0, 0, self.image.size[0], self.image.size[1]], fill='white')
        self.use_pen()

    def use_pen(self):
        self.activate_button(self.pen_button)

    def clear(self):
        self.draw.rectangle([0, 0, self.image.size[0], self.image.size[1]], fill='white')
        self.c.delete('all')

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.PEN_SIZE, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
            self.draw.line([self.old_x, self.old_y, event.x, event.y],
                           width=self.PEN_SIZE, fill=paint_color)
        self.old_x = event.x
        self.old_y = event.y
        
        self.on_update()

    def reset(self, event):
        self.old_x, self.old_y = None, None
        
    def on_update(self):
        self.label['text'] = self.model.classify(self.image)


if __name__ == '__main__':
    Paint()
