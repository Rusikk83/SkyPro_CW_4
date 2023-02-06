from flask_restx import Resource, Namespace
from flask import request
from models import Genre, GenreSchema
from setup_db import db

from views.auth import auth_required, auth_admin

genre_ns = Namespace('genres')


"""представление для списка жанров жанры"""
@genre_ns.route('/')
class GenresView(Resource):
    #@auth_required
    def get(self):
        page = request.args.get("page")
        if page is None:  # если page не задан, получаем все жанры
            rs = db.session.query(Genre).all()
            res = GenreSchema(many=True).dump(rs)
            return res, 200

        else:  # если задан page то выводится заданная страница
            rs = db.session.query(Genre).limit(12).offset((int(page)-1)*12)
            res = GenreSchema(many=True).dump(rs)
            return res, 200


"""представление для получения жанра по id"""
@genre_ns.route('/<int:gid>/')
class GenreView(Resource):
    #@auth_required
    def get(self, gid):
        r = db.session.query(Genre).get(gid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

