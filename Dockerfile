# Dockerfile to build and serve datagateway-api

FROM python:3.6-slim-bullseye

WORKDIR /datagateway-api

COPY poetry.lock pyproject.toml ./

RUN python -m pip install --upgrade pip \
  && pip install poetry \
  && poetry run pip uninstall -y setuptools \
  && poetry run pip install 'setuptools<58.0.0' \
  && poetry run pip install 'gunicorn==20.1.0' \
  && poetry install --no-dev

COPY datagateway_api ./datagateway_api

# Serve the application using gunicorn - production ready WSGI server
ENTRYPOINT ["poetry", "run", "gunicorn", "-c", "gunicorn.conf.py", "datagateway_api.wsgi:application"]
