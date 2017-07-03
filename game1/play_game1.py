from Tkinter import *
import tkFileDialog as fd
import ttk
import os
import time
from sys import platform
import subprocess as sub
from game1 import *
from slide_show import *
from PIL import Image, ImageTk

SCALE_X = 0.3
SCALE_Y = 0.7

try: 
    import ctypes
    
    user32 = ctypes.windll.user32

    WIDTH, HEIGHT = int(SCALE_X*user32.GetSystemMetrics(0)), int(SCALE_Y*user32.GetSystemMetrics(1))
except:
    WIDTH, HEIGHT = (300, 650)
    
PADX = 5
PADY = 5

BLACK = '#000000'
INK = '#062F4F'
POSY = '#813772'
EMBERS = '#B82601'

STORMY = '#494E6B'
CLOUD = '#98878F'
SUNSET = '#CB5E6D'
EVENING = '#192231'
WHITE = '#FFFFFF'
GRAY = '#BBBBBB'

NOIMG = 'noimg.png'


XSMALL_FONT = ('Segoe UI Regular', 8)
SMALL_FONT = ('Segoe UI Regular', 10)
LABEL_FONT = ('Segoe UI Semibold', 14)
MEDIUM_FONT = ('Segoe UI Regular', 22)
LARGE_FONT = ('Segoe UI Regular', 30)


