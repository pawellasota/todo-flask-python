from flask import Flask, render_template, request, url_for, Response, redirect, session, g, flash
from flask_login import login_required, current_user, LoginManager, UserMixin
from models.todo import Todo
from models.user import User
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods=["GET", "POST"])
@app.route("/<username>")
def list(username=None):
    """ Shows list of todo items stored in the database.
    """
    if "username" in session:
        redirect(url_for("index"))
    return redirect(url_for("login"))


@app.route("/index")
@app.route("/index/<username>")
def index(username):
    if g.username:
        return render_template("index.html", username=username)
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

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    session.pop("todo_list_id", None)
    return redirect(url_for("login"))

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
    if request.method == "POST":
        if "username" in session:
            session.pop("username", None)
            session.pop("user_id", None)
            session.pop("todo_list_id", None)
        user = User.get_user(request.form["username"], request.form["password"])
        if user:
            session["username"] = user.username
            session["user_id"] = user.user_id
            session["todo_list_id"] = user.todo_list_id
            return redirect(url_for("index", username=user.username))
        else:
            return redirect(url_for("login"))
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
