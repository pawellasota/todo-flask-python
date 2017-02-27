import sqlite3

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
                return User(row[0], row[1], row[2], row[3])
        return None
