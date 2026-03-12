from app import create_app
from app.models import db
import unittest


class TestMechanicRoutes(unittest.TestCase):
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

    def test_create_mechanic(self):
        """Test POST /mechanics/ - Create mechanic"""
        mechanic_data = {
            "name": "John Mechanic",
            "email": "john@shop.com",
            "phone": "555-123-4567",
            "salary": 75000.00
        }
        
        response = self.client.post('/mechanics/', json=mechanic_data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Mechanic")
        self.assertEqual(response.json['salary'], 75000.00)

    def test_get_all_mechanics(self):
        """Test GET /mechanics/ - Get all mechanics"""
        response = self.client.get('/mechanics/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_mechanic_by_id(self):
        """Test GET /mechanics/<id> - Get mechanic by ID"""
        # Create mechanic first
        mechanic_data = {
            "name": "John Mechanic",
            "email": "john@shop.com",
            "phone": "555-123-4567",
            "salary": 75000.00
        }
        create_response = self.client.post('/mechanics/', json=mechanic_data)
        mechanic_id = create_response.json['id']
        
        # Get by ID
        response = self.client.get(f'/mechanics/{mechanic_id}')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "John Mechanic")

    def test_update_mechanic(self):
        """Test PUT /mechanics/<id> - Update mechanic"""
        # Create mechanic first
        mechanic_data = {
            "name": "John Mechanic",
            "email": "john@shop.com",
            "phone": "555-123-4567",
            "salary": 75000.00
        }
        create_response = self.client.post('/mechanics/', json=mechanic_data)
        mechanic_id = create_response.json['id']
        
        # Update mechanic
        update_data = {
            "name": "John Updated",
            "email": "john.updated@shop.com",
            "phone": "555-999-8888",
            "salary": 80000.00
        }
        response = self.client.put(f'/mechanics/{mechanic_id}', json=update_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "John Updated")
        self.assertEqual(response.json['salary'], 80000.00)

    def test_delete_mechanic(self):
        """Test DELETE /mechanics/<id> - Delete mechanic"""
        # Create mechanic first
        mechanic_data = {
            "name": "John Mechanic",
            "email": "john@shop.com",
            "phone": "555-123-4567",
            "salary": 75000.00
        }
        create_response = self.client.post('/mechanics/', json=mechanic_data)
        mechanic_id = create_response.json['id']
        
        # Delete mechanic
        response = self.client.delete(f'/mechanics/{mechanic_id}')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('deleted successfully', response.json['message'])

    def test_search_mechanics(self):
        """Test GET /mechanics/search - Search mechanics by name"""
        # Create mechanic first
        mechanic_data = {
            "name": "John Mechanic",
            "email": "john@shop.com",
            "phone": "555-123-4567",
            "salary": 75000.00
        }
        self.client.post('/mechanics/', json=mechanic_data)
        
        # Search for mechanic
        response = self.client.get('/mechanics/search?name=John')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['name'], "John Mechanic")


if __name__ == '__main__':
    unittest.main()