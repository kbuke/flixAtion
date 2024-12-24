from flask import request, make_response, session, render_template

from flask_restful import Resource

from config import app, db, api, os

from werkzeug.utils import secure_filename

from flask import url_for, send_from_directory

from models import Accounts, ActorDirector, Media, TvShow, MediaCast, Genres, UserGenres, MediaGenres

from datetime import datetime

class AllUsers(Resource):
    def get(self):
        users = [user.to_dict(rules=(
            "-fave_genres",
            "-_password_hash",
        )) for user in Accounts.query.all()]
        return users, 200 
    
    def post(self):
        json = request.get_json()
        print("Received JSON:", json)  # Debugging
        try:
            # Check if the email is already registered
            if Accounts.query.filter_by(email=json.get("newUserEmail")).first():
                return {"error": "Email already registered"}, 400
        
            # Check if passwords match
            if json.get("newUserPassword") != json.get("confirmPassword"):
                return {"error": "Passwords do not match"}, 400
        
            # Create a new user
            new_user = Accounts(
                email=json.get("newUserEmail"),
                first_name=json.get("newUserFirstName"),
                surname=json.get("newUserSurname"),
                intro=json.get("newUserIntro"),
                account_type=json.get("newUserType")
            )
            new_user.password_hash = json.get("newUserPassword")
            db.session.add(new_user)
            db.session.commit()

            return new_user.to_dict(), 201
    
        except ValueError as e:
            return {"error": [str(e)]}, 400


class Login(Resource):
    def post(self):
        json=request.get_json()
        email=json.get("userEmail", "").strip()
        password=json.get("userPassword")

        if not email or not password:
            return {"error": "Email and Password required"}, 400
        
        user = Accounts.query.filter(Accounts.email==email).first()
        print(f"Wueried user: {user}")

        if user and user.authenticate(password):
            session["user_id"] = user.id 

            response=make_response(user.to_dict())
            response.status_code=200

            return response
        
        return {"error": "Invalid email or password"}, 401

class CheckSession(Resource):
    def get(self):
        user_id=session.get("user_id")
        if user_id:
            user = Accounts.query.filter(Accounts.id == user_id).first()
            if user:
                return user.to_dict(), 200
            return {"message": "Unauthorized user"}, 401

class AllActorsAndDirectors(Resource):
    def get(self):
        actors_directors = [actor_director.to_dict() for actor_director in ActorDirector.query.all()]
        return actors_directors, 200

class AllMedia(Resource):
    def get(self):
        films_shows = [film_show.to_dict() for film_show in Media.query.all()]
        return films_shows, 200
    
    def post(self):
        json=request.get_json()
        try:
            new_media = Media(
                title=json.get("newMediaTitle"),
                sub_title=json.get("newMediaSubTitle"),
                poster=json.get("newMediaPoster"),
                release_date=datetime.strptime(json.get("newMediaReleaseDate"), '%Y-%m-%d'),
                summary=json.get("newMediaSummary"),
                media_type=json.get("mediaType"),
                run_time_hours=json.get("mediaHour"),
                run_time_minutes=json.get("mediaMinute")
            )
            db.session.add(new_media)
            db.session.commit()
            return new_media.to_dict(), 201
        except ValueError as e:
            return {"error": [str(e)]}, 400

class AllShows(Resource):
    def get(self):
        shows = [show.to_dict() for show in TvShow.query.all()]
        return shows, 200

class AllMediaCasts(Resource):
    def get(self):
        casts = [cast.to_dict(rules=(
            "-media.film_cast",
        )) for cast in MediaCast.query.all()]
        return casts, 200

class AllGenre(Resource):
    def get(self):
        genres=[genre.to_dict() for genre in Genres.query.all()]
        return genres, 200

class AllFaveGenres(Resource):
    def get(self):
        fave_genres=[fave_genre.to_dict() for fave_genre in UserGenres.query.all()]
        return fave_genres, 200

class AllFilmGenres(Resource):
    def get(self):
        film_genres=[film_genre.to_dict() for film_genre in MediaGenres.query.all()]
        return film_genres, 200


api.add_resource(AllUsers, '/users')

api.add_resource(Login, '/login')
api.add_resource(CheckSession, '/check_session')

api.add_resource(AllActorsAndDirectors, '/actordirector')

api.add_resource(AllMedia, '/media')

api.add_resource(AllShows, '/shows')

api.add_resource(AllMediaCasts, '/casts')

api.add_resource(AllGenre, '/genres')

api.add_resource(AllFaveGenres, '/favegenres')

api.add_resource(AllFilmGenres, '/filmgenres')

if __name__ == "__main__":
    app.run(port=5555, debug=True)