[![Build Status](https://github.com/ral-facilities/datagateway-api/workflows/CI/badge.svg?branch=main)](https://github.com/ral-facilities/datagateway-api/actions?query=workflow%3A%22CI%22)
[![Codecov](https://codecov.io/gh/ral-facilities/datagateway-api/branch/main/graph/badge.svg)](https://codecov.io/gh/ral-facilities/datagateway-api)

# DataGateway API

This is a Flask-based API that fetches data from an ICAT instance, and has two sets of
endpoints, for two different use cases. The first is for
[DataGateway](https://github.com/ral-facilities/datagateway) which has two methods of
interfacing with an ICAT stack, using a
[Python-based ICAT wrapper library](https://github.com/icatproject/python-icat) or using
[sqlalchemy](https://www.sqlalchemy.org/) to communicate directly with an ICAT database.

The other use case is for the
[PaNOSC Search API](https://github.com/panosc-eu/search-api/), required to be
implemented and deployed for ICAT facilities part of the PaNOSC and ExPaNDS projects. A
good summary for the search API is that's it is a limited functionality version of
DataGateway API (in terms of number of endpoints and query filters available to a user),
but adheres more strictly to Loopback than DataGateway API (due to the specification of
the search API). Like DataGateway API, the search API uses Python ICAT to fetch data
from ICAT, and code is reused from DataGateway API where possible.

Both use cases can be run under the same API instance and is fully configurable.
Alternatively, a user can choose to only run one of the use cases (referred to as modes)
if they only require one of the products.

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
curl -sSL https://install.python-poetry.org | python3 -
```

The installation requires the following to be added to your `~/.bashrc` file so the installation folder is on your path.

```bash
export PATH="~/.local/bin:$PATH"
```

Then run `source ~/.bashrc` or open a new terminal and check poetry works by running `poetry --version`

If you encounter this error when installing poetry:

```
ERROR: No matching distribution found for poetry==1.2.0
```

You can try running the installer with python 3.8 with the command below:

```bash
curl -sSL https://install.python-poetry.org | python3.8 -
```

Or you can specify the version you want to install from the listed versions with the command below:

```bash
curl -sSL https://install.python-poetry.org | python3 - --version 1.2.0
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
- `unit_tests` - this uses [pytest](https://docs.pytest.org/en/stable/) to execute the
  automated tests in `test/unit`, tests for the database and ICAT backends, and non-backend
  specific tests. More details about the tests themselves [here](#running-tests).
- `integration_tests` - this uses [pytest](https://docs.pytest.org/en/stable/) to execute the
  automated tests in `test/unit`, tests for the database and ICAT backends, and non-backend
  specific tests. Requires an ICAT backend. More details about the tests themselves [here](#running-tests).

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
curl -sSL https://install.python-poetry.org | python3 -

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

By default, the API will run on `http://localhost:5000` and all requests are made here
e.g. `http://localhost:5000/datagateway-api/sessions`.

## DataGateway API

Depending on the backend you want to use (either `db` or `python_icat`, more details
about backends [here](#datagateway-api-backends)) the connection URL for the backend needs to be set.
These are set in `config.yaml` (an example file is provided in the base directory of
this repository). While both `db_url` and `icat_url` should have values assigned to them
(for best practice), `db_url` will only be used for the database backend, and `icat_url`
will only be used for the Python ICAT backend. Copy `config.yaml.example` to
`config.yaml` and set the values as needed. If you need to create an instance of ICAT,
there are a number of markdown-formatted tutorials that can be found on the
[icat.manual](https://github.com/icatproject/icat.manual/tree/master/tutorials)
repository.

## Search API

Since adding the search API, the endpoints for each type of API can be configured using
`extension` in the respective JSON object. For example, if `extension` is set to
`/search-api`, then requests for the search API can be set to
`http://localhost:5000/search-api` (assuming default host and port configuration). This
option is made configurable for both DataGateway API and the search API.

In addition to the configuration options in `config.yaml`, the mappings between the
PaNOSC and ICAT data models need configuring. An example file exists in
`datagateway_api/` which can be copied from as a starting point. Further explanation of
this file is given [here](#mapping-between-panosc-and-icat-data-models).

Within the search API, there are various entities that would need ICAT 5 to work.
Despite this, ICAT 5 is not required to use the search API, however, not every single
piece of functionality (e.g. getting technique data) will work because that
functionality/data simply doesn't exist in ICAT 4. The only strict ICAT related
requirement for the search API is that the ICAT instance which is used must have the
anon authenticator installed. This is because the search API only deals with public data
so the anon/anon user will have the relevant permissions to not show embargoed data.

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
$ poetry run flask run
```

CMD:

```CMD
> set FLASK_APP=datagateway_api/src/main.py
> poetry run flask run
```

PowerShell:

```powershell
> $env:FLASK_APP = "datagateway_api/src/main.py"
> poetry run flask run
```

The Flask app can be configured so that code changes are monitored and the server will
reload itself when a change is detected. This setting can be toggled using
`flask_reloader` in `config.yaml`. This is useful for development purposes. It should be
noted that when this setting is enabled, the API will go through the startup process
twice. In the case of the ICAT backend, this could dramatically increase startup time if
the API is configured with a large initial client pool size.

If you get the following error when starting the API, changes need to be made to your
Poetry environment:

```python
ModuleNotFoundError: No module named 'urlparse'
```

If using Python 3.10, please use Payara 5 on the ICAT stack which the API is being
pointed at. There is a known issue when making HTTPS connections to Payara (via Python
ICAT).

It is also possible to run the API inside Docker. The `Dockerfile` can be used to build
a Docker image which in turn can be used to create a container. The `Dockerfile` is
configured to create a production image and runs a Gunicorn serve on port `8000` when a
container is started. Environment variables have also been defined in the `Dockerfile`
to allow for values to be passed at runtime to future running containers. These values
are used by the `docker/docker-entrypoint.sh` script to update the config values in the
`config.yaml` file. The environment varialbes are:
- `ICAT_URL` (Default value: `http://localhost`)
- `ICAT_CHECK_CERT` (Default value: `false`)
- `LOG_LOCATION` (Default value: `/dev/stdout`)

To build an image, run:
```bash
docker build -t datagateway_api_image .
```

To start a container on port `8000` from the image that you just built, run:
```bash
docker run -p 8000:8000 --name datagateway_api_container datagateway_api_image 
```

If you want to pass values for the environment variables then instead run:
```bash
docker run -p 8000:8000 --name datagateway_api_container --env ICAT_URL=https://127.0.0.1:8181 --env ICAT_CHECK_CERT=true --env LOG_LOCATION=/datagateway-api-run/logs.log datagateway_api_image
```

## DataGateway API Authentication

Each request requires a valid session ID to be provided in the Authorization header.
This header should take the form of `{"Authorization":"Bearer <session_id>"}` A session
ID can be obtained by sending a POST request to `/sessions`. All endpoint methods that
require a session id are decorated with `@requires_session_id`.

## Swagger Interface

At each of the API's base paths, (`http://localhost:5000/datagateway-api` and
`http://localhost:5000/search-api` by default), a representation of each API will be
shown using [Swagger UI](https://swagger.io/tools/swagger-ui/). This uses an OpenAPI
specification to visualise and allow users to easily interact with the API without
building their own requests. It's great for gaining an understanding in what endpoints
are available and what inputs the requests can receive, all from an interactive
interface.

For DataGateway API, this specification is built with the Database Backend in mind
(e.g. attribute names on example outputs are capitalised), however the Swagger interface
can also be used with the Python ICAT Backend. More details on how the API's OpenAPI
specification is built can be found [here](#generating-the-openapi-specification). An
issue has been [created](https://github.com/ral-facilities/datagateway-api/issues/347)
for the Swagger interface to be up to date when using the Python ICAT backend.

# Running Tests

There are two seperate test runners provided. The integration tests, and the unit tests.
The unit test do not require an ICAT stack to be setup to run. The integration tests do
require an ICAT stack. In order to cover all the code you will need to run both tests.

To run the unit test use `nox -s unit_tests`, and to run the integration tests use `nox -s integration_tests`
The repository contains a variety of tests, to test the functionality of the API works as intended, for convenience
and quicker action runs these are additionally split into the unit and integration tests.
The tests are split into 3 main sections: non-backend specific (testing features such as the date handler), ICAT backend
tests (containing tests for backend specific components, including tests for the
different types of endpoints) and Database Backend tests (like the ICAT backend tests,
but covering only the most used aspects of the API).

The configuration file (`config.yaml`) contains two options that will be used during the
testing of the API. Set `test_user_credentials` and `test_mechanism` appropriately for your test environment, using `config.yaml.example` as a reference. The tests require a
connection to an instance of ICAT, so set the rest of the config as needed.

By default, this will execute the repo's tests in
Python 3.6, 3.7, 3.8, 3.9 and 3.10. For most cases, running the tests in a single Python
version will be sufficient:

```bash
nox -p 3.6 -s unit_tests
nox -p 3.6 -s integration
```

This repository also utilises [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/)
to check how much of the codebase is covered by the tests in `test/`:

```bash
nox -p 3.6 -s unit_tests -- --cov-report term --cov=./datagateway_api
nox -p 3.6 -s integration_tests -- --cov-report term --cov=./datagateway_api
```

With `pytest`, you can output the duration for each test, useful for showing the slower
tests in the collection (sortest from slowest to fastest). The test duration is split
into setup, call and teardown to more easily understand where the tests are being slowed
down:

```bash
nox -p 3.6 -s unit_tests -- --durations=0
nox -p 3.6 -s integration_tests -- --durations=0
```

To test a specific test class (or even a specific test function), you will
need to use pytest itself through poetry. If you want to change the python
version use `poetry env use 3.6` which will generate a virtual env with that
version.

```bash
# Test a specific file
poetry run pytest test/integration/datagateway_api/icat/test_query.py

# Test a specific test class
poetry run pytest test/integration/datagateway_api/icat/test_query.py::TestICATQuery

# Test a specific test function
poetry run pytest test/integration/datagateway_api/icat/test_query.py::TestICATQuery::test_valid_query_exeuction
```

# Project Structure

The project consists of 5 main packages:

- `datagateway_api.src.datagateway_api` - code for DataGateway API, for both database and Python ICAT backends
- `datagateway_api.src.search_api` - Search API specific code e.g. `NestedWhereFilters` for the OR functionality for WHERE clauses
- `datagateway_api.src.common` - code that is shared between DataGateway API and the search API
- `datagateway_api.src.resources` - contains the API resources and their HTTP method definitions (e.g. GET, POST)
- `test` - mixture of automated unit and integration tests written using Pytest

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

Logging configuration can be found in `datagateway_api.src.common.logger_setup`. This
contains a typical dictionary-based config for the standard Python `logging` library
that rotates files after they become 5MB in size.

The default logging location is in the root directory of this repo. This location (and
filename) can be changed by editing the `log_location` value in `config.yaml`. The log
level (set to `WARN` by default) can also be changed using the appropriate value in that
file.

## Date Handler

This is a class containing static methods to deal with dates within the API. The date
handler can be used to convert dates between string and datetime objects (using a format
agreed in `datagateway_api.src.common.constants`) and uses a parser from `dateutil` to
detect if an input contains a date. This is useful for determining if a JSON value given
in a request body is a date, at which point it can be converted to a datetime object,
ready for storing in ICAT. The handler is currently only used in the Python ICAT
Backend, however this is non-backend specific class.

## Exceptions & Flask Error Handling

Exceptions custom to DataGateway API are defined in
`datagateway_api.src.common.exceptions`. Each exception has a status code and a default
message (which can be changed when raising the exception in code). None of them are
backend specific, however some are only used in a single backend because their meaning
becomes irrelevant anywhere else.

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

Filters available for use in the API are defined in `datagateway_api.src.common.filters`.
These filters are all based from `QueryFilter`, an asbtract class to define any filter
for the API. Precedence is used to prioritise in which order filters should be applied,
but is only needed for the Database Backend.

Filtering logic is located in `datagateway_api.src.common.helpers`.
`get_filters_from_query_string()` uses the request query parameters to form filters to
be used within the API. A `QueryFilterFactory` is used to build filters for the correct
backend and the static method within this class is called in
`get_filters_from_query_string()`.

## DataGateway API Backends

As described at the top of this file, there are currently two ways that DataGateway API
creates/fetches/updates/deletes data from ICAT. The intention is each backend allows a
different method to communicate with ICAT, but results in a very similarly behaving
DataGateway API.

### Abstract Backend Class

The abstract class can be found in `datagateway_api.src.datagateway_api.backend` and
contains all the abstract methods that should be found in a class which implements
`Backend`. The typical architecture across both backends is that the implemented
functions call a helper function to process the request and the result of that is
returned to the user.

Each backend module contains the following files which offer similar functionality,
implemented in their own ways:

- `backend.py` - Implemented version of `datagateway_api.src.datagateway_api.backend`
- `filters.py` - Inherited versions of each filter defined in
  `datagateway_api.src.common.filters`
- `helpers.py` - Helper functions that are called in `backend.py`

### Creating a Backend

A function inside `datagateway_api.src.datagateway_api.backends` creates an instance of a
backend using input to that function to decide which backend to create. This function is
called in `main.py` which uses the backend type set in `config.yaml`, or a config value
in the Flask app if it's set (this config option is only used in the tests however). The
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

The ICATQuery classed is in `datagateway_api.src.datagateway_api.icat.query`. This class
stores a query created with Python ICAT
([documentation](https://python-icat.readthedocs.io/en/stable/query.html)). The
`execute_query()` function executes the query and returns either results in either a
JSON format, or a list of
[Python ICAT entity's](https://python-icat.readthedocs.io/en/stable/entity.html) (this
is defined using the `return_json_formattable` flag). Other functions within that class
are used within `execute_query()`.

## Search API

While the search API shares some code from DataGateway API, there are also various
differences in the functionality it offers and the way it goes about offering it.

### Session/Client Handling

Unlike DataGateway API, the search API does not contain any authentication or endpoints
for session handling. This is because the search API only interacts with public data, so
it can be assumed the anon user will be used. To deal with this, only a single client
object is used for the APIs lifecycle, a contrasting solution to DataGateway API. This
object is logged in upon the first request of the APIs lifecycle. For each new request,
session expiry is checked; if the session has expired, the client will be logged in
again so the same object can be used. Using the same client object between users and
requests works because only one user (i.e. the anon user) is being used to query ICAT.

### PaNOSC Data Model

The search API deals with user inputs (via query parameters) and outputs data in the
format defined by the
[PaNOSC data model](https://github.com/panosc-eu/search-api/blob/master/doc/data-model.md).
To interface with ICAT, there needs to be a way of translating between this data model
and the ICAT schema.

#### Mapping between PaNOSC and ICAT Data Models

To map between each data model, there is a JSON file (`search_api_mapping.json`) which
defines the mappings for each PaNOSC entity (and all the attributes within them). This
is configurable so these mappings can be changed as needed - each facility uses ICAT in
slightly different ways; the example file shows the mappings used for ISIS which should
give a good place to start.

Within the mapping file, each of the JSON objects represents a PaNOSC entity. Inside
each object, there is a `base_icat_entity` which defines which ICAT entity the PaNOSC
entity links to. There are also key-value pairs of all of the fields which exist for the
PaNOSC entity, where the value is the ICAT field name. For fields which are related
entities, the value contains a JSON object instead of a string. The contents of this
object are the PaNOSC entity name that the field name relates to and also the ICAT field
name translation. Looking at the example file alongside the ICAT schema is a good way to
understand how the mappings work.

The only exceptions that exist in the mapping file is for unique mapping cases; when
mapping PaNOSC `pid` fields to ICAT, a list of ICAT field names are needed. This is so
if a persistent identifier does not exist, it can use an alternative field name as an
identifier. Some facilities don't use persistent identifiers for all of their metadata,
so this solution is needed to prevent things from breaking. A similar case exists for on
the `base_icat_entity` for the `Parameter` entity, where a list of ICAT entity names are
also needed. This is because a `Parameter` can either link to a document or a dataset.
In ICAT, there are specific entities that are used to store parameters for
investigations and datasets (e.g. `InvestigationParameter` and `DatasetParameter`).
Since ICAT parameter types have three different places where values can be stored
(`numericValue`, `stringValue`, `dateTimeValue`), these need to be specified in a list
too. Order is important in this case, so it is recommended to keep them in the same
order as shown in the example file.

### Query Parameter/Filter Factory

Most of the query filters that exist in DataGateway API are also present in the search API.
However, inside the query parameters of an incoming request, they are formatted differently
(see [query filter syntax](https://github.com/panosc-eu/search-api/blob/master/doc/query.md))
so a search API specific factory class to deal with the query parameters was needed.

### NestedWhereFilters/OR Conditions

The search API requires conditions to be
[joined together using `OR`](https://github.com/panosc-eu/search-api/blob/master/doc/query.md#joining-queries),
something which isn't seen in DataGateway API. This is mainly because this isn't
directly supported by Python ICAT; its query builder class only supports the joining of
conditions by the `AND` keyword. To solve this, when the query filter factory detects an
explicit joining of conditions (via the use of `AND` or `OR`), a `NestedWhereFilters`
object is created to store the conditions from the request. This class has the concept
of a left hand side and right hand side and will join them together when the object is
converted to a string - an action performed when the JPQL query is being built.

### Search API Query

The class `SearchAPIQuery` contains everything needed to build and handle a JPQL query
to be sent to an ICAT instance. `ConditionSettingQuery` is a version of the Python ICAT
query class that allows the search API to set the conditions using a string, rather than
adding conditions via dictionaries. This is needed where queries are joined with `AND`
or `OR`. This collates all the work from `NestedWhereFilters` so all requires types of
conditions can be supported.

### Search Scoring

Search scoring allows for the results returned by the Search API to be scored in terms of
relevancy. The config option `enabled` from the `search_scoring` object in `config.yaml`
can be used to enable or disable the search scoring. When enabled, it handles the `query`
filter provided in the requests sent by the [Federated Photon and Neutron Search Service](https://github.com/panosc-eu/panosc-federated-search-service),
otherwise, it returns an error to indicate that the `query` filter is not supported.
For this functionality to work, an instance of the [PaNOSC Search Scoring Service](https://github.com/panosc-eu/panosc-search-scoring/)
is needed which has been configured and populated as per the instructions in its
repository and can return scores. The full URL to its `/score` endpoint will need to be
provided to the config option `api_url` from the `search_scoring` object in `config.yaml`
so that the Search API know where to send its result from ICAT along with the value from
the `query` filter for scoring.

The [European Photon and Neutron Open Data Search Portal](https://data.panosc.eu/)
requires all Search APIs that want to be integrated with the portal to support search
scoring.

## Generating the OpenAPI Specification

When the config option `generate_swagger` is set to true in `config.yaml`, a YAML
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
configured in `config.yaml`.

When used on a machine that doesn't use UTC timezone, you may find there are a mix of
timezones when querying the API. This issue was found on SciGateway Preprod when using
BST and there would be a mix of +00:00 and +01:00 timezones
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

This collection has not been updated for the search API endpoints, so can only be used
to query DataGateway API.

# API Versioning

This repository uses semantic versioning as the standard for version number
incrementing, with the version stored in `pyproject.toml`. There is a GitHub Actions
workflow (`release-build.yml`) which runs when main is updated (i.e. when a pull
request is merged). This uses
[python-semantic-release](https://github.com/relekang/python-semantic-release) to
determine whether a release needs to be made, and if so, whether a major, minor or patch
version bump should be made. This decision is made based on commit message content.

In a PR, at least one commit must follow the
[Angular commit message format](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#commit-message-format)
and use one of the
[conventional commit types](https://github.com/commitizen/conventional-commit-types/blob/master/index.json).
Note, there are no scopes (part of the Angular message format) configured for this repo
so there's no need to make use of this feature. Compliance to this format and use of
standard types will be checked by
[semantic-pull-requests](https://github.com/zeke/semantic-pull-requests) which is a
GitHub app installed into this repo and runs alongside existing CI jobs for pull
requests. For example, the following commit messages follow the conventional commit
standard:

```
# Commit to edit a CI job
ci: edit linting job #issue-number

# Commit for a bug fix
fix: fix bug found with count endpoints #issue-number

# Commit for a new feature
feat: add endpoints for search API #issue-number

# Commit which introduces a breaking change for users
<commit-type>: change format of `config.yaml`, the previous version is no longer supported #issue-number

BREAKING CHANGE: this feature means X functionality has been removed
```

For each pull request, only one commit message in this format is required to satisfy the
semantic pull request checker. Requiring only one commit message in this format should
hopefully not impose this commit style on developer. However, it is encouraged to use it
where possible, as the types are also used to form `CHANGELOG.md`.

New releases are only made when a `fix:` (patch), `feat:` (minor) or `BREAKING CHANGE:`
(major) commit type is found between the previous release and the most recent commit on
main. When the version is bumped, a GitHub tag and release is made which contains the
source code and the built versions of the API (sdist and wheel).

To check how the version number will be impacted before merging a pull request, use the
following command to show the version which will be made when the GitHub Actions release
build job runs (upon merging a branch/PR):

```bash
poetry run semantic-release print-version
```

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
