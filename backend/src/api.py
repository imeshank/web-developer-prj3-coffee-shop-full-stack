import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


db_drop_and_create_all()

# ROUTES


@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        # fetch all drinks in the db
        coffee_list = Drink.query.all()
        # convert fetched coffee list to short data representation
        drinks = [coffee.short() for coffee in coffee_list]

        if len(drinks) == 0:
            print("coffee list is empty")
            abort(404)

        return jsonify(
                    {
                        "success": True,
                        "drinks": drinks
                    }
        )
    except Exception as e:
        if '404' in str(e):
            abort(404)
        else:
            print(e)


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_details(payload):
    try:
        coffee_list = Drink.query.all()
        drinks = [coffee.long() for coffee in coffee_list]

        if len(drinks) == 0:
            print("coffee list is empty")
            abort(404)

        return jsonify(
                    {
                        "success": True,
                        "drinks": drinks
                    }
                )
    except Exception as e:
        if '404' in str(e):
            abort(404)
        else:
            print(e)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(payload):
    # get data in the request body
    body = request.get_json()
    new_title = body.get("title", None)
    new_recipe = body.get("recipe", None)

    if type(new_recipe) is dict:
        new_recipe = [new_recipe]
    try:
        drink = Drink(title=new_title, recipe=json.dumps(new_recipe))
        drink.insert()
        return jsonify(
            {
                "success": True,
                "drinks": [drink.long()]
            }
        )
    except Exception as e:
        print(e)


@app.route("/drinks/<int:id>", methods=["PATCH"])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    body = request.get_json()
    new_title = body.get("title", None)
    new_recipe = body.get("recipe", None)
    try:
        # fetch the corresponding row from the db according to the given id
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink is None:
            abort(404)

        if new_title is not None:
            drink.title = new_title
        if new_recipe is not None:
            drink.recipe = json.dumps(new_recipe)

        drink.update()
        return jsonify(
            {
                "success": True,
                "drinks": [drink.long()]
            }
        )
    except Exception as e:
        if '404' in str(e):
            abort(404)
        else:
            print(e)


@app.route("/drinks/<int:id>", methods=["DELETE"])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink is None:
            abort(404)
        drink.delete()
        return jsonify(
            {
                "success": True,
                "deleted": drink.id
            }
        )
    except Exception as e:
        if '404' in str(e):
            abort(404)
        else:
            print(e)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
        }), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
        }), 500


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
        }), 400


@app.errorhandler(403)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "forbidden"
        }), 403


@app.errorhandler(401)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized"
        }), 401


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code
