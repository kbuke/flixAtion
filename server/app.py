from flask import request, make_response, session, render_template

from flask_restful import Resource

from config import app, db, api, os

from werkzeug.utils import secure_filename

from flask import url_for, send_from_directory

from models import Accounts, ActorDirector, Media, TvShow

from datetime import datetime

class AllUsers(Resource):
    def get(self):
        users = [user.to_dict() for user in Accounts.query.all()]
        return users, 200 
    
    def post(self):
        json=request.get_json()
        try:
            #Check if the email is already registered
            if Accounts.query.filter_by(email=json.get("newUserEmail")):
                return {"error": "Email already registered"}, 400
            
            new_user = Accounts(
                email=json.get("newUserEmail"),
                first_name=json.get("newUserFirstName"),
                surname=json.get("newUserSurname"),
                intro=json.get("newUserIntro"),
                account_type=json.get("newUserType")
            )
            new_user.password_hash=json.get("newUserPassword")
            db.session.add(new_user)
            db.session.commit()
            return new_user.to_dict(), 201
        except ValueError as e:
            return {"error": [str(e)]}, 400

class AllActorsAndDirectors(Resource):
    def get(self):
        actors_directors = [actor_director.to_dict() for actor_director in ActorDirector.query.all()]
        return actors_directors, 200

class AllMedia(Resource):
    def get(self):
        films_shows = [film_show.to_dict() for film_show in Media.query.all()]
        return films_shows, 200

class AllShows(Resource):
    def get(self):
        shows = [show.to_dict() for show in TvShow.query.all()]
        return shows, 200


api.add_resource(AllUsers, '/users')

api.add_resource(AllActorsAndDirectors, '/actordirector')

api.add_resource(AllMedia, '/media')

api.add_resource(AllShows, '/shows')

if __name__ == "__main__":
    app.run(port=5555, debug=True)