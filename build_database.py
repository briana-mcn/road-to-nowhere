from road_to_nowhere.database import db
from road_to_nowhere.models import ArtistModel, SongModel
from road_to_nowhere.app import create_app
import os

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()