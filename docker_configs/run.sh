#!/bin/bash

gunicorn -k gthread -c ./gunicorn_config.py 'road_to_nowhere.app:create_app()'
