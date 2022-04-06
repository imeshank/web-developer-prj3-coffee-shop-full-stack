# Coffee Shop Full Stack

## Introduction
This is a full stack drink menu application. This application includes following functionalities:

1) Display graphics representing the ratios of ingredients in each drink.
2) Allow public users to view drink names and graphics.
3) Allow the shop baristas to see the recipe information.
4) Allow the shop managers to create new drinks and edit existing drinks.

## Getting Started

Developers using this project should already have Python3(Python 3.7.0), pip, node(v12.20.1), and npm installed on their local machines.

## Backend

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run
```
### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:drinks`
   - `get:drinks-detail`
   - `post:drinks`
   - `patch:drinks`
   - `delete:drinks`
6. Create new roles for:
   - Barista
     - can `get:drinks-detail`
     - can `get:drinks`
   - Manager
     - can perform all actions
7. How to test your endpoints with [Postman](https://getpostman.com).
   - Register 2 users in Auth0 Account - assign the Barista role to one and Manager role to the other.
   - Sign into each account and make note of the JWT.
   - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
   - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and include the JWT in the token field (you should have noted these JWTs).
   - Run the collection.

## Frontend

### Installing Dependencies

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node(v12.20.1) (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing Ionic Cli

The Ionic Command Line Interface is required to serve and build the frontend. Instructions for installing the CLI is in the [Ionic Framework Docs](https://ionicframework.com/docs/installation/cli).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```
### Required Tasks

#### Configure Environment Variables

Ionic uses a configuration file to manage environment variables. These variables ship with the transpiled software and should not include secrets.

- Open `./src/environments/environments.ts` and ensure each variable reflects the system you stood up for the backend.

### Running Your Frontend in Dev Mode

Ionic ships with a useful development server which detects changes and transpiles as you work. The application is then accessible through the browser on a localhost port. To run the development server, cd into the `frontend` directory and run:

```bash
ionic serve
```

Open http://localhost:8100/ to view it in the browser.

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at, `http://localhost:5000/`. The Frontend app is hosted at, `http://localhost:8100/`
- Authentication: You need to obtain two JWT tokens for manager user and barista user. (Run the frontend, go to user tab and click the log in button. Then you can get the JWT token for the logged in user)

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return following error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 405: Method not allowed
- 500: Internal server error
- 403: forbidden
- 401: unauthorized

### Endpoints

#### GET '/drinks'
- This is a public endpoint.
- Fetches a dictionary of drinks which has drink.short() data representation and success value.
- Request Arguments: None
- Returns: An json object, that contains success value and available all drinks with the drink.short() data representation or appropriate status code indicating reason for failure.

```
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "parts": 1
                }
            ],
            "title": "water"
        }
    ],
    "success": true
}
```

#### GET '/drinks-detail'
- This endpoint require the 'get:drinks-detail' permission.
- Fetches a dictionary of drinks which has drink.long() data representation and success value.
- Request Arguments: None
- Returns: An json object, that contains success value and available all drinks with the drink.long() data representation or appropriate status code indicating reason for failure.

```
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 1
                }
            ],
            "title": "water"
        }
    ],
    "success": true
}
```

#### POST '/drinks'
- This endpoint require the 'post:drinks' permission.
- Creates a new drink in the drink table using the submitted json which includes title, and the receipe
- Request Arguments: Request body,
```
{
    "title": "Water3",
    "recipe": {
        "name": "Water",
        "color": "blue",
        "parts": 1
    }
}
```
- Returns: A json object which includes, a success value, and newly created drink details with drink.long() data representation or appropriate status code indicating reason for failure.

```
{
    "drinks": [
        {
            "id": 2,
            "recipe": [
                {
                    "color": "blue",
                    "name": "Water",
                    "parts": 1
                }
            ],
            "title": "Water3"
        }
    ],
    "success": true
}
```

#### PATCH '/drinks/<id>'
- This endpoint require the 'patch:drinks' permission.
- Updates a existing drink in the drink table using the submitted json which includes title, or the receipe
- Request Arguments: Existing model id(int, required, URL parameter)
                     Request body,
```
{
    "title": "Water5"
}
```
- Returns: A json object which includes, a success value, and newly updated drink details with drink.long() data representation or appropriate status code indicating reason for failure.

```
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 1
                }
            ],
            "title": "Water5"
        }
    ],
    "success": true
}
```

#### DELETE '/drinks/<id>'
- This endpoint require the 'delete:drinks' permission.
- Delete the row of the given drink id if it exists in the drink table.
- Request Arguments: drink id(int, required, URL parameter)
- Returns: A json object which includes, a success value, and id of the deleted record

```
{
    "deleted": 1,
    "success": true
}
```


