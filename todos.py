from time import ctime


class TodosList:
    def __init__(self):
        self.todos = []

    def add_todo(self, todo):
        # TODO: validation, duplicates etc
        if todo:
            self.todos.append(todo)

    def delete_task(self, index):
        if 0 <= index < len(self.todos):
            del self.todos[index]

    def get_list(self):
        return self.todos

    def remove_todo_by_name(self, todo_name):
        for todo in self.todos:
            if str(todo) == todo_name:
                self.todos.remove(todo)


class Todo:
    def __init__(self, task, completed, due_time):
        if not task:
            raise ValueError("Task cannot be empty")
        self.name = task
        if completed not in [True, False]:
            raise ValueError("Completed must be a boolean")
        self.completed = completed
        if due_time:
            self.due_time = due_time
        #if due_date:
        #    self.due_date = due_date

    def __str__(self):
        return str(self.name + " " + self.completed_string() + " " + str(self.due_string()))

    def completed_string(self):
        if self.completed:
            return '✓'
        else:
            return '✗'

    def due_string(self):
        if self.due_time :
            return(ctime(self.due_time))
        else:
            return ''

