from tkinter import *
import timeit
from pygame import mixer

mixer.init()

def playsound():
    mixer.music.load("NaM.wav")
    mixer.music.play(2)

def HhMmSs_format(seconds):
    remaining = seconds

    hours = remaining//(60**2)
    remaining = remaining%(60**2)

    minutes = remaining//60
    remaining = remaining%60

    seconds = remaining

    return "%02i:%02i:%05.2f" % (hours,minutes,seconds)

class Timer:

    def __init__(self, master):
        self.master = master
        self.current_seconds = 0.00
        self.after_id = None # id to be used to cancel decrementing when needed
        self.timer_flag = False # indicates if the timer is running or not
        self.t_button = Button(self.master, text="Start/Stop", command=self.timer_button_func, width=10, padx=10, pady=4) # Button to start/stop the timer
        self.del_time_button = Button(self.master, text="Delete", command=self.delete_time_func, width=10, padx=10, pady=4) # Button to reset the timer to 0s
        self.timer_b_button = Button(self.master, text="Back", command=self.timer_back_func, width=10, padx=10, pady=4) # Button to go back from the timer to the choice menu
        self.timer_label = Label(text=HhMmSs_format(self.current_seconds), font=("Courier",24), width=10, padx=10, pady=4) # Timer numbers showing remaining time
        self.timer_title_label = Label(text="TIMER", font=("Courier New", 28), width=10, padx=10, pady=4)

        self.hour_entry = Entry(self.master, width=10)
        self.hour_label = Label(self.master,text="h")
        self.minute_entry = Entry(self.master, width=10)
        self.minute_label = Label(self.master,text="m")
        self.second_entry = Entry(self.master, width=10)
        self.second_label = Label(self.master,text="s")
        self.time_setter_button = Button(self.master, text="Set time", command=self.set_time_func, width=10, padx=10, pady=4)

    # Get current seconds in timer
    def current_time(self):
        return self.current_seconds
    
    # Stops the timer from running
    def pause_timer(self, id):
        self.master.after_cancel(id)
    
    # Gets the timer to run down, stops at 0
    def decrement_seconds(self):
        self.timer_label.configure(text=HhMmSs_format(self.current_seconds))
        if self.current_seconds > 0.00:
            self.current_seconds -= 0.01 
            self.after_id = self.master.after(10, self.decrement_seconds) # small delay for accurate timing
            self.timer_label.configure(text=HhMmSs_format(self.current_seconds))

        elif self.current_seconds <= 0:
            self.current_seconds = 0.0
            self.timer_label.configure(text=HhMmSs_format(self.current_seconds))
        
        # if time has run out
        if HhMmSs_format(self.current_seconds) == "00:00:00.00":
            self.current_seconds = 0.0
            self.timer_label.configure(text=HhMmSs_format(self.current_seconds))
            playsound()

    # Adds entry boxes for users to put amount of hours,minutes, and seconds into the timer
    def timer_entries(self):

        self.second_label.pack(side=RIGHT, padx=2)
        self.second_entry.pack(side=RIGHT, padx=2)
        
        self.minute_label.pack(side=RIGHT, padx=2)
        self.minute_entry.pack(side=RIGHT, padx=2)
        
        self.hour_label.pack(side=RIGHT, padx=2)
        self.hour_entry.pack(side=RIGHT, padx=2)

    # The get_seconds, get_minutes, get_hours functions get their respective values, also checks if they are valid inputs
    def get_seconds(self):
        try:
            value = int(self.second_entry.get())
            if value >= 0:
                return value
        except ValueError:
            self.second_entry.config(bg="indian red")

    def get_minutes(self):
        try:
            value = int(self.minute_entry.get())
            if value >= 0:
                return value
        except ValueError:
            self.minute_entry.config(bg="indian red")
    
    def get_hours(self):
        try:
            value = int(self.hour_entry.get())
            if value >= 0:
                return value
        except ValueError:
            self.hour_entry.config(bg="indian red")

    # Set the time from the values in the entry boxes to the timer
    def set_time_func(self):
        self.timer_flag = False
        if self.after_id != None:
            self.master.after_cancel(self.after_id)

        if not self.second_entry.get(): # check if empty
            seconds = 0
        else:
            seconds = self.get_seconds()
        
        if not self.minute_entry.get():
            minutes = 0
        else:
            minutes = self.get_minutes()
        
        if not self.hour_entry.get():
            hours = 0
        else:
            hours = self.get_hours()
        
        # Try converting to int, otherwise considered invalid input
        try:
            self.current_seconds = int(seconds + (minutes*60) + (hours*(60**2)))
            self.timer_label.config(text=HhMmSs_format(self.current_seconds))
            self.second_entry.config(bg="white")
            self.minute_entry.config(bg="white")
            self.hour_entry.config(bg="white")
            return self.time_to_add
        except:
            pass
    
    # Function to pack the button for setting time
    def set_time_button(self):
        self.time_setter_button.pack(side=BOTTOM)

    # This function decrements the timer when proper conditions are met
    def timer_button_func(self):
        if not self.timer_flag: # off to on
            self.timer_flag = True
            if self.current_seconds > 0: # must be time remaining
                self.master.after(0, self.decrement_seconds)
                self.timer_label.configure(text=HhMmSs_format(self.current_seconds))
        else: # on to off
            self.timer_flag = False
            self.pause_timer(self.after_id)

    # Pack the button for starting/stopping the timer
    def timer_button(self):
        self.t_button.pack(side=BOTTOM)

    # Function for clearing out the time in the timer, and clears out the entry boxes
    def delete_time_func(self):
        self.timer_flag = False
        if self.after_id != None:
            self.master.after_cancel(self.after_id) # cancel anything in the queue
        self.current_seconds = 0.0
        self.timer_label.configure(text=HhMmSs_format(self.current_seconds))
        self.second_entry.delete(0,END)
        self.minute_entry.delete(0,END)
        self.hour_entry.delete(0,END)

    # Pack the button for clearing time and entry boxes
    def delete_time_buttonpack(self):
        self.del_time_button.pack(side=BOTTOM)

    # Helper function used to clear widgets off the window
    def delete_widget(self, widget_name):
        widget_name.pack_forget()

    # Function used to clear widgets off the window
    def timer_back_func(self):
        self.delete_widget(self.t_button)
        self.delete_widget(self.del_time_button)
        self.delete_widget(self.timer_label)
        self.delete_widget(self.timer_title_label)
        self.delete_widget(self.timer_b_button)

        self.delete_widget(self.second_label)
        self.delete_widget(self.second_entry)
        
        self.delete_widget(self.minute_label)
        self.delete_widget(self.minute_entry)
        
        self.delete_widget(self.hour_label)
        self.delete_widget(self.hour_entry)

        self.delete_widget(self.time_setter_button)
        self.choose_win = Choose_Window(self.master)

    # Function for returning to the window for choosing between the stopwatch and timer function
    def timer_back_button(self):
        self.timer_b_button.pack(side=BOTTOM)

    # Function to pack all the text, labels, and entry boxes onto the window to display
    def timer_window(self):
        
        self.timer_title_label.pack()
        self.timer_label.pack(fill=X)
        self.timer_back_button()
        self.timer_button()
        self.set_time_button()
        self.delete_time_buttonpack()
        
        self.timer_entries()
        

