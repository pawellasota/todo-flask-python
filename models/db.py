from main import db


class Todo_items(db.Model):
    __tablename__ = 'todo_items'

    name = db.Column(db.String(80))
    list_id = db.Column(db.Integer, nullable=False)
    priority = db.Column(db.Integer)
    due_date = db.Column(db.String(10))
    id = db.Column(db.Integer, primary_key=True)
    done = db.Column(db.String(6))
    creation_date = db.Column(db.String(10))

    def __repr__(self):
        return 'Todo: ' % self.name

class Todo_lists(db.Model):
    __tablename__ = 'todo_lists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

class Lists_allowed(db.Model):
    __tablename__ = 'lists_allowed'
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

#
# class Users(Base):
#     __tablename__ = 'users'
#     __table_args__ = {'autoload':True}