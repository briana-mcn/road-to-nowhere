#!/bin/bash


gunicorn --reload --config=./gunicorn_config.py 'road_to_nowhere.app:create_app()'
