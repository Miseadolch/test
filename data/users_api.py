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
