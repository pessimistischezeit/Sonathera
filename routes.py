from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, Remedy, Message, User, bcrypt
from forums import ContactForm, LoginForm, RegisterForm, RemedyForm
from functools import wraps
from sqlalchemy import or_
from ext import app, db




def admin_required(f):
    """Decorator: allow only logged‑in admins; otherwise 403."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not (current_user.is_authenticated and current_user.is_admin):
            abort(403)
        return f(*args, **kwargs)
    return wrapper


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/remedies")
def remedy_list():
    remedies = Remedy.query.all()
    return render_template("remedies.html", remedies=remedies)

@app.route("/remedy/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_remedy():
    form = RemedyForm()
    if form.validate_on_submit():
        new_remedy = Remedy()
        form.populate_obj(new_remedy)
        db.session.add(new_remedy)
        db.session.commit()
        flash("New remedy added successfully!", "success")
        return redirect(url_for("remedy_list"))
    return render_template("add_remedy.html", form=form, edit_mode=False)



@app.route("/remedy/<int:remedy_id>")
def remedy_detail(remedy_id):
    remedy = Remedy.query.get_or_404(remedy_id)
    return render_template("remedy.html", remedy=remedy)

@app.route("/remedy/<int:remedy_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_remedy(remedy_id):
    remedy = Remedy.query.get_or_404(remedy_id)
    form = RemedyForm(obj=remedy)
    if form.validate_on_submit():
        form.populate_obj(remedy) 
        db.session.commit()
        flash("Remedy updated.", "success")
        return redirect(url_for("remedy_detail", remedy_id=remedy.id))
    return render_template("add_remedy.html", form=form, edit_mode=True)

@app.route("/remedy/<int:remedy_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_remedy(remedy_id):
    remedy = Remedy.query.get_or_404(remedy_id)
    db.session.delete(remedy)
    db.session.commit()
    flash("Remedy deleted.", "info")
    return redirect(url_for("remedy_list"))


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        new_msg = Message(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        db.session.add(new_msg)
        db.session.commit()
        flash("Thank you for your message!", "success")
        return redirect(url_for('contact'))

    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template("contact.html", form=form, messages=messages)


@app.route("/faq")
def faq(): 
    return render_template("faq.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('home'))
        flash("Invalid email or password", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered.", "warning")
            return redirect(url_for('register'))

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            is_admin=False,
            password_hash=bcrypt.generate_password_hash(
                form.password.data
            ).decode('utf-8')
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route("/admin")
@login_required
@admin_required
def admin_panel():
    """Simple dashboard showing all data."""
    users = User.query.all()
    remedies = Remedy.query.all()
    messages = Message.query.all()
    return render_template(
        "admin_panel.html",
        users=users,
        remedies=remedies,
        messages=messages
    )


@app.errorhandler(403)
def forbidden(_):
    return render_template("403.html"), 403
