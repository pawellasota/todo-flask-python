from flask import Flask, render_template, request, url_for, Response, redirect, session, g, flash
from flask_login import login_required, current_user, LoginManager, UserMixin
from models.todo import Todo
from models.user import User
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods=["GET", "POST"])
def list(user=None):
    """ Shows list of todo items stored in the database.
    """
    if request.method == "POST":
        session.pop("username", None)
        session.pop("user_id", None)
        session.pop("todo_list_id", None)
        user = User.get_user(request.form["username"], request.form["password"])
        if user:
            session["username"] = user.username
            session["user_id"] = user.user_id
            session["todo_list_id"] = user.todo_list_id
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid input")

    return render_template("login.html", title="Login")


@app.route("/index")
def index():
    if g.username:
        return render_template("index.html")
    return redirect(url_for("login"))

@app.before_request
def before_request():
    g.username = None
    g.user_id = None
    g.todo_list_id = None
    if "username" in session:
        g.username = session["username"]
        g.user_id = session["user_id"]
        g.todo_list_id = session["todo_list_id"]

@app.route("/getsession")
def get_session():
    if "user" in session:
        return session["user"]
    else:
        return "Not logged in"

@app.route("/dropsession")
def drop_session():
    session.pop("user", None)
    return "Dropped"

@app.route("/add", methods=['GET', 'POST'])
def add():
    """ Creates new todo item
    If the method was GET it should show new item form.
    If the method was POST it shold create and save new todo item.
    """
    return "Add todo"


@app.route("/remove/<todo_id>")
def remove(todo_id):
    """ Removes todo item with selected id from the database """
    return "Remove " + todo_id


@app.route("/edit/<todo_id>", methods=['GET', 'POST'])
def edit(todo_id):
    """ Edits todo item with selected id in the database
    If the method was GET it should show todo item form.
    If the method was POST it shold update todo item in database.
    """
    return "Edit " + todo_id


@app.route("/toggle/<todo_id>")
def toggle(todo_id):
    """ Toggles the state of todo item """
    return "Toggle " + todo_id

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    if request.method == "POST":
        _user = User.get_user(request.form["email"], request.form["password"])
        if _user:
            return redirect("/"+_user.username)
        else:
            return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
