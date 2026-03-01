from .schemas import add_parts_schema, receipt_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import ServiceTicket, ServiceTicketParts, db
from app.blueprints.orders import orders_bp

# ===== SERVICE TICKET PARTS ROUTES ===== #

# ADD PARTS TO SERVICE TICKET 
@orders_bp.route('/<int:service_ticket_id>/inventory', methods=['POST'])
def add_parts_to_service_ticket(service_ticket_id):

    service_ticket = db.session.get(ServiceTicket, service_ticket_id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    
    try:
        parts_data = add_parts_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for part_data in parts_data['part_quant']:
        service_ticket_part = ServiceTicketParts(
            service_ticket_id=service_ticket.id,
            part_id=part_data['part_id'],
            quantity=part_data['part_quant']
        )
        db.session.add(service_ticket_part)
        
    db.session.commit()
    
    total = 0 
    for service_ticket_part in service_ticket.service_ticket_parts:
        price = service_ticket_part.quantity * service_ticket_part.part.price 
        total += price
        
    receipt = {
        "total": total,
        "service_ticket": service_ticket
    }

    return receipt_schema.jsonify(receipt), 201

# GET PARTS RECEIPT FOR SERVICE TICKET
@orders_bp.route('/<int:service_ticket_id>/receipt', methods=['GET'])
def get_service_ticket_receipt(service_ticket_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)
    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    
    total = 0 
    for service_ticket_part in service_ticket.service_ticket_parts:
        price = service_ticket_part.quantity * service_ticket_part.part.price 
        total += price
        
    receipt = {
        "total": total,
        "service_ticket": service_ticket
    }

    return receipt_schema.jsonify(receipt), 200

