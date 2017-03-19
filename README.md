# ToDo Application

Todo application allows to maintain a list of tasks that have priorities and text description.

There are two users initially:

* 'user' with password 'pass'
* 'user2' with password 'pass' 
* 'manager' with password 'pass'

After logging in the user sees todo lists displayed and can choose list of todo's items or add new list.
![alt](http://i66.tinypic.com/24x0w74.png)
In particular list he can manipulate todo items (add/remove/modify entries/set priority/add due date/remove list). 
Todo items have creation date and are sorted by priority also.
There are 10 levels of priority (1-10).

After logging in as manager lists of users are displayed with lists of todo's allowed for modify to them.
Manager is able to assign or remove particular list to user. 
![alt](http://i64.tinypic.com/2lc39j9.png)

# Project tree

 * [models](./models)
   * [todo.py](./models/todo.py)
   * [todo_list.py](./models/todo_list.py)
   * [user.py](./models/user.py)
   * [db.py](./models/db.py)
 * [db](./db)
   * [db.sqlite](./db/db.sqlite)
   * [script.sql](./db/script.sql)
 * [static](./static)
   * [css](./static/css)
     * [style.css](./css/style.css)
   * [img](./static/img)
     * [login.png](./static/img/login.png)
     * [logo-large.png](./static/img/logo-large.png)
     * [ok.png](./static/img/ok.png)
     * [user.png](./static/img/user.png)
   * [js](./static/)
     * [main.js](./static/js/main.js)
   * [templates](./templates)
     * [add_item.html](./templates/add_item.html)
     * [404.html](./templates/404.html)
     * [add_list.html](./templates/add_list.html)
     * [base.html](./templates/base.html)
     * [edit_todo.html](./templates/edit_todo.html)
     * [lists.html](./templates/lists.html)
     * [login.html](./templates/login.html)
     * [manager.html](./templates/manager.html)
     * [show_lists.html](./templates/show_lists.html)
     * [list_todo_items.html](./templates/list_todo_items.html)
* [main.py](./main.py)
* [README.md](./README.md)

* main.py - contains the actual python code that will import the app, start the development server, 
this is file where routes are defined as well.
* /models - this is where classes are stored:
  * User and Manager - defines user who is actually logged in with methods to manipulate todo's
  * Todo - defines single todo entry
  * TodoList - defines single list of todo's
* /static - contains static files of application: CSS, Javascript, images
* /templates - this is where html templates for flask routes are stored


Required modules to pre-install

* Flask — microframework for Python based on Werkzeug and Jinja 2, with hes sub-modules 
    
    
    $ pip install Flask, render_template, request, url_for, redirect, session, g, flash, jsonify
    

    

* JSGlue - provide a Flask object with methods to handle url_for in JavaScript


    $ pip install Flask-JSGlue
* flask_sqlalchemy — Flask microframework extension which adds support for the SQLAlchemy SQL toolkit/ORM.


    $ pip install flask-sqlalchemy
    
* virtualenv(optional) - enables multiple side-by-side installations of Python, one for each project.


    $ sudo apt-get install python-virtualenv

#Getting Started

To get started, you'll want to first clone this GitHub repository locally:

    $ git clone https://github.com/CodecoolKrakow20161/python-flask-todo-pawellasota

In case of problems with database or you just want to return to default data (in /db/db.sqlite):
Create database 'db' in SQLite3, then import sql database from sql file located at /db/script.sql
You can use DBBrowser utility to handle it.

Start application by execute main.py

    $ python3 main.py

You should see something like this:

    $ Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    $ Restarting with stat
    $ Debugger is active!
    $ Debugger pin code: 460-646-704
 
Now server is listening default in port 5000 in your localhost, so start app by writing in your
browser localhost:5000 

#Support

If you are having issues, please let me know.
plasota76@gmail.com