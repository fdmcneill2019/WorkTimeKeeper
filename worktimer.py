import tkinter as tk
from tkinter import messagebox
from os.path import exists
from datetime import datetime, date
import csv


class WorkTimer(tk.Frame):
    def __init__(self, window=None):
        super().__init__(window)
        self.window = window
        self.new_time = ''
        self.is_running = False
        self.total_hours = 0
        self.total_minutes = 0
        self.total_sec = 0
        self.pack()
        self.gui_components()
        self.time_entry = None
        self.fileurl = "PUT YOUR CSV FILE PATH HERE"
        self.body_fields = ['Date', 'Day of Week', 'Time Type','Time in', 'Time out', 'Duration', 'Comment']
        self.timesheet = TimeSheet(self.fileurl, self.body_fields) 
        
    def gui_components(self): 
        self.time_display = tk.Label(self, text='00:00:00', background="black", foreground="white", font=('arial', 85, 'bold'))
        self.time_display.pack()
        
        self.action_btn = tk.Button(self, text="Start", height=5, width=7, font=('arial', 19, "bold"), background="gray", command=self.start_stop_timer)
        self.action_btn.pack(side=tk.LEFT)
    
        self.save_as_btn = tk.Button(self, text="Save", height=5, width=7, font=('arial', 19, "bold"), background="gray", command=self.save_file)
        self.save_as_btn.pack(side=tk.LEFT)
        
        self.reset_btn = tk.Button(self, text="Reset", height=5, width=7, font=('arial', 19, "bold"), background="gray", command=self.reset_timer)
        self.reset_btn.pack(side=tk.LEFT)
     
        self.exit_btn = tk.Button(self, text="Exit", height=5, width=7, font=('arial', 19, "bold"), background="gray", command=self.window.quit)
        self.exit_btn.pack(side=tk.LEFT)
        
        self.window.title('WorkTimer')
        
    def start_stop_timer(self):
        # Executes if the user starts the timer
        if not self.is_running:
            self.time_display.after(1000, self.update_display())
            self.is_running = True
            
            self.time_entry = TimeEntry(
                date=date.today(),
                day_of_week =date.today().weekday(), # Returns number from 0 to 6
                time_in=datetime.now().strftime("%I:%M:%S %p"))
            return # Exits the function and does not go any futher 
    
        # Only executes if the user stops the timer
        if self.is_running:
            self.time_display.after_cancel(self.new_time)
            self.is_running = False
            
            # Prompts user, asking them if they want to save their time
            answer = messagebox.askquestion("Save", "Do you want to save this time entry?")
            if answer:
                self.time_entry.set_time_out(datetime.now().strftime("%I:%M:%S %p"))
                self.time_entry.set_comment("Rating")
                self.time_entry.set_timed_time(self.time_display['text'])
                self.timesheet.add_body_row(self.time_entry) 
                self.timesheet.write_to_csv_file() 
            else:
                self.time_entry = None;
           
    def reset_timer(self):
        if self.is_running:
            self.action_btn.after_cancel(self.new_time) 
            self.is_running = False
        self.total_hours, self.total_minutes, self.total_sec = 0, 0, 0
        self.time_display.config(text="00:00:00")
        
    # To be fully implemented later
    def save_file(self):
        timesheet.write_to_csv_file()
    
    # Logic for computing and writing out time. Loops every second (1000 ms)
    def update_display(self):
        if self.is_running:
            self.action_btn.config(text="Stop")
        else:
            self.action_btn.config(text="Start")
            
        self.total_sec += 1
        if self.total_sec == 60:
            self.total_minutes += 1
            self.total_sec = 0
        if self.total_minutes == 60 and self.total_hours < 24:
            self.total_hours += 1
            self.total_minutes = 0
        
        # Logic for changing the text string for time_display
        if self.total_hours > 9:
            total_hours_string = f"{self.total_hours}"
        else:
            total_hours_string = f"0{self.total_hours}"
            
        if self.total_minutes > 9:
            total_minutes_string = f"{self.total_minutes}"
        else:
            total_minutes_string = f"0{self.total_minutes}"
            
        if self.total_sec > 9:
            total_sec_string = f"{self.total_sec}"
        else:
            total_sec_string = f"0{self.total_sec}"
        
        self.time_display.config(text=total_hours_string+":"+total_minutes_string+":"+total_sec_string)
        self.new_time = self.time_display.after(1000, self.update_display) 
          

class TimeEntry:
    def __init__(self, date, day_of_week, time_in):
        self.date = date
        self.day_of_week = day_of_week
        self.time_in = time_in
        self.time_out = None
        self.comment = None
        self.timed_time = None     
        
    def get_date(self):
        return self.date
        
    def get_day_of_week(self):
        return self.day_of_week
        
    def set_time_in(self, time_in):
        self.time_in = time_in
        
    def get_time_in(self):
        return self.time_in
        
    def set_time_out(self, time_out):
        self.time_out = time_out
        
    def get_time_out(self):
        return self.time_out
        
    def set_timed_time(self, time):
        self.timed_time = time
       
    def get_timed_time(self):
        return self.timed_time
        
    def set_comment(self, comment):
        self.comment = comment
    
    def get_comment(self):
        return self.comment
        

class TimeSheet:
    def  __init__(self, filename, body_fields):
        self.row_list = []
        self.header_fields = None # May be used in the future
        self.body_fields = body_fields
        self.filename = filename
        self.days = {
            '0': 'Monday',
            '1': 'Tuesday',
            '2': 'Wednesday',
            '3': 'Thursday',
            '4': 'Friday',
            '5': 'Saturday',
            '6': 'Sunday'
        }
     
    # May be refactored in the future to allow multiple rows per save
    def add_body_row(self, time_entry):
        self.row_list = [str(time_entry.get_date()),  
                   self.days[str(time_entry.get_day_of_week())], # Converts int value for day_of_week into String version
                   "Hours Worked",
                   time_entry.get_time_in(), 
                   time_entry.get_time_out(),
                   time_entry.get_timed_time(),
                   time_entry.get_comment()]

    # Written to handle two separate case: (1) when there is an existing file and (2) when there isn't
    def write_to_csv_file(self):
        if exists(self.filename): # Checks to see if file exist already; if it does, open it in append mode
            with open(self.filename, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(self.row_list)
                csvfile.close()
        else:
            with open(self.filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                try:
                    writer.writerow(self.body_fields)
                    writer.writerow(self.row_list)
                    csvfile.close()
                except TypeError:
                    print("Header could not be written")
                self.row_list = []
                
root = tk.Tk() 
app = WorkTimer(window=root)
app.mainloop()
