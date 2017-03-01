import sqlite3
import datetime
from models.todo import Todo



class TodoList:
    path = 'db/db.sqlite'

    def __init__(self, todo_list_id, todo_list_name):
        self.todo_list_id = todo_list_id
        self.todo_list_name = todo_list_name

    @classmethod
    def add_todo_item(cls, todo):
        conn = sqlite3.connect(cls.path)
        creation_date = datetime.date.today()
        conn.execute("insert into todo_items (item_content, todo_list_id, done, priority, due_date,"
                     "creation_date) values('{}','{}','{}','{}','{}','{}')"
                     .format(todo.name, todo.list_id, False, todo.priority, todo.due_date, creation_date))
        conn.commit()
        conn.close()

    @classmethod
    def get_by_id(cls, id):
        conn = sqlite3.connect(cls.path)
        cursor = conn.execute("select * from todo_lists where todo_list_id='{}'".format(id))
        result = cursor.fetchone()
        todoList = TodoList(result[0], result[1])
        conn.close()
        return todoList

    def get_to_do_items(self):
        lists = []
        conn = sqlite3.connect(TodoList.path)
        cursor = conn.execute("select * from todo_items where todo_list_id='{}' order by priority desc".format(self.todo_list_id))
        for row in cursor.fetchall():
            lists.append(Todo(row[1], row[2], row[4], row[5], id=row[0], done=row[3]))
        conn.close()
        return lists

    @classmethod
    def get_list_name_by_id(cls, id):
       conn = sqlite3.connect(cls.path)
       cursor = conn.execute("select todo_list_name from todo_lists where todo_list_id='{}'".format(id))
       name = cursor.fetchone()[0]
       conn.close()
       return name

    def delete(self):
        conn = sqlite3.connect(TodoList.path)
        conn.execute("delete from todo_lists where todo_list_id='{}'".format(self.todo_list_id))
        conn.execute("delete from todo_items where todo_list_id='{}'".format(self.todo_list_id))
        conn.execute("delete from lists_allowed where list_id='{}'".format(self.todo_list_id))
        conn.commit()
        conn.close()