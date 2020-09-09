FROM python:3.8.5

ENV PROJECT_DIR /usr/local/src/app

RUN mkdir ${PROJECT_DIR}

WORKDIR ${PROJECT_DIR}

RUN pip install pipenv

COPY . ${PROJECT_DIR}

RUN pipenv install --system --deploy

EXPOSE 6000

CMD gunicorn -k gthread -c ./gunicorn_config.py 'road_to_nowhere.app:create_app()'
