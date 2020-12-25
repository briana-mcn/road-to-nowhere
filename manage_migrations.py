from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from road_to_nowhere.database import db
from road_to_nowhere import app


app = app.create_app()
manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
