import sqlite3


class TodoList:
    def __init__(self, todo_list_id, todo_list_name, user_id):
        self.todo_list_id = todo_list_id
        self.todo_list_name = todo_list_name
        self.user_id = user_id

    # select
    # todo_lists.todo_list_id, todo_lists.todo_list_name, item_id, item_content, done,
    # priority, due_date, creation_date
    # from todo_items, todo_lists
    # where
    # todo_lists.todo_list_id = todo_items.todo_list_id
    # group
    # by
    # todo_items.item_id
    def get_all(self):
        conn = sqlite3.connect(User.path)
        cursor = conn.execute("select * from todo_lists where user_id='{}'".format(self.user_id))
        for row in cursor.fetchall():
            lists.append(TodoList(row[0], row[1], row[2]))
        conn.close()
        return lists

