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
        todo_to_update = Todo_items.query.filter_by(id=self.id).first()
        todo_to_update.name = self.name
        todo_to_update.list_id = self.list_id
        todo_to_update.priority = self.priority
        todo_to_update.due_date = self.due_date
        todo_to_update.creation_date = self.creation_date
        todo_to_update.done = self.done
        db.session.commit()

    def delete(self):
        """ Removes todo item from the database """
        deleted_todo = db.session.query(Todo_items).filter_by(id=self.id).first()
        db.session.delete(deleted_todo)
        db.session.commit()


    @classmethod
    def get_by_id(cls, id):
        """Returns Todo object by id"""
        res = db.session.query(Todo_items).filter_by(id=id).first()
        todo = Todo(res.name, res.list_id, res.priority, res.due_date, res.id, res.done, res.creation_date)
        return todo


    @classmethod
    def get_by_name(cls, name, list_id):
        res = db.session.query(Todo_items).filter_by(name=name, list_id=list_id).first()
        todo = Todo(res.name, res.list_id, res.priority, res.due_date, res.id, res.done, res.creation_date)
        return todo