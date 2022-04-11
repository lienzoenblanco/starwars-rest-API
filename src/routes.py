"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Favorite
#from models import Person

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

@api.route("/favourite", methods=["POST"])
def add_favourite():
    body = request.get_json()

    if body["type"] == "character":
        new_favourite = Favourite(user_id=body["user_id"], character_id=body["character_id"])
    elif body["type"] == "planet":
        new_favourite = Favourite(user_id=body["user_id"], planet_id=body["planet_id"])
       
    db.session.add(new_favourite)
    db.session.commit()

    return jsonify(f"A new favourite is added: {new_favourite.serialize()}"), 200

@api.route("/favourite/<int:user_id>", methods=["GET"])
def get_all_favourites(user_id):
    c = Favourite()
    return jsonify(c.get_all_favourites(user_id)), 200


@api.route("/favourite/<int:favourite_id>", methods=["DELETE"])
def delete_favourite(favourite_id):
    favourite = Favourite.query.get(favourite_id)

    if favourite == None:
        return f"There is no favourite with ID '{favourite_id}'"
    else:
        Favourite.query.filter_by(id=favourite_id).delete()
        db.session.commit()

        return jsonify(f"Favourite with ID '{favourite_id}' has been deleted!!"), 200 


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
