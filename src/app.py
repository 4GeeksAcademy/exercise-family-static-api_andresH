"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()

    if members:
        response_body = {"family": members}
        return jsonify(response_body), 200
    else:
        return {'message_error': 'Error en la solicitud'}


# metodo get  por id
@app.route('/members/<int:member_id>', methods=['GET'])
def get_members_id(member_id):
    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.get_member(member_id)
    
    if member:
        return jsonify(member), 200
    else: 
        return jsonify({
            'message_error': 'member not found'
        }), 400


#Metodo post crea member
@app.route('/member', methods=['POST'])
def add_member():
    
    request_data = request.get_json()
    
    new_member = {
    "first_name": request_data['first_name'],
    "last_name": jackson_family.last_name, 
    "age": request_data['age'],
    "lucky_numbers": request_data['lucky_numbers'],
    "id": jackson_family._generateId()
    }

    if request_data is None:
        return "El cuerpo de la solicitud es null", 400
    if 'first_name' not in request_data:
        return 'Debes especificar first_name', 400
    if 'age' not in request_data:
        return 'Debes especificar age', 400
    if 'lucky_numbers' not in request_data:
        return 'Debes especificar lucky_numbers', 400
        
    jackson_family.add_member(new_member)

    return "ok", 200
        
        
 
#Metodo Delete por id
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member_id(member_id):
    jackson_family.delete_member(member_id)
    return jsonify({'status_code': 200}), 400
 


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)


