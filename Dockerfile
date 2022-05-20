# Dockerfile to build and serve datagateway-api

FROM python:3.6-slim-bullseye

RUN python -m pip install --upgrade pip \
  && pip install poetry \
  && poetry run pip uninstall -y setuptools \
  && poetry run pip install 'setuptools<58.0.0'
