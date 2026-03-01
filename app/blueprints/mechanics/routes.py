from .schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Mechanic, db
from app.blueprints.mechanics import mechanics_bp
from app.extensions import limiter, cache

# ===== MECHANIC ROUTES ===== #

# CREATE MECHANIC
@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Mechanic).where(Mechanic.email == mechanic_data['email'])
    existing_mechanic = db.session.execute(query).scalars().all()
    if existing_mechanic:
        return jsonify({'error': 'Email already associated with a mechanic account.'}), 400
    
    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

#GET ALL MECHANICS
@mechanics_bp.route('/', methods=['GET'])
@cache.cached(timeout=30) #this can reduce the load on the API by caching the data for the user

def get_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics), 200

#GET MECHANIC BY ID
@mechanics_bp.route('/<int:mechanic_id>', methods=['GET'])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if mechanic:
        return mechanic_schema.jsonify(mechanic), 200
    return jsonify({"error": "Mechanic not found"}), 404

#UPDATE MECHANIC
@mechanics_bp.route('/<int:mechanic_id>', methods=['PUT'])
@limiter.limit("5/day") #Limits this request to 5 times daily to prevent abuse of the endpoint

def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)
    
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

#DELETE MECHANIC
@mechanics_bp.route('/<int:mechanic_id>', methods=['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {mechanic_id} was deleted successfully"}), 200

#SEARCH MECHANICS BY NAME
@mechanics_bp.route('/search', methods=['GET'])
def search_mechanics():
    name = request.args.get("name")
    
    query = select(Mechanic).where(Mechanic.name.like(f'%{name}%'))
    mechanics = db.session.execute(query).scalars().all()
    
    return mechanics_schema.jsonify(mechanics), 200  