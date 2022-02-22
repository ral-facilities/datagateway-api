# This is the Dockerfile for the datgateway_api container

FROM python:3.8

# install dependancies
RUN pip install poetry

WORKDIR /app

COPY . /app

RUN poetry run pip uninstall -y setuptools
RUN poetry run pip install 'setuptools<58.0.0'
RUN poetry install

# set the app running
#ENTRYPOINT ["tail", "-f", "/dev/null"]
ENTRYPOINT ["poetry","run","python3", "-m", "datagateway_api.src.main"]