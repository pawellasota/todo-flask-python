import sqlite3
from models.todo_list import TodoList
from models.todo import Todo
import datetime


class User:
    path = 'db/db.sqlite'

    def __init__(self, user_id, username, password, todo_list_id, type):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.todo_list_id = todo_list_id
        self.type = type

    @classmethod
    def get_user(cls, login, password):
        conn = sqlite3.connect(cls.path)
        cursor = conn.execute("SELECT * FROM users")
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
        list_users = []
        conn = sqlite3.connect(cls.path)
        cursor = conn.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            if row[4] == "user":
                list_users.append(User(row[0], row[1], row[2], row[3], row[4]))
        conn.close()
        return list_users

    def get_lists(self):
        lists = []
        conn = sqlite3.connect(User.path)
        cursor = conn.execute("select todo_list_id, todo_list_name from todo_lists where todo_list_id in "
                              "(select distinct list_id from lists_allowed where "
                              "lists_allowed.user_id='{}')".format(self.user_id))
        for row in cursor.fetchall():
            lists.append(TodoList(row[0], row[1]))
        conn.close()
        return lists

    def add_list(self, list_name):
        conn = sqlite3.connect(User.path)
        conn.execute("insert into todo_lists (`todo_list_name`) VALUES('{}')".format(list_name))
        todo_list_id = conn.execute("select todo_list_id from todo_lists where todo_list_name=('{}')".format(list_name)).fetchone()[0]
        conn.execute("insert into lists_allowed (`user_id`, `list_id`) VALUES('{}', '{}')".format(self.user_id, todo_list_id))
        conn.commit()
        conn.close()


class Manager(User):
    def __init__(self, user_id, username, password, todo_list_id, type):
        super().__init__(user_id, username, password, todo_list_id, type)

    def get_user_list_names(self, user_id):
        list_names = []
        conn = sqlite3.connect(User.path)
        # cursor = conn.execute("SELECT todo_list_name FROM todo_lists, lists_allowed where todo_list_id in"
        #                       " (select list_id from lists_allowed where user_id='{}') group by todo_lists.todo_list_name".format(user_id))
        cursor = conn.execute("SELECT todo_list_name FROM todo_lists, lists_allowed "
                              "where lists_allowed.user_id='{}' and lists_allowed.list_id=todo_lists.todo_list_id".format(user_id))
        for row in cursor.fetchall():
            list_names.append(row)
        conn.close()
        return list_names

    def get_user_id_by_name(self, username):
        conn = sqlite3.connect(User.path)
        cursor = conn.execute("select user_id from users where username='{}'".format(username))
        user_id = cursor.fetchone()[0]
        conn.close()
        return user_id

    def get_list_id_by_name(self, list_name):
        conn = sqlite3.connect(User.path)
        cursor = conn.execute("select todo_list_id from todo_lists where todo_list_name='{}'".format(list_name))
        list_id = cursor.fetchone()[0]
        conn.close()
        return list_id

    def assign_list_to_user(self, user_to_add, list_to_add):
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
        conn = sqlite3.connect(User.path)
        conn.execute("delete from lists_allowed where user_id='{}' and list_id='{}'"
                              .format(self.get_user_id_by_name(choosed_user), self.get_list_id_by_name(choosed_list)))
        conn.commit()
        conn.close()
