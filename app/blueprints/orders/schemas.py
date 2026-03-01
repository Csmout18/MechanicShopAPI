from app.extensions import ma
from app.models import ServiceTicket, ServiceTicketParts, Part
from marshmallow import fields

class ReceiptSchema(ma.SQLAlchemyAutoSchema):
    '''
    {
    total: 75.00
    service_ticket: {
        id: 1,
        VIN: "1HGCM82633A123456",
        service_date: "2024-06-01",
        service_desc: "Oil change and brake inspection",
        customer_id: 1,
        service_ticket_parts: [
            {
                part: {part_name: "Brake Pad", price: 50.00},
                quantity: 2       
            },
            {
                part: {part_name: "Oil Filter", price: 25.00},
                quantity: 1       
            }
            ]
            }
        }
    '''
    total = fields.Int(required=True)
    service_ticket = fields.Nested('ServiceTicketReceiptSchema')


class ServiceTicketReceiptSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        include_relationships = True
    service_ticket_parts = fields.Nested('ServiceTicketPartSchema', exclude=['id'], many=True)
    
class ServiceTicketPartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicketParts
    part = fields.Nested('PartReceiptSchema', exclude=['id'])

class PartReceiptSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Part

class AddPartsToServiceTicketSchema(ma.Schema):
    '''
    {
        part_quantity: [{part_id: "1", quantity: 2}]
    }
    '''
    part_quant = fields.Nested('PartQuantSchema', many=True)
    
class PartQuantSchema(ma.Schema):
    part_id = fields.Int(required=True)
    part_quant = fields.Int(required=True)    

service_ticket_receipt_schema = ServiceTicketReceiptSchema()
service_tickets_receipt_schema = ServiceTicketReceiptSchema(many=True)
add_parts_schema = AddPartsToServiceTicketSchema()
receipt_schema = ReceiptSchema()


