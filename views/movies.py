from flask import request
from flask_restx import Resource, Namespace
from sqlalchemy import desc

from models import Movie, MovieSchema
from setup_db import db

from views.auth import auth_required, auth_admin

movie_ns = Namespace('movies')


"""представление для реализации методов CRUD для модели фильмы"""
@movie_ns.route('/')
class MoviesView(Resource):
    #@auth_required
    def get(self):
        status = request.args.get("status")
        page = request.args.get("page")
        year = request.args.get("year")
        t = db.session.query(Movie)
        movies = None

        if status is not None:
            if status.lower() == 'new':
                if page is not None:
                    movies = t.order_by(desc(Movie.year)).limit(12).offset(page)
                else:
                    movies = t.order_by(desc(Movie.year))
        elif page is not None:
            movies = t.limit(12).offset(page)
        else:
            movies = t.all()
        res = MovieSchema(many=True).dump(movies)
        return res, 200

    @auth_admin
    def post(self):
        req_json = request.json
        ent = Movie(**req_json)

        db.session.add(ent)
        db.session.commit()
        return "", 201, {"location": f"/movies/{ent.id}"}


@movie_ns.route('/<int:bid>')
class MovieView(Resource):
    #@auth_admin
    def get(self, bid):
        b = db.session.query(Movie).get(bid)
        sm_d = MovieSchema().dump(b)
        return sm_d, 200

    @auth_admin
    def put(self, bid):
        movie = db.session.query(Movie).get(bid)
        req_json = request.json
        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.director_id = req_json.get("director_id")
        db.session.add(movie)
        db.session.commit()
        return "", 204

    @auth_admin
    def delete(self, bid):
        movie = db.session.query(Movie).get(bid)

        db.session.delete(movie)
        db.session.commit()
        return "", 204
