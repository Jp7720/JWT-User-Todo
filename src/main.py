"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for   #request permite  leer el request que viene del front    #jsonify                    #aquí importamos la librería Flask en nuestro archivo.
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Favorites
#from models import Person

from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
import datetime
app = Flask(__name__)#aquí creamos una nueva instancia del servidor Flask.
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

app.config["JWT_SECRET_KEY"] =" secret-key"
jwt=JWTManager(app)



# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)         
def handle_invalid_usage(error):       
    return jsonify(error.to_dict()), error.status_code   

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
#login---------------------------------------------------------
@app.route('/login', methods=["POST"])
def login():
    if request.method == "POST":
        username = request.json["email"]
        password = request.json["password"]

        # Validate
        if not username:
            return jsonify({"error": "username Invalid"}), 400
        if not password:
            return jsonify({"error": "Password Invalid"}), 400
        
        user = User.query.filter_by(email=username).first()

        # if not user:
        #     return jsonify({"error": "User not found"}), 400
        
        #if not check_password_hash(user.password, password):
        #    return jsonify({"error": "Wrong password"}), 400
        
        # Create Access Token
        expiration_date = datetime.timedelta(days=1)
        #expiration_date = datetime.timedelta(minutes=1)
        access_token = create_access_token(identity=username, expires_delta=expiration_date)

        request_body = {
            "user": user.serialize(),
            "token": access_token
        }

        return jsonify(request_body), 200    


@app.route('/user', methods=['GET'])  #aquí especificamos la ruta para el endpoint y especificamos que este endpoint acepta solicitudes GET
def handle_hello():                   #este método se llamará cuando el cliente haga el request
    people_query = User.query.all()
    all_people = list(map(lambda x: x.serialize(), people_query))
    return jsonify(all_people), 200 
    #request = list(map(lambda user:user.serialize(),user))    
    #return jsonify(request), 200

        
@app.route('/user/<int:id>', methods=['GET'])
def lista_usuario(id):
    #user = User.query.get(id)
    user = User.query.filter_by(id=id).first()
    if user is None:
        raise APIException("Message:No se encontro el user",status_code=404)
    request = user.serialize()
    return jsonify(request), 200

@app.route('/user', methods=["POST"])
def crear_usuarios():
    data = request.get_json()
    user1 = User(is_active=data["is_active"],email=data["email"],password=data["password"])
    db.session.add(user1)
    db.session.commit()
    return jsonify("Message : Se adiciono un usuario!"),200
    

@app.route('/user/<id>', methods=["PUT"])
def update_usuarios(id):
    request_body = request.get_json()
    user1 = User.query.get(id)
    if user1 is None:
        raise APIException("usuario no existe!", status_code=404)
    
    if "email" in request_body:
        user1.email = request_body["email"]
    db.session.commit()
    
    return jsonify("usuario Update, OK!"),200


@app.route('/user/<id>', methods=["DELETE"])
@jwt_required()
def delete_usuarios(id):
    current_user = get_jwt_identity()
    user1 = User.query.get(id)
    if user1 is None:
        raise APIException("usuario no existe!",status_code=404)
    db.session.delete(user1)
    db.session.commit()
    return jsonify({"Proceso realizado con exito por el usuario:" : current_user}),200
    #return jsonify("Registro eliminado,ok!"),200

#####################################################################################################
    
#                to do list
   
# @app.route('/todo', methods=['GET'])
# def listarTodos():
#     todos = Todo.query.all()
#     request = list(map(lambda todo:todo.serialize(),todo))    
#     return jsonify(request), 200

# @app.route('/todo/<int:id>', methods=['GET'])
# def listarItem(id):
#     #todo1 = Todo.query.get(id)
#     todo1 = Todo.query.filter_by(id=id).first()
#     if todo1 is None:
#         return APIException({"message": "No se encontro el item"},status_code=404)
#     request = todo1.serialize()
#     return jsonify(request), 200

# @app.route('/todo', methods=['POST'])
# def crearTodo():
#     return jsonify("Metodo Post"), 200

# @app.route('/todo', methods=['PUT'])
# def updateTodo():
#     return jsonify("Metodo PUT"), 200

# @app.route('/todo', methods=['DELETE'])
# def deleteTodo():
#     return jsonify("Metodo DELETE"), 200

########### characters ##############################
@app.route('/characters', methods=['GET'])  #aquí especificamos la ruta para el endpoint y especificamos que este endpoint acepta solicitudes GET
def getcharacters():                        #este método se llamará cuando el cliente haga el request
    personas = Characters.query.all()
    request = list(map(lambda x: x.serialize(), personas))
    return jsonify( request), 200 
    #request = list(map(lambda user:user.serialize(),user))    
    #return jsonify(request), 200

        
