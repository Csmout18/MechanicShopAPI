from .schemas import service_ticket_schema, service_tickets_schema, edit_service_ticket_schema
from app.blueprints.mechanics.schemas import mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import ServiceTicket, Customer, Mechanic, db
from app.blueprints.service_tickets import service_tickets_bp 
from app.extensions import limiter, cache
from app.utils.util import token_required

# ===== SERVICE TICKET ROUTES ===== #

# CREATE SERVICE TICKET
@service_tickets_bp.route('/', methods=['POST'])
@limiter.limit("5/day") #Limits to 5 tickers per day to avoid spam tickets

def create_service_ticket():
    try:
        ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_ticket = ServiceTicket(**ticket_data)
    db.session.add(new_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_ticket), 201

# GET TICKETS FOR A SPECIFIC CUSTOMER WITH TOKEN AUTHORIZATION REQUIRED
@service_tickets_bp.route('/my-tickets', methods=['GET'])
@token_required
def get_customer_tickets(customer_id):
    customer = db.session.get(Customer, customer_id)
    
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    return service_tickets_schema.jsonify(customer.service_tickets), 200

#GET ALL SERVICE TICKETS
@service_tickets_bp.route('/', methods=['GET'])
@cache.cached(timeout=30) #this can reduce the load on the API by caching the data for the user
def get_service_tickets():
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(ServiceTicket)
        service_tickets = db.paginate(query, page=page, per_page=per_page)
        return service_tickets_schema.jsonify(service_tickets), 200   
    except:
        query = select(ServiceTicket)
    tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(tickets), 200

#ASSIGN TICKET TO CUSTOMER
@service_tickets_bp.route('/<int:service_ticket_id>/assign_customer/<int:customer_id>', methods=['PUT'])
def add_customer_to_ticket(service_ticket_id, customer_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)
    customer = db.session.get(Customer, customer_id)
    
    if not service_ticket or not customer:
        return jsonify({'message': 'Invalid service ticket id or customer id'}), 400
    
    if service_ticket.customer_id == customer_id:
        return jsonify({'message': 'Customer already assigned to this ticket'}), 409
    
    service_ticket.customer = customer 
    db.session.commit()
    
    return service_ticket_schema.jsonify(service_ticket), 200

# ASSIGN/UNASSIGN MECHANICS TO A SERVICE TICKET
@service_tickets_bp.route('/<int:service_ticket_id>', methods=['PUT'])
def edit_service_ticket(service_ticket_id):
    try:
        service_ticket_edits = edit_service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
        
    query = select(ServiceTicket).where(ServiceTicket.id == service_ticket_id)
    service_ticket = db.session.execute(query).scalars().first()
    
    if not service_ticket:
        return jsonify({'message': 'Service ticket not found'}), 404
    
    # Add mechanics
    for mechanic_id in service_ticket_edits.get('add_mechanic_ids', []):
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()
        
        if not mechanic:
            return jsonify({'message': f'Mechanic with ID {mechanic_id} not found'}), 404
        elif mechanic in service_ticket.mechanics:
            return jsonify({'message': f'Mechanic with ID {mechanic_id} is already assigned to this ticket'}), 409
        else:
            service_ticket.mechanics.append(mechanic)
            
    # Remove mechanics (optional field - only process if provided)
    remove_mechanic_ids = service_ticket_edits.get('remove_mechanic_ids', [])
    for mechanic_id in remove_mechanic_ids:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()
        
        if not mechanic:
            return jsonify({'message': f'Mechanic with ID {mechanic_id} not found'}), 404
        elif mechanic not in service_ticket.mechanics:
            return jsonify({'message': f'Mechanic with ID {mechanic_id} is not assigned to this ticket'}), 409
        else:
            service_ticket.mechanics.remove(mechanic)
            
    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200
            
# SORT MECHANICS BY NUMBER OF TICKETS ASSIGNED USING LAMBDA
@service_tickets_bp.route('/sorted-by-mechanics', methods=['GET'])
def get_mechanics_sorted_by_tickets():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    
    mechanics.sort(key = lambda mechanic: len(mechanic.service_tickets), reverse=True)
    
    return mechanics_schema.jsonify(mechanics), 200
