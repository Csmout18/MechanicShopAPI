from app import create_app
from app.models import db
import unittest


class TestServiceTicketRoutes(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.app = create_app("TestingConfig")
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()
        
        # Create test customer for service tickets
        customer_data = {
            "name": "John Customer",
            "email": "john@email.com",
            "phone": "555-123-4567", 
            "password": "password123"
        }
        customer_response = self.client.post('/customers/', json=customer_data)
        self.test_customer_id = customer_response.json['id']

    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_service_ticket(self):
        """Test POST /service_tickets/ - Create service ticket"""
        ticket_data = {
            "VIN": "1HGBH41JXMN109186",
            "service_date": "2024-03-15",
            "service_desc": "Oil change and inspection",
            "customer_id": self.test_customer_id
        }
        
        response = self.client.post('/service_tickets/', json=ticket_data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['VIN'], "1HGBH41JXMN109186")
        self.assertEqual(response.json['service_desc'], "Oil change and inspection")

    def test_get_customer_tickets(self):
        """Test GET /service_tickets/my-tickets - Get customer's tickets (requires auth)"""
        # Create service ticket
        ticket_data = {
            "VIN": "1HGBH41JXMN109186",
            "service_date": "2024-03-15",
            "service_desc": "Oil change",
            "customer_id": self.test_customer_id
        }
        self.client.post('/service_tickets/', json=ticket_data)
        
        # Login customer to get token
        login_data = {"email": "john@email.com", "password": "password123"}
        login_response = self.client.post('/customers/login', json=login_data)
        token = login_response.json['token']
        
        # Get customer's tickets
        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.get('/service_tickets/my-tickets', headers=headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_all_service_tickets(self):
        """Test GET /service_tickets/ - Get all service tickets"""
        response = self.client.get('/service_tickets/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_assign_customer_to_ticket(self):
        """Test PUT /service_tickets/<id>/assign_customer/<customer_id> - Assign customer to ticket"""
        # Create service ticket
        ticket_data = {
            "VIN": "1HGBH41JXMN109186",
            "service_date": "2024-03-15",
            "service_desc": "Brake repair",
            "customer_id": self.test_customer_id
        }
        ticket_response = self.client.post('/service_tickets/', json=ticket_data)
        ticket_id = ticket_response.json['id']
        
        # Create another customer
        customer2_data = {
            "name": "Jane Customer",
            "email": "jane@email.com",
            "phone": "555-987-6543",
            "password": "password456"
        }
        customer2_response = self.client.post('/customers/', json=customer2_data)
        customer2_id = customer2_response.json['id']
        
        # Assign new customer to ticket
        response = self.client.put(f'/service_tickets/{ticket_id}/assign_customer/{customer2_id}')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['customer_id'], customer2_id)

    def test_assign_mechanics_to_ticket(self):
        """Test PUT /service_tickets/<id> - Assign/unassign mechanics to ticket"""
        # Create service ticket
        ticket_data = {
            "VIN": "1HGBH41JXMN109186", 
            "service_date": "2024-03-15",
            "service_desc": "Engine repair",
            "customer_id": self.test_customer_id
        }
        ticket_response = self.client.post('/service_tickets/', json=ticket_data)
        ticket_id = ticket_response.json['id']
        
        # Create mechanic
        mechanic_data = {
            "name": "Mike Mechanic",
            "email": "mike@shop.com",
            "phone": "555-444-3333",
            "salary": 70000.00
        }
        mechanic_response = self.client.post('/mechanics/', json=mechanic_data)
        mechanic_id = mechanic_response.json['id']
        
        # Assign mechanic to ticket
        assign_data = {"add_mechanic_ids": [mechanic_id]}
        response = self.client.put(f'/service_tickets/{ticket_id}', json=assign_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(mechanic_id, response.json['mechanic_ids'])

    def test_get_mechanics_sorted_by_tickets(self):
        """Test GET /service_tickets/sorted-by-mechanics - Get mechanics sorted by ticket count"""
        response = self.client.get('/service_tickets/sorted-by-mechanics')
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)


if __name__ == '__main__':
    unittest.main()