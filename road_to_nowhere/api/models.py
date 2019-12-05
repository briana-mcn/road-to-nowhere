from road_to_nowhere import db


# nullable set to False means 'not null' added to the DDL
class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    albums = db.relationship('Album', back_populates='artist')


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    artist = db.relationship('Artist', back_populates='albums')
    songs = db.relationship('Song', back_populates='album')


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    album = db.relationship('Album', back_populates='songs')

