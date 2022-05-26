from flask import Flask, request
from flask_restx import Api, Resource
from models import db, Movie, Director, Genre, MovieSchema, DirectorSchema, GenreSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 3}
db.init_app(app)

api = Api(app)
movies_ns = api.namespace('movies')
genres_ns = api.namespace('genres')
directors_ns = api.namespace('directors')


@movies_ns.route('/')
class MoviesView(Resource):

    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')

        movies_query = Movie.query

        if director_id is not None:
            movies_query = movies_query.filter(Movie.director_id == director_id)

        if genre_id is not None:
            movies_query = movies_query.filter(Movie.genre_id == genre_id)

        movies = movies_query.all()

        return MovieSchema(many=True).dump(movies), 200

    def post(self):
        movie = MovieSchema().load(request.json)
        db.session.add(Movie(**movie))
        db.session.commit()
        db.session.close()
        return 'movie added successfully', 201


@movies_ns.route('/<uid>')
class MovieView(Resource):
    def get(self, uid):
        movie = db.session.query(Movie).filter(Movie.id == uid).first()

        if movie is None:
            return "movie not found", 404

        return MovieSchema().dump(movie), 200

    def put(self, uid):
        db.session.query(Movie).filter(Movie.id == uid).update(request.json)
        db.session.commit()
        db.session.close()
        return 'movie successfully modified', 204

    def delete(self, uid):
        delete_rows = db.session.query(Movie).filter(Movie.id == uid).delete()
        if delete_rows != 1:
            return f'not found id', 400
        db.session.commit()
        db.session.close()
        return 'movie deleted successfully', 200


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = db.session.query(Genre).all()
        return GenreSchema(many=True).dump(genres), 200

    def post(self):
        genre = GenreSchema().load(request.json)
        db.session.add(Genre(**genre))
        db.session.commit()
        db.session.close()
        return 'genre added successfully', 201


@genres_ns.route('/<uid>')
class GenreView(Resource):
    def get(self, uid):
        genre = db.session.query(Genre).filter(Genre.id == uid).first()

        if genre is None:
            return 'genre not found', 404

        return GenreSchema().dump(genre), 200

    def put(self, uid):
        db.session.query(Genre).filter(Genre.id == uid).update(request.json)
        db.session.commit()
        db.session.close()
        return 'genre successfully modified', 204

    def delete(self, uid):
        delete_rows = db.session.query(Genre).filter(Genre.id == uid).delete()
        if delete_rows != 1:
            return 'not found id', 400
        db.session.commit()
        db.session.close()
        return 'genre deleted successfully', 200


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = Director.query.all()
        return DirectorSchema(many=True).dump(directors)

    def post(self):
        director = DirectorSchema().load(request.json)
        db.session.add(Director(**director))
        db.session.commit()
        db.session.close()
        return 'director added successfully', 201

@directors_ns.route('/<uid>')
class DirectorView(Resource):
    def get(self, uid):
        director = db.session.query(Director).filter(Director.id == uid).first()

        if director is None:
            return 'director not found', 404

        return DirectorSchema().dump(director), 200

    def put(self, uid):
        db.session.query(Director).filter(Director.id == uid).update(request.json)
        db.session.commit()
        db.session.close()
        return 'director successfully modified', 204

    def delete(self, uid):
        delete_rows = db.session.query(Director).filter(Director.id == uid).delete()
        if delete_rows != 1:
            return 'not found id', 400
        db.session.commit()
        db.session.close()
        return 'director deleted successfully', 200

if __name__ == '__main__':
    app.run(debug=True)
