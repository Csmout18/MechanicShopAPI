from app.extensions import ma
from app.models import ServiceTicket
from marshmallow import fields

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema): 
    mechanic_ids = fields.Method("get_mechanic_ids")  # Custom field to show assigned mechanic IDs
    
    def get_mechanic_ids(self, obj):
        return [mechanic.id for mechanic in obj.mechanics]
    
    class Meta:
        model = ServiceTicket
        include_fk=True
        

class EditServiceTicketSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int())
    remove_mechanic_ids = fields.List(fields.Int())
    class Meta:
        fields = ("add_mechanic_ids", "remove_mechanic_ids")

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
edit_service_ticket_schema = EditServiceTicketSchema()