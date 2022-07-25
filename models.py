import datetime
import jwt
from sqlalchemy import *
from sqlalchemy.sql import func
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_cors import CORS


application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URL
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(application)

# ORM wrapper to easen DB management
db = SQLAlchemy(application)

class Profile(db.Model):
    __tablename__ = "profiles"

    author_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    entries = db.relationship('JournalEntry', backref='profiles')

    def serialize(self):
        return {
            "author_id": self.author_id,
            "email": self.email,
            "username": self.username
        }

    def encode_token(self, author_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=15),
                'iat': datetime.datetime.utcnow(),
                'sub': author_id
            }
            return jwt.encode(
                payload,
                Config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e
    
    @staticmethod
    def decode_token(autho_token):
        try:
            payload = jwt.decode(autho_token, Config.SECRET_KEY, 'HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError as e:
           raise Exception(str(e))
        except jwt.InvalidTokenError as e:
            raise Exception(str(e))


class JournalEntry(db.Model):    
    __tablename__ = "entries"

    # Two user can post two similar entries but a user can't have duplicates
    __table_args__ = (
        db.UniqueConstraint('author_id', 'text'),
    )

    entry_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    author_id = db.Column(db.Integer, db.ForeignKey('profiles'))

    def serialize(self):
        return {
            "entry_id": self.entry_id,
            "text": self.text,
            "created_at": str(self.created_at),
            "author_id": self.author_id
        }