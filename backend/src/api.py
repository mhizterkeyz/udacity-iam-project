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

def find_drink_or_fail(drink_id):
    drink = Drink.query.get(drink_id)
    if drink is None:
        abort(404)
    
    return drink

# ROUTES
@app.route('/drinks')
def get_drinks():
    return jsonify({
        "success": True,
        "drinks": [drink.short() for drink in Drink.query.all()]
    })

@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_details(jwt_payload):
    return jsonify({
        "success": True,
        "drinks": [drink.long() for drink in Drink.query.all()]
    })

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt_payload):
    try:
        request_body = request.get_json()
        request_body['recipe'] = json.dumps(request_body['recipe'])
        if 'id' in request_body:
            del request_body['id']

        drink = Drink(**request_body)
        drink.insert()

        return jsonify({
            "success": True,
            "drinks": drink.long()
        })
    except:
        abort(422)

@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(jwt_payload, drink_id):
    drink = find_drink_or_fail(drink_id)
    try:
        request_body = request.get_json()
        if 'title' in request_body:
            drink.title = request_body['title']
        if 'recipe' in request_body:
            drink.recipe = json.dumps(request_body['recipe'])
        
        drink.update()

        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        })
    except:
        abort(422)

@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt_payload, drink_id):
    drink = find_drink_or_fail(drink_id)
    drink.delete()
    return jsonify({
        "success": True,
        "delete": drink_id
    })

# Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(400)
def handle_bad_request_error(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

@app.errorhandler(404)
def handle_not_found_error(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(500)
def handle_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "something went wrong"
    }), 500

@app.errorhandler(AuthError)
def handle_auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), error.status_code
