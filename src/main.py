"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Favorite

api = Blueprint("api", __name__)

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



@app.route('/user/<user_id>', methods=['GET'])
def handle_hello(user_id):
    body = User.query.get(user_id)
    return jsonify(user.serialize()), 200



@api.route("/character", methods=["GET"])
def get_all_characters():
    c = Character()
    return jsonify(c.get_all_characters()), 200

@api.route("/character/<int:character_id>", methods=["GET"])
def get_character(character_id):
    character = Character.query.get(character_id)

    if character == None:
        response = f"There is no character with ID '{character_id}'"
    else:
        response = character.serialize()

    return jsonify(response), 200


@api.route("/planet", methods=["GET"])
def get_all_planets():
    p = Planet()
    return jsonify(p.get_all_planets()), 200

@api.route("/planet/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)

    if planet == None:
        response = f"There is no planet with ID '{planet_id}'"
    else:
        response = planet.serialize()

    return jsonify(response), 200

@api.route("/favorite", methods=["POST"])
def add_favorite():
    body = request.get_json()

    if body["type"] == "character":
        new_favorite = Favorite(user_id=body["user_id"], character_id=body["character_id"])
    elif body["type"] == "planet":
        new_favorite = Favorite(user_id=body["user_id"], planet_id=body["planet_id"])
       
    db.session.add(favorite)
    db.session.commit()

    return jsonify(f"A new favorite is added: {new_favorite.serialize()}"), 200

@api.route("/favorite/<int:user_id>", methods=["GET"])
def get_all_favorites(user_id):
    c = favorite()
    return jsonify(c.get_all_favorites(user_id)), 200


@api.route("/favorite/<int:favorite_id>", methods=["DELETE"])
def delete_favorite(favorite_id):
    favorite = Favorite.query.get(favorite_id)

    if favorite == None:
        return f"There is no favorite with ID '{favorite_id}'"
    else:
        favorite.query.filter_by(id=favorite_id).delete()
        db.session.commit()

        return jsonify(f"favorite with ID '{favorite_id}' has been deleted!!"), 200 


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
