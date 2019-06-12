# datagateway-api
ICAT API to interface with the Data Gateway

## Contents
+ [Requirements](#requirements)
+ [Setup](#setup-and-running-the-api)
+ [Project structure](#project-structure)
    + [Main](#main)
    + [Endpoints](#endpoints)
    + [Mapped Classes](#mapped-classes)




## Requirements
The required python libraries:  
   - [SQLAlchemy](https://www.sqlalchemy.org/)    
   - [flask-restful](https://github.com/flask-restful/flask-restful/)  
   - [mypysql](https://pymysql.readthedocs.io/en/latest/)  
   - [requests](https://2.python-requests.org/en/master/)

## Setup and running the API   
The database connection needs to be set up first, currently it is set in `common/constants.py`  

```python 
class Constants:
    DATABASE_URL = "mysql+pymysql://root:rootpw@localhost:13306/icatdb"
```

The API can then be started by running `src/main.py`

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
    │   │   └── openapi.yaml
    │   └── main.py  
    └── test
        ├── resources
        │   ├── entities
        │   │   └──test_<entity>.py
        │   └── non_entities
        │       └── test_<non_entity>.py
        └── test_base
            ├── constants.py
            └── rest_test.py
 `````
#### Main:
The main entry point is in `/src/main.py`. This is where each endpoint route is defined and its 
related class imported e.g.  
 `api.add_resource(DatafilesWithID, "/datafiles/<string:id>")`  
Debugging may also be turned on or off with, `app.run(debug=True)` and `app.run()` respectively.
When debugging is enabled the api will restart every time code changes are detected.


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







