from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)   #nullable el espacio no puede quedar vacio
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
           # "username": self.username,
            "id": self.id,
            "email": self.email
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)   #nullable el espacio no puede quedar vacio
    mass = db.Column(db.String(80), unique=False, nullable=False)
    height = db.Column(db.String(80), unique=False, nullable=False)
    hair_color = db.Column(db.String(50), unique=False, nullable=False)
    skin_color = db.Column(db.String(60), unique=False, nullable=False)
    eye_color = db.Column(db.String(80), unique=False, nullable=False)
    birth_year = db.Column(db.String(80), unique=False, nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=False)

    
    def __repr__(self):
        return '<Characters %r>' % self.username

    def serialize(self):
        return {
            "name": self.name,
            "id": self.id,
            "height": self.height,
            "mass": self.mass ,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender
            
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)   #nullable el espacio no puede quedar vacio
    climate = db.Column(db.String(80), unique=False, nullable=False)
    created = db.Column(db.String(80), unique=False, nullable=False)
    gravity = db.Column(db.String(60), unique=False, nullable=False)
    orbital_period= db.Column(db.String(80), unique=False, nullable=False)
    population = db.Column(db.String(80), unique=False, nullable=False)
    rotation_period = db.Column(db.String(80), unique=False, nullable=False)
    surface_water = db.Column(db.String(80), unique=False, nullable=False)
    terrain = db.Column(db.String(80), unique=False, nullable=False)

    
    def __repr__(self):
        return '<Planets %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "created": self.created,
            "gravity ": self. gravity  ,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "rotation_period": self.rotation_period,
            "surface_water ": self.surface_water ,
            "terrain": self.terrain
            
            # do not serialize the password, its a security breach
        }


class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    favorito_id = db.Column(db.Integer, unique=True, nullable=False)   #nullable el espacio no puede quedar vacio
    tipo = db.Column(db.Integer, unique=False, nullable=False)
    # usuario_id= db.Column(db.Integer,db.ForeignKey("user.id"))

    def __repr__(self):
        return '<Favorites %r>' % self.name

    def serialize(self):
        return {
           # "username": self.username,
            "tipo": self.tipo,
            "favorito_id ": self.favorito_id,
            "id": self.id

            
            # do not serialize the password, its a security breach
        }

   



    
  








