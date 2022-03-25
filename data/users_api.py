import flask
from flask import Flask, render_template, make_response, request, redirect, abort, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import jsonify, request
import os
import sys
import requests
from werkzeug.utils import secure_filename

from . import db_session
from .users import User
from forms.user_login import RegisterForm, LoginForm

blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@blueprint.route('/api/register', methods=['POST', 'GET'])
def reg_users():
    form = RegisterForm()
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
        if form.year.data != 2 and form.year.data != 1:
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Enter the correct year of study")
        user = User(
            email=form.email.data,
            nickname=form.nickname.data,
            surname=form.surname.data,
            name=form.name.data,
            year=form.year.data,
            group=form.group.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        k = user.id
        return redirect('/api/ava/{}'.format(k))
    return render_template('register.html', title='Registration', form=form)


@blueprint.route('/api/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter((User.email == form.login.data) | (User.nickname == form.login.data)).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/main_chat")
        return render_template('login.html', message="Incorrect login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


@blueprint.route('/api/logout')
@login_required
def logout():
    logout_user()
    return redirect("/main_chat")


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_users(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_users(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'city_from', 'position', 'speciality', 'address', 'email']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(user_id)
    if not users:
        return jsonify({'error': 'Not found'})
    users.surname = request.json['surname']
    users.name = request.json['name']
    users.age = request.json['age']
    users.city_from = request.json['city_from']
    users.position = request.json['position']
    users.speciality = request.json['speciality']
    users.address = request.json['address']
    users.email = request.json['email']
    db_sess.commit()
    return jsonify({'success': 'OK'})
