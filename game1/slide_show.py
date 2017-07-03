
wd = r"C:\Users\Rudy\Desktop\Game 1 Output\augusta_output\augusta_images/"

import Tkinter as tk
from Tkinter import * 
from PIL import Image, ImageTk
import os
from imtovid import *


class SlideShow(tk.Tk):
    def __init__(self, frame, image_files):
        tk.Tk.__init__(self)
        # self.geometry('+{}+{}'.format(x,y))
        self.frame = frame
        
        self.pictures = [image for image in image_files]
        self.picture_display = tk.Label(self)
        self.picture_display.pack()
        self.images = [] # to keep references to images.
        
        b1 = Button(self.frame, text="Back", command=self.back_pic).pack()
        b2 = Button(self.frame, text="Next", command=self.next_pic).pack()
        
        self.img_counter = 0 
    
    def prev_pic(self):
        self.img_counter -= 1
        self.show_slide()
    
    def next_pic(self):
        self.img_counter += 1
        self.show_slide()
    
    def show_first_slide(self):        
        img_name = self.pictures[0]#next(self.pictures)
        image_pil = Image.open(img_name).resize((800, 550)) #<-- resize images here

        self.images.append(ImageTk.PhotoImage(image_pil))      

        self.picture_display.config(image=self.images[-1])
        self.title(img_name)

    def show_slide(self):        
        current_img = self.pictures[self.img_counter % len(self.pictures)]
        
        image_pil = Image.open(current_img).resize((800, 550)) #<-- resize images here

        self.images.append(ImageTk.PhotoImage(image_pil))      

        self.picture_display.config(image=self.images[-1])
