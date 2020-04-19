import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

from road_to_nowhere.database import db


class ArtistModel(db.Model):
    _tablename_ = 'artist_model'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    songs = db.relationship('SongModel', back_populates='artist')

    def __repr__(self):
        return f'<Artist: {self.name}>'


class SongModel(db.Model):
    _tablename_ = 'song_model'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    lyrics = db.Column(db.Text, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist_model.id'), nullable=False)
    artist = db.relationship('ArtistModel', back_populates='songs')

    def __repr__(self):
        return f'<Song: {self.title}, {self.artist}>'


class UserModel(db.Model):
    _tablename_ = 'user_model'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    salt = db.Column(db.String(256), nullable=False)
    api_token = db.Column(db.String, unique=True)

    def __init__(self, username=None, password=None, **kwargs):
        password_hash = None
        salt = None
        if username is not None and password is not None:
            salt = self.generate_salt()
            password_hash = self.generate_hash(password, salt)
        super(UserModel, self).__init__(username=username, password_hash=password_hash, salt=salt, **kwargs)

    @staticmethod
    def generate_hash(password, salt):
        backend = default_backend()
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2**14,
            r=8,
            p=1,
            backend=backend
        )
        return kdf.derive(password)

    @staticmethod
    def generate_salt():
        return os.urandom(16)

    def verify_hash(self, password):
        backend = default_backend()
        kdf = Scrypt(
            salt=self.salt,
            length=32,
            n=2 ** 14,
            r=8,
            p=1,
            backend=backend
        )
        kdf.verify(password, self.password_hash)

    # login manager required properties / functions
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