@app.route('/characters/<int:id>', methods=['GET'])
def list_characters(id):
    #user = User.query.get(id)
    characters= Characters.query.filter_by(id=id).first()
    if characters is None:
        raise APIException("Message:No se encontro el user",status_code=404)
    request = characters.serialize()
    return jsonify(request), 200

@app.route('/characters', methods=["POST"])
def crear_personajes():
    data = request.get_json()
    characters = Characters(name=data["name"],height=data["height"],mass=data["mass"],birth_year=data["birth_year"],
    hair_color=data["hair_color"],skin_color=data["skin_color"],eye_color=data["eye_color"],gender=data["gender"])
    db.session.add(characters)
    db.session.commit()
    return jsonify("Message : Se adiciono un usuario!"),200

@app.route('/charto', methods=["POST"])
def log():
    if request.method == "POST":
        name = request.json["name"]
        height = request.json["height"]
        mass = request.json["mass"]
        birth_year = request.json["birth_year"]
        hair_color = request.json["hair_color"]
        gender = request.json["gender"]
        skin_color = request.json["skin_color"]
        eye_color = request.json["eye_color"]

        # Validate
        if not name:
            return jsonify({"error": "username Invalid"}), 400
        if not height:
            return jsonify({"error": "Password Invalid"}), 400
        if not mass:
            return jsonify({"error": "mass Invalid"}), 400
        if not birth_year:
            return jsonify({"error": "birth_year"}), 400
        if not hair_color:
            return jsonify({"error": "hair_color Invalid"}), 400
        if not gender:
            return jsonify({"error": "gender Invalid"}), 400
        if not skin_color:
            return jsonify({"error": "skin_color Invalid"}), 400
        if not eye_color:
            return jsonify({"error": "eye_color Invalid"}), 400
        
        characters = Characters.query.filter_by(name=name).first()

        # if not user:
        #     return jsonify({"error": "User not found"}), 400
        #if not check_password_hash(user.password, password):
        #    return jsonify({"error": "Wrong password"}), 400
        
        # Create Access Token
        expiration_date = datetime.timedelta(days=1)
        #expiration_date = datetime.timedelta(minutes=1)
        access_token = create_access_token(identity=name, expires_delta=expiration_date)
        request_body = {
            "characters": characters.serialize(),
            "token": access_token
        }
        return jsonify(request_body), 200

@app.route('/characters/<id>', methods=["PUT"])
@jwt_required()
def update_personajes(id):
    request_body = request.get_json()
    characters = Characters.query.get(id)
    if characters is None:
        raise APIException("usuario no existe!", status_code=404)
    
    if "mass" in request_body:
        characters.mass = request_body["mass"]
    if "name" in request_body:
        characters.name = request_body["name"]

    db.session.commit()
    
    return jsonify("usuario Update, OK!"),200

   




###########################################################################################################################################################################3



@app.route('/planets', methods=['GET'])  #aquí especificamos la ruta para el endpoint y especificamos que este endpoint acepta solicitudes GET
def getplanets():                   #este método se llamará cuando el cliente haga el request
    planetas = Planets.query.all()
    request = list(map(lambda x: x.serialize(), planetas))
    return jsonify(request), 200 
    #request = list(map(lambda user:user.serialize(),user))    
    #return jsonify(request), 

@app.route('/planets/<int:id>', methods=['GET'])
def list_planets(id):
    #user = User.query.get(id)
    planets= Planets.query.filter_by(id=id).first()
    if planets is None:
        raise APIException("Message:No se encontro el user",status_code=404)
    request = planets.serialize()
    return jsonify(request), 200










@app.route('/favorites', methods=['GET'])  #aquí especificamos la ruta para el endpoint y especificamos que este endpoint acepta solicitudes GET
def getFavorites():                   #este método se llamará cuando el cliente haga el request
    favoritos = Favorites.query.all()
    request = list(map(lambda x: x.serialize(), favoritos))
    return jsonify(request), 200 

@app.route('/favorites/<int:id>', methods=['GET'])
def list_favorites(id):
    #user = User.query.get(id)
    favorites= Favorites.query.filter_by(id=id).first()
    if favorites is None:
        raise APIException("Message:No se encontro el user",status_code=404)
    request = favorites.serialize()
    return jsonify(request), 200







# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)  #finalmente iniciamos el servidor en el localhost.
