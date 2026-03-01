from .schemas import part_schema, parts_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Part, db
from app.blueprints.inventory import inventory_bp

# ===== PART ROUTES ===== #

# CREATE PART
@inventory_bp.route('/', methods=['POST'])
def create_part():
    try:
        part_data = part_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Part).where(Part.part_name == part_data['part_name'])
    existing_part = db.session.execute(query).scalars().all()
    if existing_part:
        return jsonify({'error': 'This part already exists.'}), 400
    
    new_part = Part(part_name=part_data['part_name'], price=part_data['price'])
    
    db.session.add(new_part)
    db.session.commit()
    
    return part_schema.jsonify(new_part), 201

#GET ALL PARTS
@inventory_bp.route('/', methods=['GET'])
# @cache.cached(timeout=30)
def get_parts():
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Part)
        parts = db.paginate(query, page=page, per_page=per_page)
        return parts_schema.jsonify(parts), 200
    except:
        query = select(Part)
    parts = db.session.execute(query).scalars().all()
    return parts_schema.jsonify(parts), 200

#GET PART BY ID
@inventory_bp.route('/<int:part_id>', methods=['GET'])
def get_part(part_id):
    part = db.session.get(Part, part_id)
    
    if part:
        return part_schema.jsonify(part), 200
    return jsonify({"error": "Part not found"}), 404

#UPDATE PART
@inventory_bp.route('/<int:part_id>', methods=['PUT'])
def update_part(part_id):
    part = db.session.get(Part, part_id)
    
    if not part:
        return jsonify({"error": "Part not found"}), 404
    try:
        part_data = part_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    for key, value in part_data.items():
        setattr(part, key, value)
    
    db.session.commit()
    return part_schema.jsonify(part), 200

#DELETE PART
@inventory_bp.route('/<int:part_id>', methods=['DELETE'])
def delete_part(part_id):
    part = db.session.get(Part, part_id)
    
    if not part:
        return jsonify({"error": "part not found"}), 404
    
    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": f"Part {part_id} was deleted successfully"}), 200

