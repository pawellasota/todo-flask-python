# ToDo Application

Todo application allows to maintain a list of tasks that have priorities and text description.

There are two users initially:

* 'user' with password 'pass'
* 'user2' with password 'pass' 
* 'manager' with password 'pass'

After logging in the user sees todo lists displayed and can choose list of todo's items or add new list.
![alt](https://goo.gl/photos/XcspUL3q8J5EhVoF6)
In particular list he can manipulate todo items (add/remove/modify entries/set priority/add due date/remove list). 
Todo items have creation date and are sorted by priority also.
There are 10 levels of priority (1-10).

After logging in as manager lists of users are displayed with lists of todo's allowed for modify to them.
Manager is able to assign or remove particular list to user. 
![alt](https://goo.gl/photos/VHj3zXEWWqpjcya18)

# Project tree

 * [models](./models)
   * [todo.py](./models/todo.py)
   * [todo_list.py](./models/todo_list.py)
   * [user.py](./models/user.py)
 * [db](./db)
   * [db.sqlite](./db/db.sqlite)
   * [script.sql](./db/script.sql)
 * [static](./static)
   * [css](./static/css)
     * [style.css](./css/style.css)
   * [img](./static/img)
     * [login.png](./static/img)
     * [logo-large.png](./static/img)
     * [ok.png](./static/img)
     * [user.png](./static/img)
   * [js](./static/)
     * [main.js](./static/js)
   * [templates](./static/templates)
     * [add_item.html](./static/templates)
     * [add_list.html](./static/templates)
     * [base.html](./static/templates)
     * [edit_todo.html](./static/templates)
     * [index.html](./static/templates)
     * [lists.html](./static/templates)
     * [login.html](./static/templates)
     * [manager.html](./static/templates)
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


Included modules support

* Flask — base framework for everything.
* JSGlue - provide a Flask object with methods to handle url_for in JavaScript


#Getting Started

To get started, you'll want to first clone this GitHub repository locally:

    $ git clone https://github.com/CodecoolKrakow20161/python-flask-todo-pawellasota

Install virtualenv(optional) - enables multiple side-by-side installations of Python, one for each project.
    
    $ sudo apt-get install python-virtualenv

Create database 'db' in SQLite3, then import sql database from sql file located at /db/script.sql.
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

Support
-------

If you are having issues, please let me know.
plasota76@gmail.com