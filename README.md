# Road to Nowhere

## Run migrations

Currently executed in the local docker container when updating the models

```bash
docker exec -it road-to-nowhere-web bash
# after updating a table
# use manage_migrations.py script to upgrade the migration, creating a new migration
python manage_migrations.py db migrate -m "Relevant note describing the schema changes"
# double check the ugrade and downgrade changes in the new revision file created in `migrations/versions`
python manage_migrations.py db upgrade
```


Interact with database locally in python shell
```bash
docker exec -it road-to-nowhere-web bash
# create app
from road_to_nowhere.app import create_app
from road_to_nowhere.database import db
from road_to_nowhere.models import UserModel
app = create_app()
with app.app_context():
    users = db.session.query(UserModel).all()
    for user in users:
        print(user.username)
```
