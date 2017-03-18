import sqlite3
import datetime
import models.todo


class TodoList:
    """ Class representing todo item list.
        Args:
            todo_list_id (int): id of list where todo item is
            todo_list_name (str): name of todo list
    """
    path = 'db/db.sqlite'

    def __init__(self, todo_list_id, todo_list_name):
        self.todo_list_id = todo_list_id
        self.todo_list_name = todo_list_name

    @classmethod
    def add_todo_item(cls, todo):
        """ Adds new todo item to data base.
            Args:
                todo (obj): todo object to add
        """
        conn = sqlite3.connect(cls.path)
        creation_date = datetime.date.today()
        conn.execute("insert into todo_items (item_content, todo_list_id, done, priority, due_date,"
                     "creation_date) values('{}','{}','{}','{}','{}','{}')"
                     .format(todo.name, todo.list_id, False, todo.priority, todo.due_date, creation_date))
        conn.commit()
        conn.close()

    @classmethod
    def get_by_id(cls, id):
        """ Returns TodoList object with id given
            Args:
                id (int): todo list id
        """
        conn = sqlite3.connect(cls.path)
        cursor = conn.execute("select * from todo_lists where todo_list_id='{}'".format(id))
        result = cursor.fetchone()
        todoList = TodoList(result[0], result[1])
        conn.close()
        return todoList

    def get_to_do_items(self):
        """ Returns todo items for particular list
        """
        lists = []
        conn = sqlite3.connect(TodoList.path)
        cursor = conn.execute("select * from todo_items where todo_list_id='{}' order by priority desc".format(self.todo_list_id))
        for row in cursor.fetchall():
            lists.append(Todo(row[1], row[2], row[4], row[5], id=row[0], done=row[3], creation_date=row[6]))
        conn.close()
        return lists

    @classmethod
    def get_list_name_by_id(cls, id):
       """ Returns list name containing particular id
            Args:
                id (int): id of list
       """
       conn = sqlite3.connect(cls.path)
       cursor = conn.execute("select todo_list_name from todo_lists where todo_list_id='{}'".format(id))
       name = cursor.fetchone()[0]
       conn.close()
       return name

    def delete(self):
        """ Removes list from database
        """
        conn = sqlite3.connect(TodoList.path)
        conn.execute("delete from todo_lists where todo_list_id='{}'".format(self.todo_list_id))
        conn.execute("delete from todo_items where todo_list_id='{}'".format(self.todo_list_id))
        conn.execute("delete from lists_allowed where list_id='{}'".format(self.todo_list_id))
        conn.commit()
        conn.close()
        return 1