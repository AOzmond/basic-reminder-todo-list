import time
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog, font

class ReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reminder App")
        self.root.geometry("300x300")  # Set initial size of the window
        self.reminders = {}

        self.font = font.Font(size=16)  # Set font size

        self.reminder_listbox = tk.Listbox(root, font=self.font)
        self.reminder_listbox.pack()
        self.reminder_listbox.bind('<Double-1>', self.remove_reminder)  # Bind double-click event

        add_button = tk.Button(root, text="Add Reminder", command=self.add_reminder, font=self.font)
        add_button.pack()

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
        messagebox.showinfo("Reminder", f"Reminder: {reminder_name}")
        self.remove_reminder()


if __name__ == "__main__":
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()