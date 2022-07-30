from flask import Flask, redirect, render_template, flash, session, abort
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, DeleteForm, FeedbackForm

app = Flask(__name__)

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
    """Home page. Redirects to login page."""

    return redirect("/login")

@app.route("/register", methods=['GET', 'POST'])
def show_register_form():
    """Show a form that when submitted will register/create a user. This form should accept a username, password, email, first_name, and last_name."""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)

        db.session.add(user)

        try:
            db.session.commit()

        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another.')
            return render_template('users/register.html', form=form)
        
        session['username'] = user.username
        flash("Account created")
        return redirect(f"/users/{user.username}")

    else:
        return render_template("users/register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def show_login_form():
    """Show a form that when submitted will login a user. This form should accept a username and password. It will return <User> or False"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password"]
            return render_template("users/login.html", form=form)

    
    else:
        return render_template("users/login.html", form=form)


@app.route("/logout")
def logout():
    """Logout"""

    session.pop("username")
    flash("Successfully logged out")
    return redirect("/login")


@app.route("/users/<username>")
def show_user(username):
    """Logged in users"""

    if "username" not in session or username != session['username']:
        abort(401, description="Must be logged in to perform this action")

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("users/show.html", user=user, form=form)


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Removes the user from the database and deletes all of their feedback. Clears any user information in the session and redirect to homepage."""

    if "username" not in session or username != session['username']:
        abort(401, description="Must be logged in to perform this action")
    
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    flash("User deleted")

    return redirect("/")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """Displays a form to add feedback. Adds a new piece of feedback and redirect to /users/<username>"""

    if "username" not in session or username != session['username']:
        abort(401, description="Must be logged in to perform this action")

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    
    else:
        return render_template("feedback/add.html", form=form, username=username)
        


@app.route("/feedback/<int:feedback_id>/edit", methods=["GET", "POST"])
def edit_feedback(feedback_id):
    """Display a form to edit feedback. Update a specific piece of feedback and redirect to /users/<username>"""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        abort(401, description="Must be logged in to perform this action")

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    
    return render_template("/feedback/edit.html", form=form, feedback=feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete a specific piece of feedback and redirect to /users/<username>"""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        abort(401, description="Must be logged in to perform this action")
    
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback deleted")

    return redirect(f"/users/{feedback.username}")

@app.errorhandler(404)
def not_found(error):

    return render_template("404.html")

@app.errorhandler(401)
def custom_401(error):
    
    return render_template("401.html")

