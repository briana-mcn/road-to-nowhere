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