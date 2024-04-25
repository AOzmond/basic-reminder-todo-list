import time
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog, font
import pickle

class ReminderApp:
    def __init__(self, root):
        root.bind('<Destroy>', self.save_data)
        self.root = root
        self.root.title("Reminder App")
        self.root.geometry("500x300")  # Set initial size of the window
        self.reminders = {}
        self.todos = {}

        self.font = font.Font(size=16)  # Set font size

        self.reminder_listbox = tk.Listbox(root, font=self.font)
        self.reminder_listbox.grid(row=0, column=0)  # Place in the first column
        self.reminder_listbox.bind('<Double-1>', self.remove_reminder)

        self.todo_listbox = tk.Listbox(root, font=self.font)
        self.todo_listbox.grid(row=0, column=1)  # Place in the second column
        self.todo_listbox.bind('<Double-1>', self.remove_todo)

        add_button = tk.Button(root, text="Add Reminder", command=self.add_reminder, font=self.font)
        add_button.grid(row=1, column=0)  # Place below the reminder listbox

        add_todo_button = tk.Button(root, text="Add Todo", command=self.add_todo, font=self.font)
        add_todo_button.grid(row=1, column=1)  # Place below the todo listbox
    
        try:
            with open('reminders.pkl', 'rb') as f:
                self.reminders = pickle.load(f)
            for reminder in self.reminders:
                self.reminder_listbox.insert(tk.END, reminder)
        except FileNotFoundError:
            self.reminders = {}

        try:
            with open('todos.pkl', 'rb') as f:
                self.todos = pickle.load(f)
            for todo in self.todos:
                self.todo_listbox.insert(tk.END, todo)
        except FileNotFoundError:
            self.todos = {}

    def save_data(self, event=None):
        with open('reminders.pkl', 'wb') as f:
            pickle.dump(self.reminders, f)
        with open('todos.pkl', 'wb') as f:
            pickle.dump(self.todos, f)

    def add_reminder(self):
        reminder_name = simpledialog.askstring("Reminder", "Enter reminder name:", parent=self.root)
        reminder_time = simpledialog.askfloat("Reminder", "Enter reminder time in minutes:", parent=self.root)
        if reminder_name and reminder_time:
            self.reminders[reminder_name] = {'time': reminder_time, 'label': self.reminder_listbox.size()}
            self.reminder_listbox.insert(tk.END, f"{reminder_name}: {reminder_time} minutes")
            threading.Thread(target=self.start_countdown, args=(reminder_name, reminder_time * 60)).start()

    def remove_reminder(self, event=None):
        selected = self.reminder_listbox.curselection()
        if selected:
            reminder_name = self.reminder_listbox.get(selected[0]).split(':')[0]
            if reminder_name in self.reminders:
                confirm = messagebox.askyesno("Confirmation", f"Do you want to remove {reminder_name}?")
                if confirm:
                    del self.reminders[reminder_name]
                    self.reminder_listbox.delete(selected[0])

    def start_countdown(self, reminder_name, reminder_time_seconds):
        for i in range(int(reminder_time_seconds), 0, -1):
            mins, secs = divmod(i, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            self.reminder_listbox.delete(self.reminders[reminder_name]['label'])
            self.reminder_listbox.insert(self.reminders[reminder_name]['label'], f"{reminder_name}: {timeformat}")
            self.root.update()
            time.sleep(1)
        self.show_reminder_popup(reminder_name)

    def show_reminder_popup(self, reminder_name):
        popup = tk.Toplevel()
        popup.title("Reminder")
        popup.geometry("200x150")
        message_label = tk.Label(popup, text=f"Reminder: {reminder_name}", font=self.font)
        message_label.pack()
        acknowledge_button = tk.Button(popup, text="Acknowledge", command=popup.destroy, font=self.font)
        acknowledge_button.pack()
        reset_button = tk.Button(popup, text="Reset", command=lambda: self.reset_reminder(reminder_name, popup), font=self.font)
        reset_button.pack()

    def reset_reminder(self, reminder_name, popup):
        reminder_time = simpledialog.askfloat("Reminder", "Enter new reminder time in minutes:", parent=self.root)
        if reminder_time:
            self.reminders[reminder_name]['time'] = reminder_time
            threading.Thread(target=self.start_countdown, args=(reminder_name, reminder_time * 60)).start()
        popup.destroy()
    
    def add_todo(self):
        todo_name = simpledialog.askstring("Todo", "Enter todo name:", parent=self.root)
        if todo_name:
            self.todos[todo_name] = {'label': self.todo_listbox.size()}
            self.todo_listbox.insert(tk.END, f"{todo_name}")

    def remove_todo(self, event=None):
        selected = self.todo_listbox.curselection()
        if selected:
            todo_name = self.todo_listbox.get(selected[0])
            if todo_name in self.todos:
                confirm = messagebox.askyesno("Confirmation", f"Do you want to remove {todo_name}?")
                if confirm:
                    del self.todos[todo_name]
                    self.todo_listbox.delete(selected[0])

if __name__ == "__main__":
    root = tk.Tk()
    app = ReminderApp(root)
    root.protocol("WM_DELETE_WINDOW", root.destroy)  # Ensure the Destroy event is triggered on window close
    root.mainloop()