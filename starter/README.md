# Full Stack Capstone Project

# Lego Database API

## Introduction

API that allows managing databases for Lego sets and collectors. It helps inventory managers to post, update and delete information about collectors and their collections.

## Motivation

The motivation of this project is to reinforce the skills and concepts taught in Full-Stack Developer Nanodegree program to build an API and host it.

- Coding in Python 3
- Relational Database Architecture
- Modeling Data Objects with SQLAlchemy
- Internet Protocols and Communication
- Developing a Flask API
- Authentication and Access
- Authentication with Auth0
- Authentication in Flask
- Role-Based Access Control (RBAC)
- Testing Flask Applications
- Deploying Applications

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

```
python -m virtualenv env
source env/bin/activate
```

In Windows:

```
python -m virtualenv env
source env/Scripts/activate
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database.

- [PostgreSQL 13.0](https://www.postgresql.org/) is an open source object-relational database system.

- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) is an extension that handles SQLAlchemy database migrations for Flask applications.

- [Auth0](https://auth0.com/) is an adaptable authentication and authorization platform.

- [Postman](https://www.postman.com/) is a collaboration platform for API development. We use it to create, share, test and document APIs.

- [Heroku](https://www.heroku.com/platform) is a cloud platform to host applications, databases and other services.

## Running the server

From within the `starter` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py
```

In Windows:

```bash
set FLASK_APP=api.py
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Testing

To run test file, execute:

```bash
python test_app.py
```

## API Documentation

### Authentication

This application has three different roles:

- Basic User
    - can `get:sets`, `get:collectors`
- Lego Set Manager
    - has all the permissions `Basic User` has
    - can also `get:sets-detail`, `post:sets`, `patch:sets`, `delete:sets`, `get:collectors-detail`
- Director
    - has all the permissions `Lego Set Manager` has
    - can also `post:collectors`, `patch:collectors`, `delete:collectors`

Bearer tokens for `Lego Set Manager` and `Director` are available in the `setup.sh` file.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
  "success": False,
  "error": 404,
  "message": "resource not found"
}
```

The API will return five error types:
- 401: Unauthorized
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Unprocessable
- 500: Internal Server Error

### Base URL

`https://lego-database.herokuapp.com/`

### Endpoints

#### GET '/sets'
General:
- Returns a list of lego set objects, and success value.
Sample:
- Postman:
    - `https://lego-database.herokuapp.com/sets`
- Curl:
    - `curl -X GET https://lego-database.herokuapp.com/sets`
- Response:
```
{
    "sets": [
        {
            "name": "Tuk Tuk",
            "number of pieces": 155,
            "release year": "2021",
            "set number": 40469
        }
    ],
    "success": true
}
```

#### GET '/sets-detail'
General:
- Returns a detailed list of lego set objects including owners, and success value.
Sample:
- Postman:
    - `https://lego-database.herokuapp.com/sets-detail`
- Curl:
    -  `curl -X GET -H "Authorization: ${MANAGER_TOKEN}" https://lego-database.herokuapp.com/sets-detail`
- Response:
```
{
    "sets": [
        {
            "collectors": [
                "Murat C"
            ],
            "name": "Tuk Tuk",
            "number of pieces": 155,
            "release year": "2021",
            "set number": 40469
        }
    ],
    "success": true
}
```

#### POST '/sets'
General:
- Creates a new lego set using the submitted set number, name, release year and number of pieces. Returns the new lego set object, and success value.
Sample:
- Postman:
    - `https://lego-database.herokuapp.com/sets`
    - Body:
```
    {
        "id": "21325",
        "name": "Medieval Blacksmith",
        "year": "2021",
        "pieces": 2164
    } 
```
- Curl:
```
    curl -X POST
         -H 'Content-type: application/json'
         -H "Authorization: ${MANAGER_TOKEN}"
         -d '{"name": "Medieval Blacksmith", "pieces": 2164, "year": "2021", "id": 21325}'
         https://lego-database.herokuapp.com/sets
```
- Response:
```
{
    "created": {
        "name": "Medieval Blacksmith",
        "number of pieces": 2164,
        "release year": "2021",
        "set number": 21325
    },
    "success": true
}
```

