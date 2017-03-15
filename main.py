from flask import Flask, render_template, request, url_for, redirect, session, g, flash, jsonify
from models.todo import Todo
from models.user import User
from models.todo_list import TodoList
from flask_jsglue import JSGlue
import os, datetime

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
    """ Shows all lists of todo's of particular user
    """
    lists = g.logged_user.get_lists()
    return render_template("lists.html", lists=lists)

@app.route("/get_todo_items")
def list_todo_items():
    """ Shows all todo's from choosen list
    """
    list_id = request.args["list_id"]
    if list_id:
        todo_list = TodoList.get_by_id(list_id.strip('list_'))
        list_of_items = todo_list.get_to_do_items()
        return render_template("list_todo_items.html", list_of_items=list_of_items, choosed_list=todo_list)

@app.route("/")
@app.route("/index")
def index():
    """ App root. Depending on type of user ('user' or 'manager') routes him for expected view
    """
    if g.logged_user is not None:
        if g.logged_user.type == "manager":
            return redirect(url_for("manager"))
        else:
            return redirect(url_for("user"))
    else:
        return redirect(url_for("login"))

@app.route("/manager", methods=["GET", "POST"])
def manager():
    """ Shows view for manager
    """
    if request.args.get("choosed_user"):
        g.logged_user.remove_access_to_list(request.args.get("choosed_user"), request.args.get("choosed_list"))
        return redirect("manager")
    users_list_names = []
    users_list = g.logged_user.get_all_users()
    full_list = g.logged_user.get_all_lists()
    if full_list:
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
    """ Check if session for user is still up, assign current user object to global g
    """
    setattr(g, 'logged_user', None)
    if "username" in session:
        g.logged_user = app.config.logged_user

@app.route("/logout")
def logout():
    """ Log out current user
    """
    session.pop("username", None)
    flash("Logged out successfully", "alert alert-success text-centered")
    return redirect(url_for("login"))

@app.route("/addlist", methods=["GET", "POST"])
def add_list():
    """ Adds new list for user if method was POST, shows form for add list if method was GET
    """
    if request.method == "POST":
        list_name = request.form["list_name"]
        todo_list = g.logged_user.add_list(list_name)
        if todo_list:
            return jsonify({"list_id": todo_list.todo_list_id,
                            "todo_list_name": todo_list.todo_list_name})
        else:
            return jsonify({"error": "List already exists"})
    return render_template("add_list.html")

@app.route("/add", methods=['GET', 'POST'])
def add():
    """ Creates new todo item. If the method was GET it shows new item form.
        If the method was POST it creates and save new todo item.
    """
    if request.method == "POST":
        choosed_list_id = request.form["choosed_list_id"]
        new_todo_item = Todo(request.form["todo_name"], choosed_list_id.strip("add_todo_submit_"), request.form["todo_priority"],
                             request.form["todo_due_date"])
        TodoList.add_todo_item(new_todo_item)
        new_todo_item = Todo.get_by_name(request.form["todo_name"], choosed_list_id.strip("add_todo_submit_"))
        return jsonify({
                        'item_id': new_todo_item.id,
                        'item_content': new_todo_item.name,
                        'list_id': new_todo_item.list_id,
                        'priority': new_todo_item.priority,
                        'due_date': new_todo_item.due_date,
                        'done': new_todo_item.done,
                        'creation_date': new_todo_item.creation_date
                        })
    choosed_list_id = request.args["choosed_list_id"]
    choosed_list = TodoList.get_by_id(choosed_list_id.strip("add_new_todo_"))
    return render_template("add_item.html", choosed_list=choosed_list)

@app.route("/remove")
def remove():
    """ Removes todo item with selected id from the database """
    todo_id = request.args["todo_id"]
    todo = Todo.get_by_id(todo_id.strip("remove_"))
    todo.delete()
    return jsonify({"todo_name": todo.name})

@app.route("/remove_list")
def remove_list():
    """ Removes particular list from database
    """
    list_id = request.args["list_id"]
    list_id = list_id.strip('rem_list_')
    list = TodoList.get_by_id(list_id)
    if list.delete():
        return jsonify({'list_id': list.todo_list_id,
                        'list_name': list.todo_list_name})
    else:
        return jsonify({'error': 'Delete operation failed'})

@app.route("/edit", methods=['GET', 'POST'])
def edit():
    """ Edits todo item with selected id in the database
        If the method was GET it shows todo item form.
        If the method was POST it updates todo item in database.
    """

    if request.method == "POST":
        todo_id = request.form["todo_id"]
        todo = Todo.get_by_id(todo_id.strip("update_todo_"))
        todo.name = request.form["todo_name"]
        todo.due_date = request.form["todo_due_date"]
        todo.priority = request.form["todo_priority"]
        todo.save()
        return jsonify({"todo_name": todo.name})
    todo_id = request.args["todo_id"]
    todo = Todo.get_by_id(todo_id.strip("edit_"))
    list_name = TodoList.get_list_name_by_id(todo.list_id)
    return render_template("edit_todo.html", todo=todo, list_name=list_name)


@app.route("/toggle")
def toggle():
    """ Toggles the state of todo item """
    todo_id = request.args["todo_id"]
    todo = Todo.get_by_id(todo_id.strip("todo_"))
    if todo.done == "True":
        todo.done = "False"
    else:
        todo.done = "True"
    todo.save()
    return todo.done

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Shows login form if method was GET. Log user if method was POST.
    """
    if request.method == "POST":
        logged_user = User.get_user(request.form["username"], request.form["password"])
        if logged_user:
            session["username"] = logged_user.username
            app.config.logged_user = logged_user
            flash('You were successfully logged in', "alert alert-success text-centered")
            return redirect(url_for("index"))
        else:
            flash("Your login data was incorrect", "alert alert-danger text-centered")
    return render_template("login.html")

# @app.route("/get_todo_list", methods=["POST"])
# def get_todo_list():
#     list_id = request.form["list_id"]


@app.errorhandler(404)
def page_not_found(error):
    """ Basic 404 error handle. Redirect to login page.
    """
    flash("Invalid address: "+str(error), "alert alert-danger text-centered")
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
