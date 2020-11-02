# datagateway-api
ICAT API to interface with the Data Gateway

## Contents
- [datagateway-api](#datagateway-api)
  - [Contents](#contents)
  - [Creating Dev Environment and API Setup](#creating-dev-environment-and-api-setup)
  - [Running DataGateway API](#running-datagateway-api)
  - [Project structure](#project-structure)
      - [Main](#main)
      - [Endpoints](#endpoints)
      - [Mapped classes](#mapped-classes)
      - [Querying and filtering](#querying-and-filtering)
      - [Swagger Generation](#generating-the-swagger-spec-openapiyaml)
      - [Authentication](#authentication)
  - [Database Generator](#database-generator)
  - [Running Tests](#running-tests)


## Creating Dev Environment and API Setup
The recommended development environment for this API has taken lots of inspiration from
the [Hypermodern Python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/)
guide found online. It is assumed the commands shown in this part of the README are
executed in the root directory of this repo.

### pyenv (Python Version Management)
To start, install [pyenv](https://github.com/pyenv/pyenv). There is a Windows version of
this tool ([pyenv-win](https://github.com/pyenv-win/pyenv-win)), however this is
currently untested on this repoThis is used to manage the various versions of Python
that will be used to test/lint Python during development. Install by executing the following:

```bash
curl https://pyenv.run | bash
```

The following lines need to be added to `~/.bashrc` - either open a new terminal or
execute `source ~/.bashrc` to make these changes apply:

```bash
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Various Python build dependencies need to be installed next. These will vary dependent
on the platform of your system (see the
[common pyenv build problems](https://github.com/pyenv/pyenv/wiki/Common-build-problems)
for the relevant command for your OS), but the following shows the bash command to
install the requirements for a CentOS/RHEL machine:

```bash
sudo yum install @development zlib-devel bzip2 bzip2-devel readline-devel sqlite \
sqlite-devel openssl-devel xz xz-devel libffi-devel findutils
```

To make use of `pyenv`, let's install different versions of Python onto the system. In
production, DataGateway API uses Python 3.6, so this should definitely be part a
development environment for this repo. This stage might take some time as each Python
version needs to be downloaded and built individually:

```bash
pyenv install 3.6.8
pyenv install 3.7.7
pyenv install 3.8.2
```

To verify the installation commands worked:

```bash
python3.6 --version
python3.7 --version
python3.8 --version
```

These Python versions need to be made available to local version of the repository. They
will used during the Nox sessions, explained further down this file. Executing the
following command will create a `.python-version` file inside the repo (this file is
currently listed in `.gitignore`):

```bash
pyenv local 3.6.8 3.7.7 3.8.2
```

### Poetry (API Dependency Management)
To maintain records of the API's dependencies,
[Poetry](https://github.com/python-poetry/poetry) is used. To install, use the following
command:

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

The installation requires `~/.poetry/env` to be refreshed for changes to be applied.
Open a new terminal or execute the following command to ensure the installation is
completed smoothly:

```bash
source ~/.poetry/env
```

The dependencies for this repo are stored in `pyproject.toml`, with a more detailed
version of this data in `poetry.lock`. The lock file is used to maintain the exact
versions of dependencies from system to system. To install the dependencies, execute the
following command (add `--no-dev` if you don't want the dev dependencies):

```bash
poetry install
```

To add a dependency to Poetry, run the following command (add `--dev` if it's a
development related dependency). The
[official docs](https://python-poetry.org/docs/cli/#add) give good detail regarding the
intricacies of this command:

```bash
poetry add [PACKAGE-NAME]
```

### Nox (Automated Testing & Other Code Changes)
When developing new features for the API, there are a number of Nox sessions that can be
used to lint/format/test the code in the included `noxfile.py`. To install Nox, use Pip
as shown below. Nox is not listed as a Poetry dependency because this has the potential
to cause issues if Nox was executed inside Poetry (see
[here](https://medium.com/@cjolowicz/nox-is-a-part-of-your-global-developer-environment-like-poetry-pre-commit-pyenv-or-pipx-1cdeba9198bd)
for more detailed reasoning):

```bash
pip install --user --upgrade nox
```

To run the sessions defined in `nox.options.sessions` (see `noxfile.py`), simply run:

```bash
nox
```

To execute a specific nox session, the following will do that:

```bash
nox -s [SESSION/FUNCTION NAME]
```

Currently, the following Nox sessions have been created:
- `format` - this uses [Black](https://black.readthedocs.io/en/stable/) to format Python
  code to a pre-defined style.
- `lint` - this uses [flake8](https://flake8.pycqa.org/en/latest/) with a number of
  additional plugins (see the included `noxfile.py` to see which plugins are used) to
  lint the code to keep it Pythonic. `.flake8` configures `flake8` and the plugins.
- `safety` - this uses [safety](https://github.com/pyupio/safety) to check the
  dependencies (pulled directly from Poetry) for any known vulnerabilities. This session
  gives the output in a full ASCII style report.

### Pre Commit (Automated Checks during Git Commit)
To make use of Git's ability to run custom hooks, [pre-commit](https://pre-commit.com/)
is used. Like Nox, Pip is used to install this tool:

```
bash
pip install --user --upgrade pre-commit
```

This repo contains an existing config file for `pre-commit` (`.pre-commit-config.yaml`)
which needs to be installed using:

```bash
pre-commit install
```

When you commit work on this repo, the configured commit hooks will be executed, but
only on the changed files. This is good because it keeps the process of committing
a simple one, but to run the hooks on all the files locally, execute the following
command:

```bash
pre-commit run --all-files
```


## Running DataGateway API
Depending on the backend you want to use (either `db` or `python_icat`) the connection
URL for the backend needs to be set. These are set in `config.json` (an example file is
provided in the base directory of this repository). Copy `config.json.example` to
`config.json` and set the values as needed.

Ideally, the API would be run with:
`poetry run python -m src.main`
However it can be run with the flask run command as shown below:


**Warning: the host, port and debug config options will not be respected when the API is run this way**

To use `flask run`, the enviroment variable `FLASK_APP` should be set to `src/main.py`. Once this is
set the API can be run with `flask run` while inside the root directory of the project. The `flask run` command gets installed with flask.

Examples shown:
Unix
```bash
$ export FLASK_APP=src/main.py
$ flask run
```
CMD
```CMD
> set FLASK_APP=src/main.py
> flask run
```
PowerShell
```powershell
> $env:FLASK_APP = "src/main.py"
> flask run
```

More information can be found [here](http://flask.pocoo.org/docs/1.0/cli/).

By default the api will run on `http://localhost:5000` and all requests are made here
e.g. `http://localhost:5000/sessions`


## Project structure
The project consists of 3 main packages: common, src and test. common contains modules shared across test and src such as the database mapping classes.
src contains the api resources and their http method definitions, and test contains tests for each endpoint.

This is illustrated below.


`````
─── datagateway-api
    ├── common
    │   ├── database
    │   │   ├── backend.py
    │   │   ├── filters.py
    │   │   ├── helpers.py
    │   │   ├── models.py
    │   │   └── session_manager.py
    │   ├── icat
    │   ├── backends.py
    │   ├── constants.py
    │   ├── exceptions.py
    │   ├── filters.py
    │   └── helpers.py
    ├── src
    │   ├── resources
    │   │   ├── entities
    │   │   │   ├── entity_endpoint.py
    │   │   │   └── entity_map.py
    │   │   └── non_entities
    │   │       └── <non_entity>_endpoints.py
    │   ├── swagger
    │   │   ├── openapi.yaml
    │   │   └── swagger_generator.py
    │   └── main.py
    ├── test
    │   ├── resources
    │   │   ├── entities
    │   │   │   └──test_<entity>.py
    │   │   └── non_entities
    │   │       └── test_<non_entity>.py
    │   └── test_base
    │       ├── constants.py
    │       └── rest_test.py
    ├── util
    │   └── icat_db_generator.py
    ├── logs.log
    └── config.json
 `````
#### Main
`main.py` is where the flask_restful api is set up. This is where each endpoint resource class is generated and mapped
to an endpoint.

Example:
 `api.add_resource(get_endpoint(entity_name, endpoints[entity_name]), f"/{entity_name.lower()}")`


#### Endpoints
The logic for each endpoint are within `/src/resources`. They are split into entities, non_entities and
table_endpoints. The entities package contains `entities_map` which maps entity names to their sqlalchemy
model. The `entity_endpoint` module contains the function that is used to generate endpoints at start up.
`table_endpoints` contains the endpoint classes that are table specific. Finally, non_entities contains the
session endpoint.


#### Mapped classes
The classes mapped from the database are stored in `/common/database/models.py`. Each model was
automatically generated using sqlacodegen. A class `EntityHelper` is defined so that each model may
inherit two methods `to_dict()` and `update_from_dict(dictionary)`, both used for returning entities
and updating them, in a form easily converted to JSON.




## Database Generator
There is a tool to generate mock data into the database. It is located in `util/icat_db_generator.py`
By default it will generate 20 years worth of data (approx 70,000 entities). The script makes use of
`random` and `Faker` and is seeded with a seed of 1. The seed and number of years of data generated can
be changed by using the arg flags `-s` or `--seed` for the seed, and `-y` or `--years` for the number of years.
For example:
`python -m util.icat_db_generator -s 4 -y 10` Would set the seed to 4 and generate 10 years of data.


#### Querying and filtering:
The querying and filtering logic is located in `/common/database_helpers.py`. In this module the abstract `Query` and
`QueryFilter` classes are defined as well as their implementations. The functions that are used by various endpoints to
query the database are also in this module.
Class diagrams for this module:
![image](https://user-images.githubusercontent.com/44777678/67954353-ba69ef80-fbe8-11e9-81e3-0668cea3fa35.png)
![image](https://user-images.githubusercontent.com/44777678/67954834-7fb48700-fbe9-11e9-96f3-ffefc7277ebd.png)


#### Authentication
Each request requires a valid session ID to be provided in the Authorization header. This header should take the form of `{"Authorization":"Bearer <session_id>"}` A session ID can be obtained by
sending a post request to `/sessions/`
All endpoint methods that require a session id are decorated with `@requires_session_id`



#### Generating the swagger spec: `openapi.yaml`
The swagger generation script is located in `/src/swagger/swagger_generator.py`. The script will only run when
the config option `generate_swagger` is set to true in `config.json`. The generator decorates the first endpoint
resource class in it's module to get the name of the entity. It then creates the correct paths using the name of the
entity and outputs the swagger spec to `openapi.yaml`

Example of the decorator:
```python
@swagger_gen.resource_wrapper()
class DataCollectionDatasets(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        return get_rows_by_filter(DATACOLLECTIONDATASET, get_filters_from_query_string()), 200
```


## Running Tests
To run the tests use `python -m unittest discover`
