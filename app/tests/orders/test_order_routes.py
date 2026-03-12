from app import create_app
from app.models import db
import unittest


class TestOrderRoutes(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.app = create_app("TestingConfig")
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()
        
        # Create test customer
        customer_data = {
            "name": "John Customer",
            "email": "john@email.com",
            "phone": "555-123-4567",
            "password": "password123"
        }
        customer_response = self.client.post('/customers/', json=customer_data)
        self.test_customer_id = customer_response.json['id']
        
        # Create test service ticket
        ticket_data = {
            "VIN": "1HGBH41JXMN109186",
            "service_date": "2024-03-15",
            "service_desc": "Brake repair",
            "customer_id": self.test_customer_id
        }
        ticket_response = self.client.post('/service_tickets/', json=ticket_data)
        self.test_ticket_id = ticket_response.json['id']
        
        # Create test part
        part_data = {
            "part_name": "Brake Pads",
            "price": 75.99
        }
        part_response = self.client.post('/inventory/', json=part_data)
        self.test_part_id = part_response.json['id']

    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_parts_to_ticket(self):
        """Test POST /service_tickets/<ticket_id>/inventory - Add parts to service ticket"""
        order_data = {
            "part_quant": [
                {
                    "part_id": self.test_part_id,
                    "part_quant": 2
                }
            ]
        }
        
        response = self.client.post(f'/service_tickets/{self.test_ticket_id}/inventory', json=order_data)
        
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.json, dict)
        self.assertIn('total', response.json)

    def test_get_receipt(self):
        """Test GET /service_tickets/<ticket_id>/receipt - Get receipt for service ticket"""
        # First add some parts to the ticket
        order_data = {
            "part_quant": [
                {
                    "part_id": self.test_part_id,
                    "part_quant": 1
                }
            ]
        }
        self.client.post(f'/service_tickets/{self.test_ticket_id}/inventory', json=order_data)
        
        # Get the receipt
        response = self.client.get(f'/service_tickets/{self.test_ticket_id}/receipt')
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)
        self.assertIn('total', response.json)


if __name__ == '__main__':
    unittest.main()