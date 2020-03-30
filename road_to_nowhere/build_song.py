from road_to_nowhere import app
from road_to_nowhere.models import ArtistModel, SongModel
from road_to_nowhere import db


with app.app_context():
    try:
        print(ArtistModel.query.all())
        print(SongModel.query.all())
    except Exception:
        raise
    finally:
        db.session.close()
