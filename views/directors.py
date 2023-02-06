from flask_restx import Resource, Namespace
from flask import request

from models import Director, DirectorSchema
from setup_db import db

from views.auth import auth_required, auth_admin

director_ns = Namespace('directors')


"""представление для получения списка всех режиссеров"""
@director_ns.route('/')
class DirectorsView(Resource):
    #@auth_required
    def get(self):
        page = request.args.get('page')
        if page is None:  # если НЕ задан параметр page
            rs = db.session.query(Director).all()
            res = DirectorSchema(many=True).dump(rs)
            return res, 200
        else:
            rs = db.session.query(Director).limit(12).offset((int(page)-1)*12)  # постраничный вывод данных
            res = DirectorSchema(many=True).dump(rs)
            return res, 200


"""представление для получения режиссера по ID """
@director_ns.route('/<int:rid>/')
class DirectorView(Resource):
    #@auth_required
    def get(self, rid):
        r = db.session.query(Director).get(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

