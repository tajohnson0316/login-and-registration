from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user_model import User


# Login and registration routes
@app.route("/", methods=["GET"])
@app.route("/registration", methods=["GET"])
@app.route("/login", methods=["GET"])
def display_login_registration():
    return render_template("index.html")


# Create new user route
@app.route("/users/new", methods=["POST"])
def create_user():
    if not User.validate_user(request.form):
        return redirect("/")

    # Assign a valid user's id to session
    session["user_id"] = User.create_one(
        {**request.form, "password": User.encrypt_string(request.form["password"])}
    )

    return redirect("/home")


# Login route
@app.route("/users/login", methods=["POST"])
def login():
    email = request.form["email"]
    if not User.validate_login_email(email):
        return redirect("/")

    user = User.get_one_with_email({"email": email})

    if not User.validate_password(user.password, request.form["password"]):
        return redirect("/")

    session["user_id"] = user.id

    return redirect("/home")


# Display homepage route
@app.route("/home", methods=["GET"])
def display_homepage():
    if not "user_id" in session:
        return redirect("/")
    return render_template("home.html", user=User.get_one({"id": session["user_id"]}))


# Log out route
@app.route("/users/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")
