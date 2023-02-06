from flask import request
from flask_restx import Resource, Namespace

from models import User, UserSchema
from setup_db import db

from views.auth import auth_required, auth_admin

user_ns = Namespace('user')

"""представление для реализации методов CRUD для модели пользователь"""
@user_ns.route('/')
class UsersView(Resource):
    @auth_required
    def get(self, email):
        u = db.session.query(User).filter(User.email == email).first()
        sm_d = UserSchema().dump(u)

        return sm_d, 200

    @auth_required
    def patch(self, email):
        user = db.session.query(User).filter(User.email == email).first()
        req_json = request.json
        user.email = req_json.get("surname")  # перепутано специально, т.к. это ошибка нп фронте
        user.name = req_json.get("name")
        user.surname = req_json.get("email")
        user.favorite_genre = req_json.get("favourite_genre")


        db.session.add(user)
        db.session.commit()
        return "", 201


@user_ns.route('/<int:uid>')
class UserView(Resource):
    @auth_required
    def get(self, uid, email):
        u = db.session.query(User).get(uid)
        sm_d = UserSchema().dump(u)
        return sm_d, 200

    # @auth_admin
    def put(self, uid):
        user = db.session.query(User).get(uid)
        req_json = request.json
        user.username = req_json.get("username")
        user.password = req_json.get("password")
        user.role = req_json.get("role")

        user.password = user.get_hash()

        db.session.add(user)
        db.session.commit()
        return "", 201

    # @auth_admin
    def delete(self, uid):
        user = db.session.query(User).get(uid)

        db.session.delete(user)
        db.session.commit()
        return "", 204