class Stopwatch:

    def __init__(self, master):
        self.master = master
        self.current_seconds = 0.00 
        self.after_id = None # id to be used with the after and after_cancel methods
        self.stopwatch_flag = False # indicates if the stopwatch is running or paused
        self.sw_reset_button = Button(self.master, text="Restart", command=self.reset_button_func) # button which resets the stopwatch at 0
        self.sw_button = Button(self.master, text="Start/Stop", command=self.sw_button_func) # button which starts/pauses the stopwatch
        self.sw_b_button = Button(self.master, text="Back", command=self.sw_back_func)

    # get number of seconds elapsed in the stopwatch
    def current_time(self):
        return self.current_seconds

    # pauses stopwatch, prevent incrementing
    def pause_stopwatch(self, id):
        self.master.after_cancel(id)

    # increment seconds to the stopwatch
    def increment_seconds(self):
        self.stopwatch_label.configure(text=HhMmSs_format(self.current_seconds))
        self.current_seconds += 0.01 
        self.after_id = self.master.after(10, self.increment_seconds) # small delay for accurate timing

    # start/resume the stopwatch if it isn't running, or pause it if it is running 
    def sw_button_func(self):
        if not self.stopwatch_flag: # off to on
            self.stopwatch_flag = True
            self.master.after(10, self.increment_seconds)
        else: # on to off
            self.stopwatch_flag = False
            self.pause_stopwatch(self.after_id)

    # Button to start/stop the stopwatch
    def stopwatch_button(self):
        self.sw_button.pack()
    
    # button used to reset the stopwatch time to 0
    def reset_button_func(self):
        self.stopwatch_flag = False
        if self.after_id != None:
            self.master.after_cancel(self.after_id) # cancel anything in the queue
            self.current_seconds = 0.0
            self.stopwatch_label.configure(text=HhMmSs_format(self.current_seconds))
    
    # Button to reset the stopwatch at 0
    def stopwatch_reset_button(self):
        self.sw_reset_button.pack()

    # Helper function to remove widgets off display
    def delete_widget(self, widget_name):
        widget_name.pack_forget()

    # Functon to go to the window to choose between the stopwatch and timer functions
    def sw_back_func(self):
        self.delete_widget(self.sw_title_label)
        self.delete_widget(self.stopwatch_label)
        self.delete_widget(self.sw_button)
        self.delete_widget(self.sw_reset_button)
        self.delete_widget(self.sw_b_button)
        self.choose_win = Choose_Window(self.master)

    # Function to pack the back button
    def sw_back_button(self):
        self.sw_b_button.pack()

    # Function to pack in all the labels, text, and buttons for the stopwatch window
    def stopwatch_window(self):
        self.sw_title_label = Label(text="STOPWATCH", font=("Courier New", 28))
        self.sw_title_label.pack()
        self.stopwatch_label = Label(text=HhMmSs_format(self.current_seconds), font=("Courier New",24))
        self.stopwatch_label.pack()
        self.stopwatch_button()
        self.stopwatch_reset_button()
        self.sw_back_button()
        
