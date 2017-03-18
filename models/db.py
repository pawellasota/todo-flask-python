from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from sqlalchemy import SQLAlchemy
import os


engine = create_engine('sqlite:////' + os.getcwd() + '/db/db.sqlite', echo=True)
Base = declarative_base(engine)
metadata = Base.metadata
Session = sessionmaker(bind=engine)
session_db = Session()
# db = SQLAlchemy(app)

class Todo_items(Base):
    __tablename__ = 'todo_items'
    __table_args__ = {'autoload':True}

    def __init__(self, item_content, todo_list_id, priority, due_date, item_id=None, done=False, creation_date=None):
        self.item_content = item_content
        self.todo_list_id = todo_list_id
        self.priority = priority
        self.due_date = due_date
        self.item_id = item_id
        self.done = done
        self.creation_date = creation_date


class Todo_lists(Base):
    __tablename__ = 'todo_lists'
    __table_args__ = {'autoload':True}

class Lists_allowed(Base):
    __tablename__ = 'lists_allowed'
    __table_args__ = {'autoload':True}

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'autoload':True}