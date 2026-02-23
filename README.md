MECHANIC SHOP API

Overview
--------
This is a REST API built with Flask for managing a mechanic shop. The API provides endpoints for managing customers, mechanics, and service tickets.

Technology Stack
----------------
- Flask (Python web framework)
- SQLAlchemy (Database ORM)
- MySQL (Database)
- Marshmallow (Data serialization and validation)
- Flask-SQLAlchemy (Flask-SQLAlchemy extension)

API Endpoints
-------------
The API is organized into three main blueprints:

/customers
- Manage customer information
- CREATE, READ, UPDATE, DELETE operations

/mechanics  
- Manage mechanic information
- CREATE, READ, UPDATE, DELETE operations

/service_tickets
- Manage service tickets/work orders
- CREATE, READ, UPDATE, DELETE operations

Setup Instructions
------------------
1. Install required dependencies:
   pip install -r requirements.txt

2. Configure database settings in config.py:
   - Update SQLALCHEMY_DATABASE_URI with your MySQL connection details
   - Note: Currently configured for MySQL database named 'library_db'

3. Initialize the database:
   python app.py
   (This will create all necessary tables)

4. Start the development server:
   python app.py
   (Server will run on debug mode by default)

Project Structure
-----------------
app.py              - Main application entry point
config.py           - Configuration settings  
requirements.txt    - Python dependencies
app/
  __init__.py       - Flask app factory
  models.py         - Database models
  extensions.py     - Flask extensions
  blueprints/       - API route blueprints
    customers/      - Customer management endpoints
    mechanics/      - Mechanic management endpoints  
    service_tickets/ - Service ticket endpoints

Development
-----------
The application uses Flask's development server with debug mode enabled.
Database tables are automatically created when the application starts.
All API endpoints support JSON request/response format.