# Class contains some widgets to use for the window, to choose between the timer and stopwatch function
class Choose_Window():
    
    def __init__(self, master):
        self.master = master
        self.stopwatch = Stopwatch(self.master)
        self.timer = Timer(self.master)
        self.title = Label(self.master, text=" TIMER PROGRAM ", font=("Courier New", 28))
        self.title.pack()
        self.stopwatch_button(self.master)
        self.timer_button(self.master)
        

    # Helper function to remove widgets off display
    def delete_widget(self, widget_name):
        widget_name.pack_forget()

    # Button to go to the stopwatch window
    def stopwatch_button_func(self):
        self.delete_widget(self.sw_button)
        self.delete_widget(self.timer_button)
        self.delete_widget(self.title)
        self.stopwatch.stopwatch_window()

    def stopwatch_button(self, master):
        self.sw_button = Button(master, text="Stopwatch ⏱️", command=self.stopwatch_button_func, width=10, borderwidth=4)
        self.sw_button.pack()

    # Button to go to the timer window
    def timer_button_func(self):
        self.delete_widget(self.sw_button)
        self.delete_widget(self.timer_button)
        self.delete_widget(self.title)
        self.timer.timer_window()

    def timer_button(self, master):
        self.timer_button = Button(master, text="Timer ⌛", command=self.timer_button_func, width=10, borderwidth=4)
        self.timer_button.pack()

# Main window 
class Main_Window():
    
    def __init__(self):
        self.root = Tk()

        self.stopwatch = Stopwatch(self.root)
        self.timer = Timer(self.root)

        self.choose_win = Choose_Window(self.root)

        self.root.resizable(0, 0) 
        self.root.minsize(275,150)
        self.root.mainloop()
    

win = Main_Window()
