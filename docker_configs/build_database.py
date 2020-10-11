from road_to_nowhere.database import db
from road_to_nowhere.models import ArtistModel, SongModel
from road_to_nowhere.app import create_app
import os

print('HERE')
print(os.getcwd())
print(os.listdir())

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        artist = ArtistModel(name='Talking Heads')
        song = SongModel(title='This Must Be the Place', artist=artist, lyrics='Home, is where I want to be')
        db.session.add(artist)
        db.session.add(song)
        db.session.commit()
