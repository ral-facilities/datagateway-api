# datagateway-api
ICAT API to interface with the Data Gateway

## Contents
- [datagateway-api](#datagateway-api)
    + [Requirements](#requirements)
    + [Setup](#setup-and-running-the-api)
    + [Project structure](#project-structure)
        + [Main](#main)
        + [Endpoints](#endpoints)
        + [Mapped Classes](#mapped-classes)
        + [Querying and Filtering](#querying-and-filtering)
        + [Swagger Generation](#generating-the-swagger-spec)
        + [Database Generator](#database-generator)
    + [Running the Tests](#running-tests)




## Requirements
All requirements can be installed with `pip install -r requirements.txt`

The required python libraries:  
   - [SQLAlchemy](https://www.sqlalchemy.org/)    
   - [flask-restful](https://github.com/flask-restful/flask-restful/)  
   - [pymysql](https://pymysql.readthedocs.io/en/latest/)  
   - [requests](https://2.python-requests.org/en/master/)
   - [pyyaml](https://pyyaml.org/wiki/PyYAMLDocumentation) (For the swagger generation)
   - [pip-tools](https://github.com/jazzband/pip-tools) (For generating requirements.txt)

## Setup and running the API   
The database connection needs to be set up first. This is set in config.json, an example config file called `config.json.example` is provided.


To run the API from the command line, the enviroment variable `FLASK_APP` should be set to `src/main.py`. Once this is 
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
    │   │   │   └── <entity>_endpoints.py
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
`main.py` is where the flask_restful api is set up. This is where each endpoint resource class is 
imported and mapped to an endpoint.  

Example:  
 `api.add_resource(DatafilesWithID, "/datafiles/<int:id>")`  
This means that the http methods defined in the `DatafilesWithID` class are mapped to `/datafiles/<int:id>`   



#### Endpoints:  
The logic for each endpoint are within `/src/resources`. They are split into entities 
and non entities. Each endpoint has its own file within these folders e.g. the datafile endpoint
is in `/src/resources/entities/datafiles_endpoints.py`. Inside of this file there is a class for
each type of endpoint e.g. `/datafiles/count`. Each class is then imported to `/main.py` and added
as a resource.


#### Mapped classes:
The classes mapped from the database are stored in `/common/models/db_models.py`. Each model was 
automatically generated using sqlacodegen. A class `EntityHelper` is defined so that each model may
inherit two methods `to_dict()` and `update_from_dict(dictionary)`, both used for returning entities 
and updating them, in a form easily converted to JSON.  

#### Querying and filtering:
The querying and filtering logic is located in `/common/database_helpers.py`. In this module the abstract `Query` and
`QueryFilter` classes are defined as well as their implementations. The functions that are used by various endpoints to
query the database are also in this module.
Class diagram for this module:
![image](https://user-images.githubusercontent.com/44777678/66651511-1d401a80-ec2b-11e9-96a4-316e94939a0f.png)


#### Authentication
Each request requires a valid session ID to be provided in the Authorization header. This header should take the form of `{"Authoirzation":"Bearer <session_id>"}` A session ID can be obtained by
sending a post request to `/sessions/`  
All endpoint methods that require a session id are decorated with `@requires_session_id`



<<<<<<< HEAD
#### Generating the swagger spec:
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

=======
## Database Generator
There is a tool to generate mock data into the database. It is located in `util/icat_db_generator.py`
By default it will generate 20 years worth of data (approx 70,000 entities). The script makes use of 
`random` and `Faker` and is seeded with a seed of 1. The seed and number of years of data generated can 
be changed by using the arg flags `-s` or `--seed` for the seed, and `-y` or `--years` for the number of years.
For example:  
`python -m util.icat_db_generator -s 4 -y 10` Would set the seed to 4 and generate 10 years of data.
>>>>>>> master

## Running Tests
To run the tests use `python -m unittest discover`


