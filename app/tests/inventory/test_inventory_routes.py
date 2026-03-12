from app import create_app
from app.models import db
import unittest


class TestInventoryRoutes(unittest.TestCase):
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

    def test_create_part(self):
        """Test POST /inventory/ - Create part"""
        part_data = {
            "part_name": "Brake Pads",
            "price": 89.99
        }
        
        response = self.client.post('/inventory/', json=part_data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['part_name'], "Brake Pads")
        self.assertEqual(response.json['price'], 89.99)

    def test_get_all_parts(self):
        """Test GET /inventory/ - Get all parts"""
        response = self.client.get('/inventory/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_part_by_id(self):
        """Test GET /inventory/<id> - Get part by ID"""
        # Create part first
        part_data = {
            "part_name": "Oil Filter",
            "price": 24.99
        }
        create_response = self.client.post('/inventory/', json=part_data)
        part_id = create_response.json['id']
        
        # Get by ID
        response = self.client.get(f'/inventory/{part_id}')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['part_name'], "Oil Filter")

    def test_update_part(self):
        """Test PUT /inventory/<id> - Update part"""
        # Create part first
        part_data = {
            "part_name": "Spark Plugs",
            "price": 15.99
        }
        create_response = self.client.post('/inventory/', json=part_data)
        part_id = create_response.json['id']
        
        # Update part
        update_data = {
            "part_name": "Premium Spark Plugs",
            "price": 25.99
        }
        response = self.client.put(f'/inventory/{part_id}', json=update_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['part_name'], "Premium Spark Plugs")
        self.assertEqual(response.json['price'], 25.99)

    def test_delete_part(self):
        """Test DELETE /inventory/<id> - Delete part"""
        # Create part first
        part_data = {
            "part_name": "Air Filter",
            "price": 19.99
        }
        create_response = self.client.post('/inventory/', json=part_data)
        part_id = create_response.json['id']
        
        # Delete part
        response = self.client.delete(f'/inventory/{part_id}')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('deleted successfully', response.json['message'])


if __name__ == '__main__':
    unittest.main()