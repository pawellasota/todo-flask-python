import sqlite3
from models.db import *


class Todo:
    """ Class representing todo item.
        Args:
            name (str): name of todo item
            list_id (int): list id where todo item is
            priority (int): describes priority of todo item
            due_date (str): due date of todo item
            id (int): id of todo item
            done (['True', 'False']: describes if todo item is done or not
            creation_date (str): date of creation of todo item
    """
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
    @classmethod
    def add(cls, item_content, todo_list_id, priority, due_date=None, id=None, done=False):
        """ Removes todo item from the database """
        todo_to_add = Todo_items(item_content, todo_list_id, priority, due_date, id, done)
        session_db.add(todo_to_add)
        session_db.commit()
        return todo_to_add

    def delete(self):
        """ Removes todo item from the database """
        deleted_todo = session_db.query(Todo_items).filter_by(item_id=self.id).first()
        session_db.delete(deleted_todo)
        session_db.commit()


    @classmethod
    def get_by_id(cls, id):
        """Returns Todo object by id"""
        res = session_db.query(Todo_items).filter_by(item_id=id).first()
        todo = Todo(res.item_content, res.todo_list_id, res.priority, res.due_date, res.item_id, res.done, res.creation_date)
        return todo


    @classmethod
    def get_by_name(cls, name, list_id):
        res = session_db.query(Todo_items).filter_by(item_content=name, todo_list_id=list_id).first()
        todo = Todo(res.item_content, res.todo_list_id, res.priority, res.due_date, res.item_id, res.done,
                    res.creation_date)
        return todo