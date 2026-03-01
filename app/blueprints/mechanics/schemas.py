from app.extensions import ma
from app.models import Mechanic
from marshmallow import fields

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    service_ticket_ids = fields.Method("get_service_ticket_ids")  # Show assigned ticket IDs
    
    def get_service_ticket_ids(self, obj):
        return [ticket.id for ticket in obj.service_tickets]
    
    class Meta:
        model = Mechanic
        include_fk=True

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)