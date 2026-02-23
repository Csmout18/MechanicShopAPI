from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import ServiceTicket, db
from . import service_tickets_bp
from app.models import Mechanic

# ===== SERVICE TICKET ROUTES ===== #

# CREATE SERVICE TICKET
@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    try:
        ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_ticket = ServiceTicket(**ticket_data)
    db.session.add(new_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_ticket), 201

#GET ALL SERVICE TICKETS
@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    query = select(ServiceTicket)
    tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(tickets), 200

# Assign mechanic to a service ticket
@service_tickets_bp.route('/<int:service_ticket_id>/assign_mechanic/<int:mechanic_id>', methods=['PUT'])
def add_mechanic_to_ticket(service_ticket_id, mechanic_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not service_ticket or not mechanic:
        return jsonify({'message': 'Invalid service ticket id or mechanic id'}), 400
    
    # Check if mechanic is already assigned to the ticket
    if mechanic in service_ticket.mechanics:
        return jsonify({'message': 'Mechanic already assigned to this ticket'}), 409
    
    service_ticket.mechanics.append(mechanic)
    db.session.commit()
    
    return service_ticket_schema.jsonify(service_ticket), 200
    
# Remove mechanic from a ticket
@service_tickets_bp.route('/<int:service_ticket_id>/remove_mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic_from_ticket(service_ticket_id, mechanic_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not service_ticket or not mechanic:
        return jsonify({'message': 'Invalid service ticket id or mechanic id'}), 400

    # Check if mechanic is on the ticket
    if mechanic not in service_ticket.mechanics:
        return jsonify({'message': 'Mechanic not found on this ticket'}), 404
    
    service_ticket.mechanics.remove(mechanic)
    db.session.commit()
    
    return service_ticket_schema.jsonify(service_ticket), 200

