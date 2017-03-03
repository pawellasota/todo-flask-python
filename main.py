from flask import Flask, render_template, request, url_for, Response, redirect, session, g, flash
from models.todo import Todo
from models.user import User, Manager
from models.todo_list import TodoList
from flask_jsglue import JSGlue
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)
jsglue = JSGlue(app)

@app.route("/list_todo_lists")
def list_todo_lists():
    """ Shows list of todo items stored in the database.
    """
    lists = g.logged_user.get_lists()
    if lists:
        return render_template("lists.html", lists=lists)
    return redirect(url_for("index"))

@app.route("/user")
def user():
    """ Shows list of todo items stored in the database.
    """
    lists = g.logged_user.get_lists()
    if lists:
        return render_template("lists.html", lists=lists)
    return redirect(url_for("index"))

@app.route("/list_todo_items/<choosed_list_id>")
def list_todo_items(choosed_list_id):
    if choosed_list_id:
        todo_list = TodoList.get_by_id(choosed_list_id)
        list_of_items = todo_list.get_to_do_items()
        return render_template("lists.html", list_of_items=list_of_items, choosed_list=todo_list)

@app.route("/")
@app.route("/index")
def index():
    if g.logged_user:
        if g.logged_user.type == "manager":
            return redirect(url_for("manager"))
        else:
            return redirect(url_for("user"))
    else:
        return redirect(url_for("login"))

@app.route("/manager", methods=["GET", "POST"])
def manager():
    if request.args.get("choosed_user"):
        g.logged_user.remove_access_to_list(request.args.get("choosed_user"), request.args.get("choosed_list"))
        return redirect("manager")
    users_list_names = []
    users_list = g.logged_user.get_all_users()
    full_list = g.logged_user.get_all_lists()
    for user in users_list:
        users_list_names.append([user.user_id, g.logged_user.get_user_list_names(user.user_id)])
    if request.method == "POST":
        g.logged_user.assign_list_to_user(request.form["user_to_add"], request.form["list_to_add"])
        users_list_names = []
        for user in users_list:
            users_list_names.append([user.user_id, g.logged_user.get_user_list_names(user.user_id)])
    return render_template("manager.html", users_list=users_list, user_list_names=users_list_names, full_list=full_list)

@app.before_request
def before_request():
    if "username" in session:
        setattr(g, 'logged_user', User.get_user(session['username'], session['password']))
    else:
        setattr(g, 'logged_user', None)

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("password", None)
    return redirect(url_for("login"))

@app.route("/addlist", methods=["GET", "POST"])
def add_list():
    if request.method == "POST":
        g.logged_user.add_list(request.form["list_name"])
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
        TodoList.add_todo_item(new_todo_item)
        return redirect(url_for("list_todo_items", choosed_list_id=choosed_list_id))
    return render_template("add_item.html")

@app.route("/remove/<todo_id>")
def remove(todo_id):
    """ Removes todo item with selected id from the database """
    todo = Todo.get_by_id(todo_id)
    choosed_list_id = todo.list_id
    todo.delete()
    return redirect(url_for("list_todo_items", choosed_list_id=choosed_list_id))

@app.route("/remove_list/<choosed_list_id>")
def remove_list(choosed_list_id):
    list = TodoList.get_by_id(choosed_list_id)
    list.delete()
    return redirect("list_todo_lists")

@app.route("/edit/<todo_id>", methods=['GET', 'POST'])
def edit(todo_id):
    """ Edits todo item with selected id in the database
    If the method was GET it should show todo item form.
    If the method was POST it shold update todo item in database.
    """
    todo = Todo.get_by_id(todo_id)
    if request.method == "POST":
        todo.name = request.form["todo_name"]
        todo.due_date = request.form["todo_due_date"]
        todo.priority = request.form["todo_priority"]
        todo.save()
        return redirect(url_for("list_todo_items", choosed_list_id=todo.list_id))
    choosed_list_name = TodoList.get_list_name_by_id(todo.list_id)
    return render_template("edit_todo.html", todo=todo, choosed_list_name=choosed_list_name)


@app.route("/toggle/<todo_id>, <checked>")
def toggle(todo_id, checked):
    """ Toggles the state of todo item """
    todo = Todo.get_by_id(todo_id)
    if checked == "True":
        todo.done = "True"
    else:
        todo.done = "False"
    todo.save()
    return redirect(url_for("list_todo_items", choosed_list_id=todo.list_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        logged_user = User.get_user(request.form["username"], request.form["password"])
        if logged_user:
            session["username"] = logged_user.username
            session["password"] = logged_user.password
            return redirect(url_for("index"))
        else:
            error = "Your login data was incorect"
    return render_template("login.html", error=error)

if __name__ == "__main__":
    app.run(debug=True)
