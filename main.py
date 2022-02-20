from flask import render_template, request, redirect, jsonify, url_for, session, flash
from clarifai import get_images, get_all_images, upload_db_t, classify_image, get_concepts
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from datetime import timedelta
from werkzeug.routing import BuildError
from flask_bcrypt import check_password_hash
from flask_login import (
    login_user,
    logout_user,
    login_required,
)

from app import create_app, db, login_manager, bcrypt
from models import User
from forms import login_form, register_form


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app = create_app()


@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)


def get_classes():
    """
    Get classes from clarifai
    """
    return get_concepts()


def upload_db(bytes, classification):
    """
    temporarily stored locally
    """
    upload_db_t(bytes, classification)
    # f = open(f'./out/image-{classification}.png', 'wb')
    # f.write(bytes)
    # f.close()
    return True


@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect('/')
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("auth.html",
                            page_name="login",
                            form=form,
                            text="Login",
                            title="Login",
                            btn_action="Login"
                        )

@app.route('/')
def home():
    return render_template('index.html', page_name="home")


@app.route('/explore')
def explore_page():
    return render_template('explore.html',
                           page_name="explore",
                           options=get_classes(),
                           images=get_all_images())


@app.route('/results', methods=['GET', 'POST'])
def results_page():
    if request.args.get('results'):
        return render_template('results.html',
                               results=get_images(request.args.get('results')),
                               page_name="results")
    if request.method == "POST":
        return render_template('results.html',
                               results=get_images(request.form.get('disease')),
                               page_name="results")
    return redirect('/')


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_page():
    if request.method == "POST":
        classification = request.form.get('disease')
        image_bytes = request.files.get('image').read()
        upload_db(image_bytes, classification)
        return redirect(f'/results?class={classification}')
    return render_template('upload.html',
                           page_name="upload",
                           options=get_classes())


@app.route('/classify', methods=['GET', 'POST'])
def classify_page():
    if request.method == "POST":
        # print(request.form) # ImmutableMultiDict([])
        image_bytes = request.files.get('image').read()
        predictions = classify_image(image_bytes)
        # print("Predictions: ", predictions)
        # return jsonify(predictions)
        return render_template('classify.html',
                               page_name="classify",
                               options=get_classes(),
                               predictions = predictions
                               )
    else:
        return render_template('classify.html',
                               page_name="classify",
                               options=get_classes())


@app.route('/get_images/<label>', methods=['GET'])
def get_image_t(label):
    print(get_images(label))
    return jsonify(get_images(label))


@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            email = form.email.data
            pwd = form.pwd.data
            username = form.username.data

            newuser = User(
                username=username,
                email=email,
                pwd=bcrypt.generate_password_hash(pwd),
            )

            db.session.add(newuser)
            db.session.commit()
            flash(f"Account Succesfully created", "success")
            return redirect(url_for("login"))

        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", "danger")
    return render_template("auth.html",
                           form=form,
                           page_name="register",
                           text="Create account",
                           title="Register",
                           btn_action="Register account")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


app.run(host='0.0.0.0', port=8080)
