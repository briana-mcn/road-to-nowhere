from road_to_nowhere.database import db


# nullable set to False means 'not null' added to the DDL
class ArtistModel(db.Model):
    _tablename_ = 'artist_model'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    songs = db.relationship('SongModel', back_populates='artist')

    def __repr__(self):
        return f'<Artist {self.name}>'


class SongModel(db.Model):
    _tablename_ = 'song_model'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    lyrics = db.Column(db.Text, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist_model.id'), nullable=False)
    artist = db.relationship('ArtistModel', back_populates='songs')

    def __repr__(self):
        return f'<Song {self.title}, {self.artist}>'
