from road_to_nowhere.database import db


# nullable set to False means 'not null' added to the DDL
class ArtistModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    albums = db.relationship('Album', back_populates='artist')

    def __repr__(self):
        return f'<Artist {self.name}>'

class AlbumModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    artist = db.relationship('Artist', back_populates='albums')
    songs = db.relationship('Song', back_populates='album')

    def __repr__(self):
        return f'<Album {self.name, self.artist_id}>'

class SongModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    album = db.relationship('Album', back_populates='songs')
    lyrics = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Song {self.name}, {self.album_id}>'