class Game1_GUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
        self.x = (self.screen_width / 2) - (WIDTH / 2)
        self.y = (self.screen_height / 2) - (HEIGHT / 2)
        
        height = HEIGHT
        
        self.title("Play Game 1")
        self.geometry('{0}x{1}+{2}+{3}'.format(WIDTH, height, self.x, 0))
        self.configure(background=STORMY)
        self.resizable(width=False, height=False)
         
        ttk.Style().configure("TButton", padding=4, font=SMALL_FONT, background=STORMY, foreground=STORMY)
        ttk.Style().configure("TCheckbutton", padding=4, font=SMALL_FONT, background=STORMY, foreground=WHITE)
        ttk.Style().configure("HomeCheck.TCheckbutton", padding=4, font=LABEL_FONT, background=STORMY, foreground=WHITE)        
        ttk.Style().configure("TSeparator", padding=4, background=STORMY)
        ttk.Style().configure("TScale", padding=4, background=STORMY)
        
                
        menubar = Menu(self)
        
        menubar.add_command(label="Show All Windows", command=self.show_all)
        menubar.add_command(label="Close All Windows", command=self.close_all)
        
        # display the menu
        self.config(menu=menubar)
        
        self.home_frame = Frame(self, background=STORMY)
        self.animate = False
                
        choose_networks_home = Label(self.home_frame, text="Choose Networks Directory", font=LABEL_FONT, fg=WHITE, bg=STORMY)
        choose_networks_home.grid(row=0, column=0, padx=PADX, pady=PADY)
        
        self.choose_networks_home_btn = ttk.Button(self.home_frame, text="Browse", command=self.choose_networks_directory)
        self.choose_networks_home_btn.grid(row=1, column=0, padx=PADX, pady=PADY)
        
        self.chosen_networks_home_label = Label(self.home_frame, text="<No Directory Selected>", font=SMALL_FONT, fg=SUNSET, bg=STORMY)
        self.chosen_networks_home_label.grid(row=2, column=0, padx=PADX, pady=PADY)
        
        choose_player_method_label = Label(self.home_frame, text="Choose Networks and Main Nodes from File", font=LABEL_FONT, fg=WHITE, bg=STORMY)
        choose_player_method_label.grid(row=3, column=0, padx=PADX, pady=PADY)
        
        self.choose_networks_node_btn = ttk.Button(self.home_frame, text="Browse", command=self.choose_config_file)
        self.choose_networks_node_btn.grid(row=4, column=0, padx=PADX, pady=PADY)
        
        self.chosen_networks_node_label = Label(self.home_frame, text="<No File Selected>", font=SMALL_FONT, fg=SUNSET, bg=STORMY)
        self.chosen_networks_node_label.grid(row=5, column=0, padx=PADX, pady=PADY)
        
        output_home_label = Label(self.home_frame, text="Output Directory", font=LABEL_FONT, fg=WHITE, bg=STORMY)
        output_home_label.grid(row=6, column=0, padx=PADX, pady=PADY)
        
        self.choose_output_dir_btn = ttk.Button(self.home_frame, text="Browse", command=self.choose_output_directory)
        self.choose_output_dir_btn.grid(row=7, column=0, padx=PADX, pady=PADY)
        
        self.chosen_output_dir_label = Label(self.home_frame, text="<No Directory Selected>", font=SMALL_FONT, fg=SUNSET, bg=STORMY)
        self.chosen_output_dir_label.grid(row=8, column=0, padx=PADX, pady=PADY)
        
        self.animate_checkbox = ttk.Checkbutton(self.home_frame, text="Create Animation", style="HomeCheck.TCheckbutton", command=self.movie_duration_handler)
        self.animate_checkbox.grid(row=9, column=0, padx=PADX, pady=PADY)
        
        self.movie_duration = IntVar(value=30)
        
        self.animation_duration_label = Label(self.home_frame, text="Animation Duration (sec)", font=LABEL_FONT, fg=GRAY, bg=STORMY)
        self.animation_duration_label.grid(row=10, column=0, padx=PADX, pady=PADY)
        
        self.movie_duration_slider = ttk.Scale(self.home_frame, from_=20, to=60, value=self.movie_duration.get(), variable=self.movie_duration,
                                               command=lambda x: self.movie_duration.set('%d' % float(x)), orient=HORIZONTAL, length=200)
        self.movie_duration_slider.grid(row=11, column=0, padx=PADX, pady=PADY)
        
        self.movie_duration_slider.state(["disabled"])
        
        Label(self.home_frame, textvariable=self.movie_duration, font=XSMALL_FONT, bg=STORMY, fg=WHITE).grid(row=12, column=0, padx=PADX, pady=PADY)
        
        ttk.Separator(self.home_frame).grid(row=13, column=0, padx=PADX, pady=PADY, sticky="EW")
        
        self.run_btn = ttk.Button(self.home_frame, text="Run", command=self.run_game1)
        self.run_btn.grid(row=14, column=0, padx=PADX, pady=PADY)
        
        self.progress = ttk.Progressbar(self.home_frame, length=200)
        self.progress.grid(row=15, column=0, padx=PADX*10, pady=PADY*3)
        
        self.home_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        with open('show_help_onstartup.txt', 'r') as f:
            self.show_on_startup_state = BooleanVar(value=int(f.read()))
        
        instructions_show_status = self.show_on_startup_state.get()
        
        self.movie_visualizer()
        
        if instructions_show_status == True: 
            self.help()
        else:
            pass
    
    def choose_networks_directory(self):        
        try:
            if not os.path.exists('recent_networks_directory.txt'):
                with open('recent_networks_directory.txt', 'w') as hf:                
                    hf.write('.')
                
                with open('recent_networks_directory.txt', 'r') as hf:                
                    dir_history = hf.read()
                    
            with open('recent_networks_directory.txt', 'r') as hf:                
                dir_history = hf.read()
            
            self.networks_directory = fd.askdirectory(initialdir=dir_history.strip(), title="Choose Networks Directory")
            
            if len(self.networks_directory) > 0:                
                self.chosen_networks_home_label.configure(text=self.networks_directory.split("/")[-1], fg=CLOUD)
                
                with open('recent_networks_directory.txt', 'w') as hf:
                    hf.write(self.networks_directory)
                
            else:
                print "\n\nNo Folder Selected\n\n"
                self.chosen_networks_home_label.configure(text="<No Directory Selected>", fg=SUNSET)
                
        except Exception, e:
            print e
            
    def choose_config_file(self):        
        try:
            
            self.config_file = fd.askopenfilename(title="Choose Config File")
            
            if len(self.config_file) > 0:                
                self.chosen_networks_node_label.configure(text=self.config_file.split("/")[-1], fg=CLOUD)
                
            else:
                print "\n\nNo File Selected\n\n"
                self.chosen_networks_node_label.configure(text="<No Directory Selected>", fg=SUNSET)
                
        except Exception, e:
            print e
    
    def choose_output_directory(self):
        try:
            if not os.path.exists('recent_output_directory.txt'):
                with open('recent_output_directory.txt', 'w') as hf:                
                    hf.write('.')
                
                with open('recent_output_directory.txt', 'r') as hf:                
                    dir_history = hf.read()
                    
            with open('recent_output_directory.txt', 'r') as hf:                
                dir_history = hf.read()
            
            self.output_directory = fd.askdirectory(initialdir=dir_history.strip(), title="Choose Output Directory")
            
            if len(self.output_directory) > 0:                
                self.chosen_output_dir_label.configure(text=self.output_directory.split("/")[-1], fg=CLOUD)
                
                with open('recent_output_directory.txt', 'w') as hf:
                    hf.write(self.output_directory)
                
            else:
                print "\n\nNo Folder Selected\n\n"
                self.chosen_output_dir_label.configure(text="<No Directory Selected>", fg=SUNSET)
                
        except Exception, e:
            print e
    
    def movie_duration_handler(self):
        if len(self.movie_duration_slider.state()) > 0: 
            self.movie_duration_slider.state(["!disabled"])
            self.animation_duration_label.configure(fg=WHITE)
            self.animate = True
        else:
            self.movie_duration_slider.state(["disabled"])
            self.animation_duration_label.configure(fg=GRAY)
            self.animate = False
            
        print self.animate, self.movie_duration.get()
        
    def run_game1(self):
        self.env = Environment(self.networks_directory, self.config_file, self.output_directory, self.animate)
        # wd = r'C:\Users\Rudy\Downloads\game1'
        # env = Environment(wd, r'C:\Users\Rudy\Desktop\config.csv', r'C:\Users\Rudy\Desktop', animate=True)
        # 
        self.env.run()
        self.update_option_menu()
        # self.show_slide()
        
    def movie_visualizer(self):
        ttk.Style().configure("TMenubutton", padding=4, width=25)
        
        self.movie_window = Toplevel()
        self.movie_window.title("Movie Player")
        
        self.image_options = ["<None>"]
        
        height = HEIGHT/2
        
        self.movie_window.geometry("{0}x{1}+{2}+{3}".format(WIDTH, height - 30, self.x, self.y + height + 26))
        self.movie_window.configure(background=SUNSET)
        self.movie_window.resizable(width=False, height=False)
        
        self.movie_frame = Frame(self.movie_window, bg=SUNSET)
        
        
        
        var = StringVar()
        
        
        var.set(self.image_options[0])
        
        
        self.image_paths = ttk.OptionMenu(self.movie_frame, var, self.image_options[0], *self.image_options)
        self.image_paths.grid(row=1, column=0, columnspan=2, padx=PADX, pady=PADY)
        
        self.picture_display = tk.Label(self.movie_frame)
        self.picture_display.grid(row=2, column=0, columnspan=2, padx=PADX, pady=PADY)
        
        self.prev_btn = ttk.Button(self.movie_frame, text="Previous")
        self.prev_btn.grid(row=3, column=0, padx=PADX, pady=PADY)
        
        self.next_btn = ttk.Button(self.movie_frame, text="Next")
        self.next_btn.grid(row=3, column=1, padx=PADX, pady=PADY)
        
        self.movie_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.show_no_slide()
    
    def update_option_menu(self):
        option_menu = self.image_paths['menu']
        
        for img_path in self.env.images_paths:
            short_path = img_path.replace('\\', '/').split('/')[-1]
            
            option_menu.add_command(label=img_path)
    
    def prev_pic(self):
        self.img_counter -= 1
        self.show_slide()
    
    def next_pic(self):
        self.img_counter += 1
        self.show_slide()
    
    def show_no_slide(self):
        img_name = NOIMG
        image_pil = Image.open(img_name).resize((400, 200)) #<-- resize images here
        
        img_to_show = ImageTk.PhotoImage(image_pil)
        
        self.picture_display.config(image=img_to_show)
        self.picture_display.image = img_to_show
        
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
        
    # def show_slide(self):
    #     wd = r'C:\Users\Rudy\Desktop\Game 1 Output\augusta_output\augusta_images'
    #     
    #     images = [wd + '/' + img for img in os.listdir(wd)]
    #     
    #     slideshow = SlideShow(self.movie_window, images)
    #     slideshow.show_first_slide()
        
    def help(self):
        self.help_window= Toplevel()
        self.help_window.title("Help")
        
        width = WIDTH/2
        
        self.help_window.geometry("{0}x{1}+{2}+{3}".format(width, HEIGHT - 4, self.x - width, self.y))
        self.help_window.configure(background=EVENING)
        self.help_window.resizable(width=False, height=False)
        
        self.help_frame = Frame(self.help_window, background=STORMY)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        if not os.path.exists('show_help_onstartup.txt'):
            with open('show_help_onstartup.txt', 'w') as f:
                f.write("1")
                
            with open('show_help_onstartup.txt', 'r') as f:
                self.show_on_startup_state = BooleanVar(value=int(f.read()))
                
        else:
            with open('show_help_onstartup.txt', 'r') as f:
                self.show_on_startup_state = BooleanVar(value=int(f.read()))
                
        self.show_on_startup_checkbox = ttk.Checkbutton(self.help_frame, text="Show on Startup", variable=self.show_on_startup_state, command=self.show_on_startup)
        self.show_on_startup_checkbox.grid(row=10, column=0, padx=PADX, pady=PADY, sticky="EW")
        
        if self.show_on_startup_state > 0:
            self.show_on_startup_checkbox.invoke()
        else:
            pass
        
        self.help_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    def show_all(self):
        try:
            if self.help_window.winfo_exists() == 1:
                print "Help already open!"
            else:
                print "Opening Help."
                self.help()
        except:
            self.help()
            
        try:
            if self.movie_window.winfo_exists() == 1:
                print "Movie already open!"
            else:
                print "Opening Movie."
                self.movie_visualizer()
        except:
            self.movie_visualizer()
            
    def close_all(self):
        try:
            if self.help_window.winfo_exists() == 1:
                print "Closing Help."
                self.help_window.destroy()
            else:
                print "Help already closed!"
                
        except:
            print "Help already closed!"
            
        try:
            if self.movie_window.winfo_exists() == 1:
                print "Closing Movie."
                self.movie_window.destroy()
            else:
                print "Movie already closed!"                
        except:
            print "Movie already closed!"
                
    def show_on_startup(self):
        status = self.show_on_startup_state.get()
        
        if status == False: 
            with open('show_help_onstartup.txt', 'w') as f:
                f.write("0")
                
        else:
            with open('show_help_onstartup.txt', 'w') as f:
                f.write("1")
            
        
        
        
        
        
app = Game1_GUI()
app.mainloop()