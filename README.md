# datagateway-api
ICAT API to interface with the Data Gateway

## Contents
- [datagateway-api](#datagateway-api)
  - [Contents](#contents)
  - [Requirements](#requirements)
  - [Setup and running the API](#setup-and-running-the-api)
  - [Project structure](#project-structure)
      - [Main:](#main)
      - [Endpoints:](#endpoints)
      - [Mapped classes:](#mapped-classes)
  - [Database Generator](#database-generator)
  - [Running Tests](#running-tests)




## Requirements
All requirements can be installed with `pip install -r requirements.txt`, and all development requirements can be installed with `pip install -r dev-requirements.txt`

The required python libraries:  
   - [SQLAlchemy](https://www.sqlalchemy.org/)    
   - [flask-restful](https://github.com/flask-restful/flask-restful/)  
   - [pymysql](https://pymysql.readthedocs.io/en/latest/)  
   - [requests](https://2.python-requests.org/en/master/)
   - [pyyaml](https://pyyaml.org/wiki/PyYAMLDocumentation) (For the swagger generation)
   - [pip-tools](https://github.com/jazzband/pip-tools) (For generating requirements.txt)

## Setup and running the API   
The database connection needs to be set up first. This is set in config.json, an example config file called `config.json.example` is provided.

Ideally the API would be run with:  
`python -m src.main`
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

More information can be found [here](http://flask.pocoo.org/docs/1.0/cli/)

Alternatively the api can be run with `python -m src.main`

By default the api will run on `http://localhost:5000` and all requests are made here

e.g.
`http://localhost:5000/sessions`



## Project structure
The project consists of 3 main packages: common, src and test. common contains modules shared across test and src such as the database mapping classes.
src contains the api resources and their http method definitions, and test contains tests for each endpoint.

This is illustrated below.


`````
─── datagateway-api
    ├── common  
    │   ├── models
    │   │   └── db_models.py
    │   ├── constants.py
    │   ├── database_helpers.py
    │   ├── exceptions.py
    │   └── helpers.py
    ├── src
    │   ├── resources
    │   │   ├── entities
    │   │   │   ├── entity_endpoint.py
    │   │   │   └── entity_map.py
    │   │   └── non_entities
    │   │       └── <non_entity>_endpoints.py
    │   ├── swagger
    │   │   └── openapi.yaml
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
#### Main:
The main entry point is in `/src/main.py`. This is where each endpoint route is defined and its 
related class imported e.g.  
 `api.add_resource(DatafilesWithID, "/datafiles/<int:id>")`  
Debugging may also be turned on or off with, `app.run(debug=True)` and `app.run()` respectively.
When debugging is enabled the api will restart every time code changes are detected.


#### Endpoints:  
The logic for each endpoint are within `/src/resources`. They are split into entities, non_entities and 
table_endpoints. The entities package contains `entities_map` which maps entity names to their sqlalchemy
model. The `entity_endpoint` module contains the function that is used to generate endpoints at start up.
`table_endpoints` contains the endpoint classes that are table specific. Finally, non_entities contains the
session endpoint.


#### Mapped classes:
The classes mapped from the database are stored in `/common/models/db_models.py`. Each model was 
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

## Running Tests
To run the tests use `python -m unittest discover`


