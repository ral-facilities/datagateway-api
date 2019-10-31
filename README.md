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
      - [Querying and filtering](#querying-and-filtering)
      - [Swagger Generation](#generating-the-swagger-spec-openapiyaml)
      - [Authentication](#authentication)
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
#### Main:
`main.py` is where the flask_restful api is set up. This is where each endpoint resource class is generated and mapped 
to an endpoint.

Example:  
 `api.add_resource(get_endpoint(entity_name, endpoints[entity_name]), f"/{entity_name.lower()}")`	   
   

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


