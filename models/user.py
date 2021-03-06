import sqlite3
from models.todo_list import TodoList
import models.db
import main

class User:
    """ Class representing user of todo app.
        Args:
            user_id (int): id of the user
            username (str): name of user
            password (str): password of user
            type (str): Manager or User
    """
    path = 'db/db.sqlite'

    def __init__(self, user_id, username, password, list_allowed_id, type):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.list_allowed_id = list_allowed_id
        self.type = type

    @classmethod
    def get_user(cls, login, password):
        """ On successful authentication returns User or Manager object
            Args:
                login (str): login of the user
                password (str): password of the user
            Returns:
                User (obj): if authentication passed
                None: if authentication fails
        """
        conn = sqlite3.connect(cls.path)
        cursor = conn.execute("SELECT * FROM users where username=? and password=?", (login, password))
        for row in cursor.fetchall():
            if row[1] == login and row[2] == password:
                conn.close()
                if row[4] == "manager":
                    return Manager(row[0], row[1], row[2], row[3], row[4])
                return User(row[0], row[1], row[2], row[3], row[4])
        conn.close()
        return None

    @classmethod
    def get_all_users(cls):
        """ Returns list of all User objects from database
        """
        list_users = []
        conn = sqlite3.connect(cls.path)
        cursor = conn.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            if row[4] == "user":
                list_users.append(User(row[0], row[1], row[2], row[3], row[4]))
        conn.close()
        return list_users

    def get_lists(self):
        """ Returns list of TodoList for particular user
        """
        lists = []
        conn = sqlite3.connect(User.path)
        cursor = conn.execute("select id, name from todo_lists where id in "
                              "(select distinct list_id from lists_allowed where "
                              "lists_allowed.user_id='{}')".format(self.user_id))
        for row in cursor.fetchall():
            lists.append(TodoList(row[0], row[1]))
        conn.close()
        return lists

    def add_list(self, list_name):
        """Adds new list to database
            Args:
                list_name (str): name for new list
            Returns:
                "success" (str): if list was added
                "fail": if list with name given already exists in database
        """
        res = main.db.session.query(models.db.Todo_lists).filter_by(name=list_name).first()
        if res:
            return None
        list_to_add = models.db.Todo_lists(name=list_name)
        main.db.session.add(list_to_add)
        main.db.session.commit()
        list_allowed_to_add = models.db.Lists_allowed(list_id=list_to_add.id, user_id=self.user_id)
        main.db.session.add(list_allowed_to_add)
        main.db.session.commit()
        return TodoList(list_to_add.id, list_to_add.name)

class Manager(User):
    """ Class representing manager of todo app.
        Args:
            user_id (int): id of the user
            username (str): name of user
            password (str): password of user
            type (str): Manager or User
    """
    def __init__(self, user_id, username, password, list_allowed_id, type):
        super().__init__(user_id, username, password, list_allowed_id, type)

    def get_user_list_names(self, user_id):
        """ Returns list of user TodoLists names
        """
        list_names = []
        conn = sqlite3.connect(User.path)
        cursor = conn.execute("SELECT name FROM todo_lists, lists_allowed "
                              "where lists_allowed.user_id='{}' and lists_allowed.list_id=todo_lists.id".format(user_id))
        for row in cursor.fetchall():
            list_names.append(row)
        conn.close()
        return list_names

    def get_all_lists(self):
        """ Returns all list names from database
        """
        list_names = []
        conn = sqlite3.connect(User.path)
        cursor = conn.execute("SELECT name FROM todo_lists")
        for row in cursor.fetchall():
            list_names.append(row)
        conn.close()
        return list_names


    def get_user_id_by_name(self, username):
        """ Returns id number of User with username given
        """
        conn = sqlite3.connect(User.path)
        cursor = conn.execute("select user_id from users where username='{}'".format(username))
        user_id = cursor.fetchone()[0]
        conn.close()
        return user_id

    def get_list_id_by_name(self, list_name):
        """ Returns id of list with name given
        """
        conn = sqlite3.connect(User.path)
        cursor = conn.execute("select id from todo_lists where name='{}'".format(list_name))
        list_id = cursor.fetchone()[0]
        conn.close()
        return list_id

    def assign_list_to_user(self, user_to_add, list_to_add):
        """ Gives permission for using particular list for user
            Args:
                user_to_add (str): user which gains access for list
                list_to_add (str): list for user
            Returns:
                True: if assigning passed
                None: if assigning fails
        """
        conn = sqlite3.connect(User.path)
        cursor = conn.execute("select user_id from lists_allowed where list_id='{}' "
                              "and user_id='{}'".format(self.get_list_id_by_name(list_to_add), self.get_user_id_by_name(user_to_add)))
        data = cursor.fetchone()
        if not data:
            conn.execute("insert into lists_allowed (`user_id`, `list_id`) values ('{}', '{}')"
                                  .format(self.get_user_id_by_name(user_to_add), self.get_list_id_by_name(list_to_add)))
        else:
            conn.close()
            return None
        conn.commit()
        conn.close()
        return True

    def remove_access_to_list(self, choosed_user, choosed_list):
        """Removes permission for using particular list for user
            Args:
                choosed_user (str): user which loose access for list
                choosed_list (str): list for user
            Returns:
                None
        """
        conn = sqlite3.connect(User.path)
        conn.execute("delete from lists_allowed where user_id='{}' and list_id='{}'"
                              .format(self.get_user_id_by_name(choosed_user), self.get_list_id_by_name(choosed_list)))
        conn.commit()
        conn.close()
