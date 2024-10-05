from tokenize import String

from todos import TodosList, Todo
import tkinter as tk
from tkinter import LabelFrame, simpledialog, messagebox, font
import time


class ReminderApp:
    def __init__(self, root):
        root.bind('<Destroy>', self.save_data)
        self.root = root
        self.root.title("ToDo App")
        # root.iconbitmap()
        self.todos = TodosList()

        self.font = font.Font(size=16)  # Set font size
        self.root.geometry("500x300")  # Set initial size of the window
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.frame = LabelFrame(root, text="ToDos", padx=5, pady=5, font=self.font)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid(row=0, column=0, sticky="nsew")


        self.frame.todo_listbox = tk.Listbox(self.frame, font=self.font)
        self.frame.todo_listbox.grid(row=0, column=0, sticky="nsew")
        self.frame.todo_listbox.bind('<Double-1>', self.edit_todo)

        add_todo_button = tk.Button(self.frame, text="Add Todo", command=self.add_todo, )
        add_todo_button.grid(row=1, column=0, sticky="nsew", pady=5)  # Place below the todo listbox

    def save_data(self, event=None):
        pass

    def add_todo(self):
        todo_name = simpledialog.askstring("Todo", "Enter todo name:", parent=self.root)
        if todo_name:
            todo = Todo(todo_name, False, time.time())
            self.todos.add_todo(todo)
            self.refresh_todos()

    def edit_todo(self, event):
        selected = self.frame.todo_listbox.curselection()
        if selected:
            todo_name = self.frame.todo_listbox.get(selected[0])
            # ask them what do they want to do with the todo
            # edit, delete, mark as done
            self.refresh_todos()

    def remove_todo(self, event):
        selected = self.frame.todo_listbox.curselection()
        if selected:
            todo_name = self.frame.todo_listbox.get(selected[0])
            # confirmation message
            if self.remove_confirm(todo_name):
                self.todos.remove_todo_by_name(todo_name)
                self.refresh_todos()

    def remove_confirm(self, todo_name):
        return messagebox.askyesno("Delete", "Delete " + todo_name + "?")

    def refresh_todos(self):
        self.frame.todo_listbox.delete(0, tk.END)
        for todo in self.todos.todos:
            self.frame.todo_listbox.insert(tk.END, str(todo))

if __name__ == "__main__":
    root = tk.Tk()
    app = ReminderApp(root)
    root.protocol("WM_DELETE_WINDOW", root.destroy)  # Ensure the Destroy event is triggered on window close
    root.mainloop()
