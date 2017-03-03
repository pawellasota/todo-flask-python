import sqlite3
import datetime


class Todo:
    """ Class representing todo item."""
    path = 'db/db.sqlite'

    def __init__(self, name, list_id, priority, due_date, id=None, done=False, creation_date=None):
        self.id = id
        self.name = name
        self.list_id = list_id
        self.priority = priority
        self.due_date = due_date
        self.done = done
        self.creation_date = creation_date

    def toggle(self):
        """ Toggles item's state """
        if self.done:
            self.done = False
        else:
            self.done = True

    def save(self):
        """ Saves/updates todo item in database """
        conn = sqlite3.connect("db/db.sqlite")
        conn.execute("update todo_items set item_content='{}', priority='{}', due_date='{}', done='{}'"
                              " where item_id='{}'".format(self.name, self.priority, self.due_date, self.done, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        """ Removes todo item from the database """
        conn = sqlite3.connect(Todo.path)
        conn.execute("delete from todo_items where item_id='{}'".format(self.id))
        conn.commit()
        conn.close()

    @classmethod
    def get_by_id(cls, id):
        conn = sqlite3.connect(cls.path)
        cursor = conn.execute("select * from todo_items where item_id='{}'".format(id))
        result = cursor.fetchone()
        todo = Todo(result[1], result[2], result[4], result[5], result[0], result[3], result[6])
        conn.close()
        return todo
