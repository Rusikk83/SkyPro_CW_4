import hashlib

from flask import request
from flask_restx import Resource, Namespace, abort

from models import User, UserSchema
from setup_db import db

from views.auth import auth_required, auth_admin

user_ns = Namespace('user')

"""представление для получения и изменения профиля пользователя"""
@user_ns.route('/')
class UsersView(Resource):
    @auth_required  # получение профиля пользователя по email из токена
    def get(self, email):  # получаем email пользователя из декоратора
        u = db.session.query(User).filter(User.email == email).first()  # получаем данные  пользователя по email
        sm_d = UserSchema().dump(u)

        return sm_d, 200

    @auth_required  # изменение профиля пользователя по email из токена
    def patch(self, email):
        user = db.session.query(User).filter(User.email == email).first()  # получаем данные  пользователя по email
        req_json = request.json  # получаем данные из запроса
        # изменяем данные пользователя на новые из запроса
        if req_json.get("surname") is not None:
            user.email = req_json.get("surname")  # перепутано c email специально, т.к. это ошибка нп фронте
        if req_json.get("name") is not None:
            user.name = req_json.get("name")
        if req_json.get("email") is not None:
            user.surname = req_json.get("email")
        if req_json.get("favourite_genre") is not None:
            user.favorite_genre = req_json.get("favourite_genre")

        db.session.add(user)
        db.session.commit()
        return "", 201


"""представление для изменения пароля пользователя"""
@user_ns.route('/password/')
class UserChangePassword(Resource):
    @auth_required
    def put(self, email):  # получаем из декоратора email пользователя
        user = db.session.query(User).filter(User.email == email).first()  # получаем данные пользователя по email
        req_json = request.json  # получаем парметры из запроса
        old_password = req_json.get("old_password")
        new_password = req_json.get("new_password")
        if hashlib.md5(old_password.encode('utf-8')).hexdigest() != user.password:  # сравниваем хеши паролей
            abort(401)
        else:  # меняем хеш пароля на новый если старый пароль указан верно
            user.password = hashlib.md5(new_password.encode('utf-8')).hexdigest()
            db.session.add(user)
            db.session.commit()
            return "", 201


"""Представление для администрирования пользователей, доступно для роли администратора"""
@user_ns.route('/<int:uid>')
class UserView(Resource):
    @auth_admin
    def get(self, uid):
        u = db.session.query(User).get(uid)
        sm_d = UserSchema().dump(u)
        return sm_d, 200


    @auth_admin
    def delete(self, uid):
        user = db.session.query(User).get(uid)

        db.session.delete(user)
        db.session.commit()
        return "", 204