#### PATCH '/sets/{lego_id}'
General:
- Updates an existing lego set using the submitted set number, name, release year and number of pieces. Returns the updated lego set object, and success value.
Sample:
- Postman:
    - `https://lego-database.herokuapp.com/sets/21325`
    - Body:
```
    {
        "year": "2021",
        "pieces": 2164
    }
```
- Curl:
```
    curl -X PATCH
         -H 'Content-type: application/json'
         -H "Authorization: ${MANAGER_TOKEN}"
         -d '{"year": "2021", "pieces": 2164}'
         https://lego-database.herokuapp.com/sets/21325
```
- Response
```
{
    "success": true,
    "updated": {
        "collectors": [],
        "name": "Medieval Blacksmith",
        "number of pieces": 2164,
        "release year": "2021",
        "set number": 21325
    }
}
```

#### DELETE '/sets/{lego_id}'
General:
- Deletes an existing lego set. Returns the number of the deleted lego set, and success value.
Sample:
- Postman:
    - `https://lego-database.herokuapp.com/sets/21325`
- Curl:
```
    curl -X DELETE
         -H 'Content-type: application/json'
         -H "Authorization: ${MANAGER_TOKEN}"
         https://lego-database.herokuapp.com/sets/21325
```
- Response
```
{
    "deleted": 21325,
    "success": true
}
```

#### GET '/collectors'
General:
- Returns a list of collector objects, and success value.
Sample:
- Postman:
    - `https://lego-database.herokuapp.com/collectors`
- Curl:
    - `curl -X GET https://lego-database.herokuapp.com/collectors`
- Response:
```
{
    "collectors": [
        {
            "location": "Fremont",
            "name": "Murat C"
        }
    ],
    "success": true
}
```

#### GET '/collectors-detail'
General:
- Returns a detailed list of collector objects including their collection, and success value.
Sample:
- Postman:
    - `https://lego-database.herokuapp.com/collectors-detail`
- Curl:
    -  `curl -X GET -H "Authorization: ${DIRECTOR_TOKEN}" https://lego-database.herokuapp.com/collectors-detail`
- Response:
```
{
    "collectors": [
        {
            "id": 1,
            "location": "Fremont",
            "name": "Murat C",
            "sets collected": [
                40469
            ]
        }
    ],
    "success": true
}
```

#### POST '/collectors'
General:
- Creates a new collector using the submitted name, location and collection. Returns the new collector object, and success value.
Sample:
- Postman:
    - `https://lego-database.herokuapp.com/collectors`
    - Body:
```
{
    "name": "B C",
    "location": "Fremont",
    "legos": [40469]
}
```
- Curl:
```
    curl -X POST
         -H 'Content-type: application/json'
         -H "Authorization: ${DIRECTOR_TOKEN}"
         -d '{"name": "B C", "location": "Fremont", "legos": [40469]}'
         https://lego-database.herokuapp.com/collectors
```
- Response:
```
{
    "created": {
        "id": 2,
        "location": "Fremont",
        "name": "B C",
        "sets collected": [
            40469
        ]
    },
    "success": true
}
```

#### PATCH '/collectors/{collector_id}'
General:
- Updates an existing collector using the submitted name, location and collections. Returns the updated collector object, and success value.
Sample:
- Postman:
    - `https://lego-database.herokuapp.com/collectors/1`
    - Body:
```
{
      "legos": [40469]
      }

```
- Curl:
```
    curl -X PATCH
         -H 'Content-type: application/json'
         -H "Authorization: ${DIRECTOR_TOKEN}"
         -d '{"legos": [40469]}'
         https://lego-database.herokuapp.com/collectors/1
```
- Response:
```
{
    "success": true,
    "updated": {
        "id": 1,
        "location": "Fremont",
        "name": "Murat C",
        "sets collected": [
            40469
        ]
    }
}
```

#### DELETE '/collectors/{collector_id}'
General:
- Deletes an existing collector. Returns the id of the deleted collector, and success value.
Sample:
- Postman:
    - `https://lego-database.herokuapp.com/collectors/2`
- Curl:
```
    curl -X DELETE
         -H 'Content-type: application/json'
         -H "Authorization: ${DIRECTOR_TOKEN}"
         https://lego-database.herokuapp.com/collectors/2
```
- Response
```
{
    "deleted": 2,
    "success": true
}
```
