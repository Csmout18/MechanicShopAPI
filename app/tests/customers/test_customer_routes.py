from app import create_app
from app.models import db
import unittest
import json


class TestCustomerRoutes(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.app = create_app("TestingConfig")
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_customer(self):
        """Test POST /customers/ - Create customer"""
        customer_data = {
            "name": "John Doe",
            "email": "john@email.com",
            "phone": "555-123-4567",
            "password": "password123"
        }
        
        response = self.client.post('/customers/', json=customer_data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")
        self.assertEqual(response.json['email'], "john@email.com")

    def test_login_customer(self):
        """Test POST /customers/login - Customer login"""
        # Create customer first
        customer_data = {
            "name": "John Doe",
            "email": "john@email.com",
            "phone": "555-123-4567",
            "password": "password123"
        }
        self.client.post('/customers/', json=customer_data)
        
        # Login
        login_data = {
            "email": "john@email.com",
            "password": "password123"
        }
        response = self.client.post('/customers/login', json=login_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)

    def test_get_all_customers(self):
        """Test GET /customers/ - Get all customers"""
        response = self.client.get('/customers/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_customer_by_id(self):
        """Test GET /customers/<id> - Get customer by ID"""
        # Create customer first
        customer_data = {
            "name": "John Doe",
            "email": "john@email.com",
            "phone": "555-123-4567",
            "password": "password123"
        }
        create_response = self.client.post('/customers/', json=customer_data)
        customer_id = create_response.json['id']
        
        # Get by ID
        response = self.client.get(f'/customers/{customer_id}')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "John Doe")

    def test_update_customer(self):
        """Test PUT /customers/ - Update customer (requires authentication)"""
        # Create customer
        customer_data = {
            "name": "John Doe",
            "email": "john@email.com",
            "phone": "555-123-4567",
            "password": "password123"
        }
        self.client.post('/customers/', json=customer_data)
        
        # Login to get token
        login_data = {"email": "john@email.com", "password": "password123"}
        login_response = self.client.post('/customers/login', json=login_data)
        token = login_response.json['token']
        
        # Update customer
        update_data = {
            "name": "John Updated",
            "email": "john.updated@email.com",
            "phone": "555-999-8888",
            "password": "newpassword"
        }
        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.put('/customers/', json=update_data, headers=headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "John Updated")

    def test_delete_customer(self):
        """Test DELETE /customers/ - Delete customer (requires authentication)"""
        # Create customer
        customer_data = {
            "name": "John Doe",
            "email": "john@email.com",
            "phone": "555-123-4567",
            "password": "password123"
        }
        self.client.post('/customers/', json=customer_data)
        
        # Login to get token
        login_data = {"email": "john@email.com", "password": "password123"}
        login_response = self.client.post('/customers/login', json=login_data)
        token = login_response.json['token']
        
        # Delete customer
        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.delete('/customers/', headers=headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('deleted successfully', response.json['message'])


if __name__ == '__main__':
    unittest.main()