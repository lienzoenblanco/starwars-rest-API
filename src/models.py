from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
             "is_active": self.is_active, 
        }

    def get_all_users(self):
        users = User.query.all()        
        user_list = list(map(lambda user: user.serialize(), users)) 
        
        return user_list

        


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    temperature = db.Column(db.Float)
    image_url = db.Column(db.String(250))
    
    def __repr__(self):
        return "<Planet %r>" % f"id: {self.id}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "temperature": self.temperature,
            "image_url": self.image_url            
        }

    def get_all_planets(self):
        planets = Planet.query.all()        
        planets_list = list(map(lambda planet: planet.serialize(), planets)) 
        
        return planets_list

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    url = db.Column(db.String(60))
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    planet = db.relationship(Planet)

    def __repr__(self):
        return '<Character %r>' % self.id

    def serialize(self):
        return{
            "id": self.id,
            "name": self.id,
            "url": self.url,
            "planet_id": self.planet_id,
        }

class Favorite(db.Model):
     id = db.Column(db.Integer,primary_key=True)
     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
     favorite_character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
     favorite_planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
     character = db.relationship(Character)
     planet = db.relationship(Planet)

     def __repr__(self):
        return '<Favorite %r>' % self.id

     def serialize(self):
         return {
            "id": self.id,
            "user_id": self.user_id,
            "favorite_peope_id": self.favorite_peope_id,
            "favorite_planet_id": self.favorite_planet_id,
         }

     def get_all_favorites(self, user_id):
        favorites = Favorite.query.all()        
        favorites_list = list(map(lambda favorite: favorite.serialize(), favorites)) 
        
        return favorites_list