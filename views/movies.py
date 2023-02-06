from flask import request
from flask_restx import Resource, Namespace
from sqlalchemy import desc

from models import Movie, MovieSchema
from setup_db import db

from views.auth import auth_required, auth_admin

movie_ns = Namespace('movies')


"""представление для получения списков фильмов"""
@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        # получаем парметры status и page из запроса
        status = request.args.get("status")
        page = request.args.get("page")
        t = db.session.query(Movie)
        movies = None

        if status is not None:  # если статус  задан
            if status.lower() == 'new':  # если статус  имнно new
                if page is not None:  # если страница задана
                    movies = t.order_by(desc(Movie.year)).limit(12).offset((int(page)-1)*12)  # ели есть  статус и страница
                else:
                    movies = t.order_by(desc(Movie.year))  # если только статус

        elif page is not None:
            movies = t.limit(12).offset(page)  # если только страница
        else:
            movies = t.all()  # если нет ни статуса ни страницы
        res = MovieSchema(many=True).dump(movies)
        return res, 200


@movie_ns.route('/<int:id>/')
class MovieView(Resource):
    def get(self, id):
        b = db.session.query(Movie).get(id)
        sm_d = MovieSchema().dump(b)
        return sm_d, 200


