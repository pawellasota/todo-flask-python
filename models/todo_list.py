import datetime
import models.todo
import models.db
import main

class TodoList:
    """ Class representing todo item list.
        Args:
            list_id (int): id of list where todo item is
            name (str): name of todo list
    """

    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def add_todo_item(cls, name, list_id, priority, due_date, done="False"):
        creation_date = datetime.date.today()
        todo_to_add = models.db.Todo_items(name=name, list_id=list_id, priority=priority, due_date=due_date,
                                 done=done, creation_date=creation_date)
        main.db.session.add(todo_to_add)
        main.db.session.commit()
        return todo_to_add

    @classmethod
    def get_by_id(cls, id):
        """ Returns TodoList object with id given
            Args:
                id (int): todo list id
        """
        res = main.db.session.query(models.db.Todo_lists).filter_by(id=id).first()
        todo_list = TodoList(res.id, res.name)
        return todo_list


    def get_to_do_items(self):
        """ Returns todo items for particular list
        """
        lists = []
        res = main.db.session.query(models.db.Todo_items).filter_by(list_id=self.id).order_by("priority desc")
        for row in res:
            lists.append(models.todo.Todo(row.name, row.list_id, row.priority, row.due_date, row.id, row.done, row.creation_date))
        return lists

    @classmethod
    def get_list_name_by_id(cls, id):
        """ Returns list name containing particular id
            Args:
                id (int): id of list
        """
        res = main.db.session.query(models.db.Todo_lists).filter_by(id=id).first()
        return res.name


    def delete(self):
        """ Removes list from database
        """
        main.db.session.query(models.db.Todo_lists).filter_by(id=self.id).delete()
        main.db.session.query(models.db.Todo_items).filter_by(list_id=self.id).delete()
        main.db.session.query(models.db.Lists_allowed).filter_by(list_id=self.id).delete()
        main.db.session.commit()
        return 1