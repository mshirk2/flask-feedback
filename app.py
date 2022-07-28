from flask import Flask, redirect, render_template, flash
from models import db, connect_db, User
from forms import RegisterForm, LoginForm
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Debug Toolbar
from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)


@app.route("/")
def homepage():
    """Home page"""

    return redirect("/register")


@app.route("/register", methods=['GET', 'POST'])
def show_register_form():
    """Show a form that when submitted will register/create a user. This form should accept a username, password, email, first_name, and last_name."""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = User.register(username, form.password.data)
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        db.session.add(user)
        db.session.commit()

        flash(f"Added {username}")
        return redirect("/secret")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def show_login_form():
    """Show a form that when submitted will login a user. This form should accept a username and password."""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        User = User.authenticate(username, password)

        if user:
            session["username"] = Username
            flash(f"Welcome back, {username}")
            return redirect("/secret")
    
    else:
        return render_template("login.html", form=form)


@app.route("/secret")
def show_secret():

    flash("You made it!")


@app.route("/logout")
def logout():

    flash("Logged Out!")

