import sqlite3
from models.todo_list import TodoList
from models.todo import Todo
import datetime


class User:
    path = 'db/db.sqlite'

    def __init__(self, user_id, username, password, todo_list_id):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.todo_list_id = todo_list_id

    @classmethod
    def get_user(cls, login, password):
        conn = sqlite3.connect(cls.path)
        cursor = conn.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            if row[1] == login and row[2] == password:
                conn.close()
                return User(row[0], row[1], row[2], row[3])
        conn.close()
        return None

    def get_lists(self):
        lists = []
        conn = sqlite3.connect(User.path)
        cursor = conn.execute("select * from todo_lists where user_id='{}'".format(self.user_id))
        for row in cursor.fetchall():
            lists.append(TodoList(row[0], row[1], row[2]))
        conn.close()
        return lists

    def get_to_do_items(self, list_id):
        lists = []
        conn = sqlite3.connect(User.path)
        cursor = conn.execute("select * from todo_items where todo_list_id='{}'".format(list_id))
        for row in cursor.fetchall():
            lists.append(Todo(row[1], row[2], row[4], row[5], id=row[0], done=row[3]))
        conn.close()
        return lists

    def add_list(self, list_name):
        conn = sqlite3.connect(User.path)
        conn.execute("insert into todo_lists (`todo_list_name`, `user_id`) VALUES('{}', '{}')".format(list_name, self.user_id))
        conn.commit()
        conn.close()

    def remove_item(self, item_id):
        conn = sqlite3.connect(User.path)
        conn.execute("delete from todo_items where item_id='{}'".format(item_id))
        conn.commit()
        conn.close()

    def add_todo_item(self, todo):
        conn = sqlite3.connect(User.path)
        creation_date = datetime.date.today()
        conn.execute("insert into todo_items (item_content, todo_list_id, done, priority, due_date,"
                     "creation_date) values('{}','{}','{}','{}','{}','{}')"
                     .format(todo.name, todo.list_id, False, todo.priority, todo.due_date, creation_date))
        conn.commit()
        conn.close()
