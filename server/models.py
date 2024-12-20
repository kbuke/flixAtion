from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates 
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Time 
from config import db, bcrypt
import re 
from sqlalchemy.ext.hybrid import hybrid_property

#Table that will host all registered accounts
class Accounts(db.Model, SerializerMixin):
    __tablename__ = "accounts"

    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String, nullable=False)
    first_name=db.Column(db.String, nullable=False)
    surname=db.Column(db.String, nullable=False)
    intro=db.Column(db.String, nullable=True)
    _password_hash=db.Column(db.String, nullable=False)
    initial_sign_in=db.Column(db.Boolean, default=False)
    account_type=db.Column(db.String, nullable=False, default="User")

    #Password hashing and authentication
    @hybrid_property
    def password_hash(self):
        raise AttributeError("password: write only attribute")

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash=bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    #Validate email structure
    @validates("email")
    def validate_email(self, key, value):
        if '@' and '.' not in value:
            raise ValueError("Please enter a valid email address")
        return value

#Actor and Director table that will host actors and directors
class ActorDirector(db.Model, SerializerMixin):
    __tablename__ = "actors_directors"

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.Integer, nullable=False)
    dob=db.Column(db.DateTime, nullable=True)
    place_of_birth=db.Column(db.String, nullable=True)
    image=db.Column(db.String, nullable=True)
    intro=db.Column(db.String, nullable=False)
    actor_director=db.Column(db.String, nullable=False)

    #State what type of person this is
    ALLOWED_TYPES=("Director", "Actor")

    #Add Validations
    @validates("actor_director")
    def validate_actor_director(self, key, actor_director):
        if actor_director in self.ALLOWED_TYPES:
            return actor_director
        raise ValueError(f"This person must be one of {', '.join(self.ALLOWED_TYPES)}")

#Media table that will host films and tv shows
class Media(db.Model, SerializerMixin):
    __tablename__ = "media_types"

    id=db.Column(db.Integer, primary_key=True)

    title=db.Column(db.String, nullable=False)
    sub_title=db.Column(db.String, nullable=True)
    poster=db.Column(db.String)
    cover_photo=db.Column(db.String)
    release_date=db.Column(db.DateTime)
    summary=db.Column(db.String, nullable=False)
    media_type=db.Column(db.String, nullable=False)
    run_time_hours=db.Column(db.Integer)
    run_rime_minutes=db.Column(db.Integer)

    #Set up polymorphic relations
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'media'
    }

    #State what type of media can be registered
    ALLOWED_MEDIA=("Movie", "TV Show")

    #Add Validations
    @validates("media_type")
    def validate_media(self, key, media_type):
        if media_type in self.ALLOWED_MEDIA:
            return media_type 
        raise ValueError(f"This media must be one of {', '.join(self.ALLOWED_MEDIA)}")

#Set up model for films
class TvShow(Media):
    __tablename__ = "tv_shows"

    @declared_attr
    def id(cls):
        return db.Column(db.Integer, db.ForeignKey('media_types.id'), primary_key=True)
    
    end_date=db.Column(db.DateTime, nullable=True)

    #Set up validations
    @validates("end_date")
    def validate_end_date(self, key, end_date):
        if self.release_date and self.release_date <= end_date:
            return end_date
        raise ValueError("End date can not be before premiere date")

    #Set up polymorphic relations
    __mapper_args__={
        "polymorphic_identity": "tv_show"
    }
