from flask import Flask, render_template, make_response, request, redirect, abort, jsonify
from data import db_session, users_api
from data.users import User
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from flask_restful import reqparse, abort, Api, Resource

from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/main_chat")
def index():
    return render_template("hat.html")


if __name__ == '__main__':
    db_session.global_init("db/students_chat.db")
    app.register_blueprint(users_api.blueprint)
    app.run(port=8080, host='127.0.0.1')
