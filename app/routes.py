import os
import secrets
from PIL import Image
from app.models import User, Lesson, Course
from flask import render_template, url_for, flash, redirect, request
from app.forms import RegistrationForm, LoginForm,UpdateProfileForm,NewLessonForm,NewCourseForm
from app import app, bcrypt, db

from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user,
    login_required,
)
lessons = [
    {
        "title":"Request Library Course",
        "course":"Python",
        "author":"Ghassen Ben Taher",
        "thumbnail": "thumbnail.jpg"
        },
    {
            "title":"Cyber Sicurity",
            "course":"Cisco",
            "author":"Ghassen Bouzidi",
            "thumbnail": "thumbnail.jpg"
        },
    {
        "title":"Bootstrap Design",
        "course":"Bootstrap",
        "author":"Waad Bouzidi",
        "thumbnail": "thumbnail.jpg"
    },
    {
        "title":"Master your Ubuntu",
        "course":"Ubuntu",
        "author":"Unknown Author",
        "thumbnail": "thumbnail.jpg"
        },
    {
            "title":"Your deliciouse Omlette ",
            "course":"Kitchen",
            "author":"Rawdha Bouzidi",
            "thumbnail": "thumbnail.jpg"
        },
    {
        "title":"improuve your english level",
        "course":"English",
        "author":"Firas Bouzidi",
        "thumbnail": "thumbnail.jpg"
    },
]

courses = [
    {
        "name":"Python",
        "icon":"python.svg",
        "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Neque quidem nihil dolor officiis at magni!",
    },
    {
        "name":"Data Analysis",
        "icon":"analysis.png",
        "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Neque quidem nihil dolor officiis at magni!",
    },
    {
        "name":"Machine Learning",
        "icon":"machinelearning.png",
        "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Neque quidem nihil dolor officiis at magni!",
    },
    {
        "name": "Web Design",
        "icon": "web.png",
        "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Neque quidem nihil dolor officiis at magni!",
    },
    {
        "name": "Blockchain",
        "icon": "blockchain.png",
        "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Neque quidem nihil dolor officiis at magni!",
    },
    {
        "name": "Tips & Tricks",
        "icon": "idea.png",
        "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Neque quidem nihil dolor officiis at magni!",
    },
]



def save_picture(form_picture):
    """ Fun gives a random name for pictures uploaded from user and save it in userpic folder """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/user_pics", picture_name)
    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_name


def get_previous_next_lesson(lesson):
    course = lesson.course_name
    for lsn in course.lessons:
        if lsn.title == lesson.title:
            index = course.lessons.index(lsn)
            previous_lesson = course.lessons[index - 1] if index > 0 else None
            next_lesson = (
                course.lessons[index + 1] if index < len(course.lessons) - 1 else None
            )
            break
    return previous_lesson, next_lesson


@app.route("/")
@app.route("/home")
def home():
    lessons = Lesson.query.all()
    courses = Course.query.all()
    return render_template("home.html", lessons=lessons, courses=courses)

@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            fname=form.fname.data,
            lname=form.lname.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Account created successfully for {form.username.data}", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash("You have been logged in!", "success")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check credentials", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template("dashboard.html", title="Dashboard", active_tab=None)

@app.route("/dashboard/profile", methods=["GET", "POST"])
@login_required
def profile():
    profile_form = UpdateProfileForm()
    if profile_form.validate_on_submit():
        if profile_form.picture.data:
            picture_file = save_picture(profile_form.picture.data)
            current_user.image_file = picture_file
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        current_user.bio = profile_form.bio.data
        db.session.commit()
        flash("Your profile has been updated", "success")
        return redirect(url_for("profile"))
    elif request.method == "GET":
        profile_form.username.data = current_user.username
        profile_form.email.data = current_user.email
        profile_form.bio.data = current_user.bio
    image_file = url_for("static", filename=f"user_pics/{current_user.image_file}")
    return render_template("profile.html",title="Profile",profile_form=profile_form,image_file=image_file,active_tab="profile",)


@app.route("/dashboard/new_lesson", methods=["GET", "POST"])
@login_required
def new_lesson():
    new_lesson_form = NewLessonForm()
    new_course_form = NewCourseForm()
    return render_template("new_lesson.html",title="New Lesson",new_lesson_form=new_lesson_form,new_course_form=new_course_form,active_tab="new_lesson",)




