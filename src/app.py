"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for # url_for??
from flask_migrate import Migrate
from flask_swagger import swagger # is this a joke
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
#from models import Person

# where your endpoints should be coded

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        User
    }

    return jsonify(response_body), 200

# add get for user, planets, and favorites / add post and delete for favorites

@app.route('/people', methods=['GET'])
def get_people():

    characters = Character.query.all()
    response_body = [char.serialize() for char in characters] # study for loop here

    return jsonify(response_body), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):

    character = Character.query.get(people_id) # research syntax here
    response_body = character.serialize()

    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_planets():

    planets = Planet.query.all()
    response_body = [planet.serialize() for planet in planets]

    return jsonify(response_body), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_one_planet(planets_id):

    planet = Planet.query.get(planets_id) # research syntax here
    response_body = planet.serialize()

    return jsonify(response_body), 200

# FAVORITES
# /users, /users/favorites (GET)
# /favorite/planet/<int:planet_id>, favorite/people/<int:planet_id>, (POST and DELETE)

@app.route('/users', methods=['GET'])
def get_users():

    users = User.query.all()
    response_body = [user.serialize() for user in users]

    return jsonify(response_body), 200

@app.route('/favorites', methods=['GET']) #get all favorites
def get_favorites():

    favorites = Favorite.query.all()
    response_body = [fav.serialize() for fav in favorites]

    return jsonify(response_body), 200

@app.route('/<user>/favorites', methods=['GET'])
def get_user_favorites(user):

    favorites = Favorite.query.filter_by(user_id = user) # re-study filter_by
    response_body = [fav.serialize() for fav in favorites]

    return jsonify(response_body), 200

@app.route('/<user>/favorite/', methods=['POST'])
def create_favorite(user):

    body = request.json #request.json gives body in dictionary format
    print(body)

    favorite = Favorite(name = body["name"], link = body["link"], user_id = user)
    db.session.add(favorite)
    db.session.commit()
    return "recieved", 200

@app.route('/favorite/<int:favid>', methods=['DELETE'])
def delete_favorite(favid):

    favorite = db.session.get(Favorite, favid) 
    db.session.delete(favorite)
    db.session.commit()
    return "recieved", 200

# run query with filter by to filter for entries with user ID equal to user whose favorites you want to see





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
