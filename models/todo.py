import sqlite3
# from models.user import User


class Todo:
    """ Class representing todo item."""

    def __init__(self, id, name, done=False):
        self.id = id
        self.name = name
        self.done = done

    def toggle(self):
        """ Toggles item's state """
        if self.done:
            self.done = False
        else:
            self.done = True

    def save(self):
        """ Saves/updates todo item in database """
        conn = sqlite3.connect("db/db.sqlite")
        cursor = conn.execute("select * from todo_items where todo_list_id='{}'".format(list_id))
        for row in cursor.fetchall():
            lists.append(Todo(row[0], row[1], row[3]))
        conn.close()

    def delete(self):
        """ Removes todo item from the database """
        pass

    @classmethod
    def get_all(cls):
        """ Retrieves all Todos form database and returns them as list.
        Returns:
            list(Todo): list of all todos
        """
        pass

    @classmethod
    def get_by_id(cls, id):
        """ Retrieves todo item with given id from database.
        Args:
            id(int): item id
        Returns:
            Todo: Todo object with a given id
        """
        pass
