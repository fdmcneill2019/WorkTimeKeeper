import tkinter as tk
import pytz
from datetime import datetime
import csv


class TimeKeeper(tk.Frame):
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
        
    def gui_components(self):
        # We use a parameter here, instead of a literal string, to allow the text of the button to change and reflect
        # the state of the program during running time. 
        if self.is_running:
            btn_text = "Stop"
        else:
            btn_text = "Start" 
        
        self.timekeeper_label = tk.Label(self, text='00:00:00', background="black", foreground="white", font=('arial', 85, 'bold'))
        self.timekeeper_label.pack()
        
        self.action_btn = tk.Button(self, text=btn_text, height=5, width=9, font=('arial', 19, "bold"), background="gray")
        self.action_btn.pack(side=tk.LEFT)
        
        self.save_as_btn = tk.Button(self, text="Save As", height=5, width=9, font=('arial', 19, "bold"), background="blue")
        self.save_as_btn.pack(side=tk.LEFT)
        
        self.exit_btn = tk.Button(self, text="Exit", height=5, width=9, font=('arial', 19, "bold"), background="red")
        self.exit_btn.pack(side=tk.LEFT)
        
        self.window.title('TimeKeeper')

class TimeEntry:
    def __init__(self, date, day_of_week):
        self.date = date
        self.day_of_week = day_of_week
        self.time_in = None
        self.time_out = None
        self.comment = None
        
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
        
    def set_comment(self, comment):
        self.comment = comment
    
    def get_comment(self):
        return self.comment
        

class TimeSheet:
    def  __init__(self, filename, header_fields, body_fields, timezone):
        self.dict_list = [] # List of dictionaries for each row
        self.header_fields = header_fields
        self.body_fields = body_fields
        self.timezone = timezone
        self.filename = filename
     
    def add_body_row(self, time_entry):
        row_dict = {'date': time_entry.get_date(), 
                   'day of week': time_entry.get_day_of_week, 
                   'time in': time_entry.get_time_in(), 
                   'time out': time_entry.get_time_out(), 
                   'comment': time_entry.get_comment()}
        dict_list.append(row_dict)
        
        
    # Writes a list of dictionaries to the end of the file.
    # Once dictionaries have been written, the list is reset to empty for new time entries.
    def write_to_csv_file(self):
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, header_fields)
            try:
                writer.writeheader()
            except TypeError:
                print("Header could not be written")
            try:
                writer.writerows(dict_list) # do except handling
            except TypeError:
                print("Rows could not be written")
            dict_list = []


root = tk.Tk() 
app = TimeKeeper(window=root)
app.mainloop()
