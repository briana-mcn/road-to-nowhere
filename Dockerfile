FROM python:3.8.5

ENV PROJECT_DIR /usr/local/src/app

RUN mkdir ${PROJECT_DIR}

WORKDIR ${PROJECT_DIR}

RUN pip install pipenv

COPY . ${PROJECT_DIR}

RUN pipenv install --system --deploy

EXPOSE 5000

CMD gunicorn -c ./gunicorn_config.py 'road_to_nowhere:app'
