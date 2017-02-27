from flask import Flask, render_template, request, url_for, Response, redirect, session, g, flash
from models.todo import Todo
from models.user import User
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/list_todo_lists")
def list_todo_lists():
    """ Shows list of todo items stored in the database.
    """
    lists = app.config.logged_user.get_lists()
    if lists:
        return render_template("lists.html", lists=lists)
    return redirect(url_for("index"))

@app.route("/list_todo_items/<choosed_list_id>")
def list_todo_items(choosed_list_id=None):
    if choosed_list_id:
        lists = app.config.logged_user.get_to_do_items(choosed_list_id)
        return render_template("lists.html", list_of_items=lists, choosed_list_id=choosed_list_id)

@app.route("/")
@app.route("/index")
@app.route("/index/<username>")
def index(username=None):
    if g.username:
        return render_template("index.html", username=g.username)
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

@app.route("/addlist", methods=["GET", "POST"])
def add_list():
    if request.method == "POST":
        app.config.logged_user.add_list(request.form["list_name"])
        return redirect(url_for("list_todo_lists"))
    return render_template("add_list.html")

@app.route("/add/<choosed_list_id>", methods=['GET', 'POST'])
def add(choosed_list_id):
    """ Creates new todo item
    If the method was GET it should show new item form.
    If the method was POST it shold create and save new todo item.
    """
    if request.method == "POST":
        new_todo_item = Todo(request.form["todo_name"], choosed_list_id, request.form["todo_priority"],
                             request.form["todo_due_date"])
        app.config.logged_user.add_todo_item(new_todo_item)
    return render_template("add_item.html")

@app.route("/remove/<todo_id>")
def remove(todo_id):
    """ Removes todo item with selected id from the database """
    app.config.logged_user.remove_item(todo_id)
    return redirect("index")


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
            session.pop("password", None)
        user = User.get_user(request.form["username"], request.form["password"])
        if user:
            session["username"] = user.username
            session["password"] = user.password
            session["user_id"] = user.user_id
            session["todo_list_id"] = user.todo_list_id
            app.config.logged_user = user
            return redirect(url_for("index", username=user.username))
        else:
            return redirect(url_for("login"))
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
