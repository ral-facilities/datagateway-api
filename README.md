[![Build Status](https://github.com/ral-facilities/datagateway-api/workflows/CI/badge.svg?branch=main)](https://github.com/ral-facilities/datagateway-api/actions?query=workflow%3A%22CI%22)
[![Codecov](https://codecov.io/gh/ral-facilities/datagateway-api/branch/main/graph/badge.svg)](https://codecov.io/gh/ral-facilities/datagateway-api)



# DataGateway API
This is a Flask-based API that fetches data from an ICAT instance, to interface with
[DataGateway](https://github.com/ral-facilities/datagateway). This API uses two ways
for data collection/manipulation, using a Python-based ICAT API wrapper or using
sqlalchemy to communicate directly with ICAT's database.




# Contents
- [Creating Dev Environment and API Setup](#creating-dev-environment-and-api-setup)
  - [Python Version Management (pyenv)](#python-version-management-(pyenv))
  - [API Dependency Management (Poetry)](#api-dependency-management-(poetry))
  - [Automated Testing & Other Development Helpers (Nox)](#automated-testing-&-other-development-helpers-(nox))
  - [Automated Checks during Git Commit (Pre Commit)](#automated-checks-during-git-commit-(pre-commit))
  - [Summary](#summary)
- [Running DataGateway API](#running-datagateway-api)
  - [API Startup](#api-startup)
  - [Authentication](#authentication)
  - [Swagger Interface](#swagger-interface)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)
  - [Main](#main)
  - [Endpoints](#endpoints)
  - [Logging](#logging)
  - [Date Handler](#date-handler)
  - [Exceptions & Flask Error Handling](#exceptions-&-flask-error-handling)
  - [Filtering](#filtering)
  - [Backends](#backends)
    - [Abstract Backend Class](#abstract-backend-class)
    - [Creating a Backend](#creating-a-backend)
  - [Database Backend](#database-backend)
    - [Mapped Classes](#mapped-classes)
  - [Python ICAT Backend](#python-icat-backend)
    - [Client Handling](#client-handling)
    - [ICATQuery](#icatquery)
  - [Generating the OpenAPI Specification](#generating-the-openapi-specification)
- [Utilities](#utilities)
  - [Database Generator](#database-generator)
  - [Postman Collection](#postman-collection)
- [Updating README](#updating-readme)




# Creating Dev Environment and API Setup
The recommended development environment for this API has taken lots of inspiration from
the [Hypermodern Python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/)
guide found online. It is assumed the commands shown in this part of the README are
executed in the root directory of this repo once it has been cloned to your local
machine.


## Python Version Management (pyenv)
To start, install [pyenv](https://github.com/pyenv/pyenv). There is a Windows version of
this tool ([pyenv-win](https://github.com/pyenv-win/pyenv-win)), however this is
currently untested on this repo. This is used to manage the various versions of Python
that will be used to test/lint Python during development. Install by executing the
following:

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
pyenv install 3.9.0
```

To verify the installation commands worked:

```bash
python3.6 --version
python3.7 --version
python3.8 --version
python3.9 --version
```

These Python versions need to be made available to local version of the repository. They
will used during the Nox sessions, explained further down this file. Executing the
following command will create a `.python-version` file inside the repo (this file is
currently listed in `.gitignore`):

```bash
pyenv local 3.6.8 3.7.7 3.8.2 3.9.0
```


## API Dependency Management (Poetry)
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


## Automated Testing & Other Development Helpers (Nox)
When developing new features for the API, there are a number of Nox sessions that can be
used to lint/format/test the code in the included `noxfile.py`. To install Nox, use Pip
as shown below. Nox is not listed as a Poetry dependency because this has the potential
to cause issues if Nox was executed inside Poetry (see
[here](https://medium.com/@cjolowicz/nox-is-a-part-of-your-global-developer-environment-like-poetry-pre-commit-pyenv-or-pipx-1cdeba9198bd)
for more detailed reasoning). When using the `--user` option, ensure your user's Python
installation is added to the system `PATH` variable, remembering to reboot your system
if you need to change the `PATH`. If you do choose to install these packages within a
virtual environment, you do not need the `--user` option:

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
- `black` - this uses [Black](https://black.readthedocs.io/en/stable/) to format Python
  code to a pre-defined style.
- `lint` - this uses [flake8](https://flake8.pycqa.org/en/latest/) with a number of
  additional plugins (see the included `noxfile.py` to see which plugins are used) to
  lint the code to keep it Pythonic. `.flake8` configures `flake8` and the plugins.
- `safety` - this uses [safety](https://github.com/pyupio/safety) to check the
  dependencies (pulled directly from Poetry) for any known vulnerabilities. This session
  gives the output in a full ASCII style report.
- `tests` - this uses [pytest](https://docs.pytest.org/en/stable/) to execute the
  automated tests in `test/`, tests for the database and ICAT backends, and non-backend
  specific tests. More details about the tests themselves [here](#running-tests).

Each Nox session builds an environment using the repo's dependencies (defined using
Poetry) using `install_with_constraints()`. This stores the dependencies in a
`requirements.txt`-like format temporarily during this process, using the OS' default
temporary location. These files are manually deleted in `noxfile.py` (as opposed to
being automatically removed by Python) to minimise any potential permission-related
issues as documented
[here](https://github.com/bravoserver/bravo/issues/111#issuecomment-826990).


## Automated Checks during Git Commit (Pre Commit)
To make use of Git's ability to run custom hooks, [pre-commit](https://pre-commit.com/)
is used. Like Nox, Pip is used to install this tool:

```bash
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


## Summary
As a summary, these are the steps needed to create a dev environment for this repo
compressed into a single code block:

```bash
# Install pyenv
curl https://pyenv.run | bash

# Paste into ~/.bashrc
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Apply changes made in ~/.bashrc
source ~/.bashrc

# Install Python build tools
sudo yum install @development zlib-devel bzip2 bzip2-devel readline-devel sqlite \
sqlite-devel openssl-devel xz xz-devel libffi-devel findutils

# Install different versions of Python and verify they work
pyenv install 3.6.8
python3.6 --version
pyenv install 3.7.7
python3.7 --version
pyenv install 3.8.2
python3.8 --version

# Make installed Python versions available to repo
pyenv local 3.6.8 3.7.7 3.8.2

# Install Poetry
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# Apply changes made to file when installing Poetry
source ~/.poetry/env

# Install API's dependencies
poetry install

# Install Nox
pip install --user --upgrade nox

# Install Pre Commit
pip install --user --upgrade pre-commit

# Install commit hooks
pre-commit install
```




# Running DataGateway API
Depending on the backend you want to use (either `db` or `python_icat`, more details
about backends [here](#backends)) the connection URL for the backend needs to be set.
These are set in `config.json` (an example file is provided in the base directory of
this repository). While both `db_url` and `icat_url` should have values assigned to them
(for best practice), `db_url` will only be used for the database backend, and `icat_url`
 will only be used for the Python ICAT backend. Copy `config.json.example` to
`config.json` and set the values as needed. If you need to create an instance of ICAT,
there are a number of markdown-formatted tutorials that can be found on the
[icat.manual](https://github.com/icatproject/icat.manual/tree/master/tutorials)
repository.

By default, the API will run on `http://localhost:5000` and all requests are made here
e.g. `http://localhost:5000/sessions`.


## API Startup
Ideally, the API would be run using the following command, the alternative (detailed
below) should only be used for development purposes.

```bash
poetry run python -m datagateway_api.src.main
```

However, it can also be run with the `flask run` command (installed with Flask). To use
`flask run`, the enviroment variable `FLASK_APP` should be set to
`datagateway_api/src/main.py`. Once this is set, the API can be run with `flask run`
while inside the root directory of the project. This shouldn't be used in production, as
detailed in Flask's documentation, this method of running the API is only
["provided for convenience"](https://flask.palletsprojects.com/en/1.1.x/cli/#run-the-development-server).

**WARNING: the host, port and debug config options will not be respected when the API is
run this way**

Examples:

Unix:
```bash
$ export FLASK_APP=datagateway_api/src/main.py
$ flask run
```

CMD:
```CMD
> set FLASK_APP=datagateway_api/src/main.py
> flask run
```

PowerShell:
```powershell
> $env:FLASK_APP = "datagateway_api/src/main.py"
> flask run
```

The Flask app can be configured so that code changes are monitored and the server will
reload itself when a change is detected. This setting can be toggled using
`flask_reloader` in `config.json`. This is useful for development purposes. It should be
noted that when this setting is enabled, the API will go through the startup process
twice. In the case of the ICAT backend, this could dramatically increase startup time if
the API is configured with a large initial client pool size.


## Authentication
Each request requires a valid session ID to be provided in the Authorization header.
This header should take the form of `{"Authorization":"Bearer <session_id>"}` A session
ID can be obtained by sending a POST request to `/sessions`. All endpoint methods that
require a session id are decorated with `@requires_session_id`.


## Swagger Interface
If you go to the API's base path in your browser (`http://localhost:5000` by default), a
representation of the API will be shown using
[Swagger UI](https://swagger.io/tools/swagger-ui/). This uses an OpenAPI specfication to
visualise and allow users to easily interact with the API without building their own
requests. It's great for gaining an understanding in what endpoints are available and
what inputs the requests can receive, all from an interactive interface.

This specification is built with the Database Backend in mind (attribute names on
example outputs are capitalised for example), however the Swagger interface can also be
used with the Python ICAT Backend. More details on how the API's OpenAPI specification
is built can be found [here](#generating-the-openapi-specification).




# Running Tests
To run the tests use `nox -s tests`. The repository contains a variety of tests, to test
the functionality of the API works as intended. The tests are split into 3 main
sections: non-backend specific (testing features such as the date handler), ICAT backend
tests (containing tests for backend specific components, including tests for the
different types of endpoints) and Database Backend tests (like the ICAT backend tests,
but covering only the most used aspects of the API).

The configuration file (`config.json`) contains two options that will be used during the
testing of the API. Set `test_user_credentials` and `test_mechanism` appropriately for
your test environment, using `config.json.example` as a reference. The tests require a
connection to an instance of ICAT, so set the rest of the config as needed.

By default, this will execute the repo's tests in
Python 3.6, 3.7 and 3.8. For most cases, running the tests in a single Python version
will be sufficient:

```bash
nox -p 3.6 -s tests
```

This repository also utilises [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/)
to check how much of the codebase is covered by the tests in `test/`:

```bash
nox -p 3.6 -s tests -- --cov-report term --cov=./datagateway_api
```

With `pytest`, you can output the duration for each test, useful for showing the slower
tests in the collection (sortest from slowest to fastest). The test duration is split
into setup, call and teardown to more easily understand where the tests are being slowed
down:

```bash
nox -p 3.6 -s tests -- --durations=0
```

To test a specific test class (or even a specific test function), use a double colon to
denote a each level down beyond the filename:

```bash
# Test a specific file
nox -p 3.6 -s tests -- test/icat/test_query.py

# Test a specific test class
nox -p 3.6 -s tests -- test/icat/test_query.py::TestICATQuery

# Test a specific test function
nox -p 3.6 -s tests -- test/icat/test_query.py::TestICATQuery::test_valid_query_exeuction
```




# Project Structure
The project consists of 3 main packages: `datagateway_api.common`,
`datagateway_api.src`, and `test`. `datagateway_api.common` contains modules for the
Database and Python ICAT Backends as well as code to deal with query filters.
`datagateway_api.src` contains the API resources and their HTTP method definitions (e.g.
GET, POST). `test` contains automated tests written using Pytest. A directory tree is
illustrated below:

`````
.
├── .flake8
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE
├── README.md
├── datagateway_api
│   ├── config.json.example
│   ├── wsgi.py
│   ├── common
│   │   ├── backend.py
│   │   ├── backends.py
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── database
│   │   │   ├── backend.py
│   │   │   ├── filters.py
│   │   │   ├── helpers.py
│   │   │   ├── models.py
│   │   │   └── session_manager.py
│   │   ├── date_handler.py
│   │   ├── exceptions.py
│   │   ├── filter_order_handler.py
│   │   ├── filters.py
│   │   ├── helpers.py
│   │   ├── icat
│   │   │   ├── backend.py
│   │   │   ├── filters.py
│   │   │   ├── helpers.py
│   │   │   └── query.py
│   │   ├── logger_setup.py
│   │   └── query_filter_factory.py
│   └── src
│       ├── main.py
│       ├── resources
│       │   ├── entities
│       │   │   ├── entity_endpoint.py
│       │   │   └── entity_map.py
│       │   ├── non_entities
│       │   │   └── sessions_endpoints.py
│       │   └── table_endpoints
│       │       └── table_endpoints.py
│       └── swagger
│           ├── apispec_flask_restful.py
│           ├── initialise_spec.py
│           └── openapi.yaml
├── noxfile.py
├── poetry.lock
├── postman_collection_icat.json
├── pyproject.toml
├── test
│   ├── conftest.py
│   ├── db
│   │   ├── conftest.py
│   │   ├── endpoints
│   │   │   ├── test_count_with_filters_db.py
│   │   │   ├── test_findone_db.py
│   │   │   ├── test_get_by_id_db.py
│   │   │   ├── test_get_with_filters.py
│   │   │   └── test_table_endpoints_db.py
│   │   ├── test_entity_helper.py
│   │   ├── test_query_filter_factory.py
│   │   └── test_requires_session_id.py
│   ├── icat
│   │   ├── conftest.py
│   │   ├── endpoints
│   │   │   ├── test_count_with_filters_icat.py
│   │   │   ├── test_create_icat.py
│   │   │   ├── test_delete_by_id_icat.py
│   │   │   ├── test_findone_icat.py
│   │   │   ├── test_get_by_id_icat.py
│   │   │   ├── test_get_with_filters_icat.py
│   │   │   ├── test_table_endpoints_icat.py
│   │   │   ├── test_update_by_id_icat.py
│   │   │   └── test_update_multiple_icat.py
│   │   ├── filters
│   │   │   ├── test_distinct_filter.py
│   │   │   ├── test_include_filter.py
│   │   │   ├── test_limit_filter.py
│   │   │   ├── test_order_filter.py
│   │   │   ├── test_skip_filter.py
│   │   │   └── test_where_filter.py
│   │   ├── test_filter_order_handler.py
│   │   ├── test_query.py
│   │   └── test_session_handling.py
│   ├── test_backends.py
│   ├── test_base.py
│   ├── test_config.py
│   ├── test_date_handler.py
│   ├── test_endpoint_rules.py
│   ├── test_get_filters_from_query.py
│   ├── test_get_session_id_from_auth_header.py
│   ├── test_is_valid_json.py
│   └── test_queries_records.py
└── util
    └── icat_db_generator.py
`````


## Main
`main.py` is where the flask_restful API is set up. This is where each endpoint resource
class is generated and mapped to an endpoint.

Example:
```python
api.add_resource(get_endpoint_resource, f"/{entity_name.lower()}")
```


## Endpoints
The logic for each endpoint is within `/src/resources`. They are split into entities,
non_entities and table_endpoints.

The entities package contains `entity_map` which
maps entity names to their field name used in backend-specific code. The Database
Backend uses this for its mapped classes (explained below) and the Python ICAT Backend
uses this for interacting with ICAT objects within Python ICAT. In most instances, the
dictionary found in `entity_map.py` is simply mapping the plural entity name (used to
build the entity endpoints) to the singular version. The `entity_endpoint` module
contains the function that is used to generate endpoints at start up. `table_endpoints`
contains the endpoint classes that are table specific (currently these are the ISIS
specific endpoints required for their use cases). Finally, `non_entities` contains the
session endpoint for session handling.


## Logging
Logging configuration can be found in `datagateway_api.common.logger_setup.py`. This
contains a typical dictionary-based config for the standard Python `logging` library
that rotates files after they become 5MB in size.

The default logging location is in the root directory of this repo. This location (and
filename) can be changed by editing the `log_location` value in `config.json`. The log
level (set to `WARN` by default) can also be changed using the appropriate value in that
file.


## Date Handler
This is a class containing static methods to deal with dates within the API. The date
handler can be used to convert dates between string and datetime objects (using a format
agreed in `datagateway_api.common.constants`) and uses a parser from `dateutil` to
detect if an input contains a date. This is useful for determining if a JSON value given
in a request body is a date, at which point it can be converted to a datetime object,
ready for storing in ICAT. The handler is currently only used in the Python ICAT
Backend, however this is non-backend specific class.


## Exceptions & Flask Error Handling
Exceptions custom to DataGateway API are defined in `datagateway_api.common.exceptions`.
Each exception has a status code and a default message (which can be changed when
raising the exception in code). None of them are backend specific, however some are only
used in a single backend because their meaning becomes irrelevant anywhere else.

When the API is setup in `main.py`, a custom API object is created (inheriting
flask_restful's `Api` object) so `handle_error()` can be overridden. A previous
iteration of the API registered a error handler with the `Api` object, however this
meant DataGateway API's custom error handling only worked as intended in debug mode (as
detailed in a
[GitHub issue](https://github.com/ral-facilities/datagateway-api/issues/147)). This
solution prevents any exception returning a 500 status code (no matter the defined
status code in `exceptions.py`) in production mode. This is explained in a
[Stack Overflow answer](https://stackoverflow.com/a/43534068).


## Filtering
Filters available for use in the API are defined in `datagateway_api.common.filters`.
These filters are all based from `QueryFilter`, an asbtract class to define any filter
for the API. Precedence is used to prioritise in which order filters should be applied,
but is only needed for the Database Backend.

Filtering logic is located in `datagateway_api.common.helpers`.
`get_filters_from_query_string()` uses the request query parameters to form filters to
be used within the API. A `QueryFilterFactory` is used to build filters for the correct
backend and the static method within this class is called in
`get_filters_from_query_string()`.


## Backends
As described at the top of this file, there are currently two ways that the API
creates/fetches/updates/deletes data from ICAT. The intention is each backend allows a
different method to communicate with ICAT, but results in a very similarly behaving
DataGateway API.


### Abstract Backend Class
The abstract class can be found in `datagateway_api.common.backend` and contains all the
abstract methods that should be found in a class which implements `Backend`. The typical
architecture across both backends is that the implemented functions call a helper
function to process the request and the result of that is returned to the user.

Each backend module contains the following files which offer similar functionality,
implemented in their own ways:
- `backend.py` - Implemented version of `datagateway_api.common.backend`
- `filters.py` - Inherited versions of each filter defined in
  `datagateway_api.common.filters`
- `helpers.py` - Helper functions that are called in `backend.py`


### Creating a Backend
A function inside `datagateway_api.common.backends` creates an instance of a backend
using input to that function to decide which backend to create. This function is called
in `main.py` which uses the backend type set in `config.json`, or a config value in the
Flask app if it's set (this config option is only used in the tests however). The
backend object is then parsed into the endpoint classes so the correct backend can be
used.


## Database Backend
The Database Backend uses [SQLAlchemy](https://www.sqlalchemy.org/) to interface
directly with the database for an instance of ICAT. This backend favours speed over
thoroughness, allowing no control over which users can access a particular piece of
data.


### Mapped Classes
The classes mapped from the database (as described [above](#endpoints)) are stored in
`/common/database/models.py`. Each model was automatically generated using sqlacodegen.
A class `EntityHelper` is defined so that each model may inherit two methods `to_dict()`
and `update_from_dict(dictionary)`, both used for returning entities and updating them,
in a form easily converted to JSON.


## Python ICAT Backend
Sometimes referred to as the ICAT Backend, this uses
[python-icat](https://python-icat.readthedocs.io/en/stable/) to interact with ICAT data.
The Python-based API wrapper allows ICAT Server to be accessed using the SOAP interface.
Python ICAT allows control over which users can access a particular piece of data, with
the API supporting multiple authentication mechanisms. Meta attributes such as `modId`
are dealt by Python ICAT, rather than the API.


### Client Handling
Python ICAT uses
[client objects](https://python-icat.readthedocs.io/en/stable/client.html) to
authenticate users and provide interaction to ICAT (e.g. querying icatdb). A client
object has a high creation cost (often taking several seconds), so it's unsuitable to
create a new client object at the start of each request. In a similar vein, it would
also be unsuitable to use a single client object for the entire API due to collisions
between different users.

Client objects are handled using an
[LRU cache](https://docs.python.org/3/library/functools.html#functools.lru_cache),
fetching clients from an [object pool](https://object-pool.readthedocs.io/en/latest/)
when a new client is requested for the cache.

#### Caching
The cache is extended from Cachetools' implementation (although the documentation for
the builtin LRU cache is more detailed, hence that's linked above) to allow for a client
object to be placed back into the object pool once it becomes 'least recently used' and
therefore is removed from the cache (in place of another item). Each cache item is
differentiated by the arguments of the function it's applied to which in this case is
the session ID. The client pool object is also passed into the function, but this is a
singleton object (mandated by the library it's implemented from) so this won't change
throughout the lifetime of the API.

#### Pooling
The object pool has an initial pool size that will be created at startup, and a maximum
size that the pool can grow to if needed, where both values are configurable. The
clients within the pool do not expire and have unlimited reuses, so clients created at
startup can be used for the lifespan of the API. Python ICAT's `Client` class is
extended (to `ICATClient`) to rename `cleanup()` to a function name that the object pool
will recognise to clean up resources and will disable the auto logout feature to prevent
sessions from being logged out when the client is reused.

#### Attributes of the Design
Combining caching and pooling into one design gives the following high-level results.
There is a 1 client to 1 session ID ratio, which will prevent collision between users
and doesn't require an excessive amount of resources (such as a 1 client to 1 request
ratio would). Since the object pool is created at startup, this design can cause the API
to be slow to start as the pool of object needs to be created. A rough guide would be to
multiply the configured initial pool size by around 5 or 6 seconds to get a time
estimate for pool creation.

#### Configuring Client Handling
When configuring the cache size and the client pool, the following should be considered.
The pool's max size should be configured to the maximum number of concurrent users
expected for the API. The cache size must not exceed the pool's maximum size. If
this does happen, the cache could attempt to acquire a client from an empty pool that
cannot grow, causing the request to never respond because the API will wait
indefinitely. The pool's initial size should be configured to strike a balance of
reasonable startup time and not slowing down requests when the pool grows beyond its
initial size. NOTE: when the pool exceeds the initial size and a client is requested by
the cache, a client is created on the fly, so that request (and any others sent before
the client is created and in the cache) WILL be slow. For development, the following
settings (as also set in the example config) would allow for an acceptable startup time
but allow for multiple session IDs to be used if required.

```json
"client_cache_size": 5,
"client_pool_init_size": 2,
"client_pool_max_size": 5,
```


### ICATQuery
The ICATQuery classed is in `datagateway_api.common.icat.query`. This class stores a
query created with Python ICAT
([documentation](https://python-icat.readthedocs.io/en/stable/query.html)). The
`execute_query()` function executes the query and returns either results in either a
JSON format, or a list of
[Python ICAT entity's](https://python-icat.readthedocs.io/en/stable/entity.html) (this
is defined using the `return_json_formattable` flag). Other functions within that class
are used within `execute_query()`.


## Generating the OpenAPI Specification
When the config option `generate_swagger` is set to true in `config.json`, a YAML
file defining the API using OpenAPI standards will be created at
`src/swagger/openapi.yaml`. This option should be disabled in production to avoid any
issues with read-only directories.

[apispec](https://apispec.readthedocs.io/en/latest/) is used to help with this, with an
`APISpec()` object created in `src/main.py` which endpoint specifications are added to
(using `APISpec.path()`) when the endpoints are created for Flask. These paths are
iterated over and ordered alphabetically, to ensure `openapi.yaml` only changes if there
have been changes to the Swagger docs of the API; without that code, Git will detect
changes on that file everytime startup occurs (preventing a clean development repo). The
contents of the `APISpec` object are written to a YAML file and is used when the user
goes to the configured (root) page in their browser.

The endpoint related files in `src/resources/` contain `__doc__` which have the Swagger
docs for each type of endpoint. For non-entity and table endpoints, the Swagger docs are
contained in the docstrings. `src/resources/swagger/` contain code to aid Swagger doc
generation, with a plugin (`RestfulPlugin`) created for `apispec` to extract Swagger
documentation from `flask-restful` functions.




# Utilities
Within the repository, there are some useful files which can help with using the API.


## Database Generator
There is a tool to generate mock data into ICAT's database. It is located in
`util/icat_db_generator.py`. By default it will generate 20 years worth of data (approx
70,000 entities). The default arguments will match the data on SciGateway Preprod and
therefore this is usually a good starting point. The script makes use of `random` and
`Faker` and is seeded with a seed of 1. The seed and number of years of data generated
can be changed by using the arg flags `-s` or `--seed` for the seed, and `-y` or
`--years` for the number of years. For example:
`python -m util.icat_db_generator -s 4 -y 10` Would set the seed to 4 and generate 10
years of data.

This uses code from the API's Database Backend, so a suitable `db_url` should be
configured in `config.json`.

When used on a machine that doesn't use UTC timezone, you may find there are a mix of timezones when querying the API. This issue was found on SciGateway Preprod when using BST
and there would be a mix of +00:00 and +01:00 timezones
([more details with screenshots](https://github.com/ral-facilities/datagateway/issues/782)).
The current suggested workaround is to change your machine to use UTC. In the case of
SciGateway preprod, the JVM timezone was changed to UTC (in
`/home/glassfish/[PAYARA_VERSION]/glassfish/domains/domain1/config/domain.xml`). This
was done to ensure the VM's system timezone wasn't changed back to BST by the automated
systems that maintain it.


## Postman Collection
With a handful of endpoints associated with each entity, there are hundreds of endpoints
for this API. A Postman collection is stored in the root directory of this repository,
containing over 300 requests, with each type of endpoint for every entity as well as the
table and session endpoints. The exported collection is in v2.1 format and is currently
the recommended export version for Postman.

This collection is mainly based around the Python ICAT Backend (request bodies for
creating and updating data uses camelCase attribute names as accepted by that backend)
but can easily be adapted for using the Database Backend if needed (changing attribute
names to uppercase for example). The collection also contains a login request specially
for the Database Backend, as logging in using that backend is slightly different to
logging in via the Python ICAT Backend.

The repo's collection can be easily imported into your Postman installation by opening
Postman and selecting File > Import... and choosing the Postman collection from your
cloned DataGateway API repository.




# Updating README
Like the codebase, this README file follows a 88 character per line formatting approach.
This isn't always possible with URLs and codeblocks, but the vast majority of the file
should follow this approach. Most IDEs can be configured to include a guideline to show
where this point is. To do this in VS Code, insert the following line into
`settings.json`:

```json
"editor.rulers": [
  88
]
```

Before a heading with a single hash, a four line gap should be given to easily indicate
separation between two sections. Before every other heading (i.e. headings with two or
more hashes), a two line gap should be given. This helps to denote a new heading rather
than just a new paragraph. While sections can be easily distinguished in a colourful
IDE, the multi-line spacing can be much easier to identify on an editor that doesn't use
colours.

The directory tree found in the [project structure](#project-structure) can be generated
using the following command:

 ```bash
 git ls-tree -r --name-only HEAD | grep -v __init__.py | tree --fromfile
 ```
