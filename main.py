import os

from PIL import Image
import io

from flask import Flask, render_template, make_response, request, redirect, abort, jsonify
from data import db_session, users_api
from data.users import User
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from flask_restful import reqparse, abort, Api, Resource
from forms.user_login import RegisterForm, LoginForm
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/main_chat/<int:user_id>")
def main_chat(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter((User.id == user_id)).first()
    photo = Image.open(io.BytesIO(user.photo))
    photo.save('static/img/photo_for_ava_for_user{}.png'.format(user.id))
    return render_template("hat.html", photo=user.id)


@app.route('/register', methods=['POST', 'GET'])
def reg_users():
    db_sess = db_session.create_session()
    form = RegisterForm()
    user_first = db_sess.query(User).filter(User.id == 1).first()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Passwords don't match")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter((User.email == form.email.data) | (User.nickname == form.nickname.data)).first():
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="There is already such a user")
        user = User(
            email=form.email.data,
            nickname=form.nickname.data,
            surname=form.surname.data,
            name=form.name.data,
            group=form.group.data,
            photo=user_first.photo
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/load_ava/{}'.format(int(user.id)))
    return render_template('register.html', title='Registration', form=form)


@app.route('/load_ava/<int:user_id>', methods=['GET', 'POST'])
def load_ava(user_id):
    flag = 0
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter((User.id == user_id)).first()
    user_first = db_sess.query(User).filter(User.id == 1).first()
    if request.method == 'POST':
        photo = request.files['file']
        if photo.filename != '':
            photo.save('static/img/etot_parol_nikto_ne_uznaet{}.png'.format(user.id))
            user.photo = convert_to_binary_data('static/img/etot_parol_nikto_ne_uznaet{}.png'.format(user.id))
            db_sess.commit()
        else:
            photo = Image.open(io.BytesIO(user_first.photo))
            photo.save('static/img/etot_parol_nikto_ne_uznaet{}.png'.format(user.id))
            user.photo = convert_to_binary_data('static/img/etot_parol_nikto_ne_uznaet{}.png'.format(user.id))
            db_sess.commit()
        return redirect('/login')
    return render_template('load_ava.html', title='Avatar')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter((User.email == form.login.data) | (User.nickname == form.login.data)).first()
        if user.sing_in == 0:
            os.remove('static/img/etot_parol_nikto_ne_uznaet{}.png'.format(user.id))
        if user and user.check_password(form.password.data):
            user.sing_in = 1
            db_sess.commit()
            login_user(user, remember=form.remember_me.data)
            return redirect("/main_chat/{}".format(user.id))
        return render_template('login.html', message="Incorrect login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


if __name__ == '__main__':
    db_session.global_init("db/students_chat.db")
    app.run(port=8080, host='127.0.0.1')
