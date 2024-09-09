import pytest
from app import app
from models import db, User, Product, Order, init_db
from werkzeug.security import generate_password_hash


@pytest.fixture(scope='module')
def test_client():
    # Configure the app for testing and use SQLite as the test database
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_ecommerce.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Create a test client to simulate HTTP requests
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all() # Create the tables before the tests
        yield testing_client

    # Remove all tables after each test
    with app.app_context():
        db.drop_all()

# Test for user registration
def test_register_user(test_client):
    response = test_client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 201
    assert b'User registered successfully!' in response.data

# Test for duplicate user registration
def test_register_user_duplicate(test_client):
    test_client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    response = test_client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 400
    assert b'User already exists' in response.data

# Test for missing required fields during registration
def test_register_user_missing_fields(test_client):
    response = test_client.post('/register', json={
        'username': 'testuser'
    })
    assert response.status_code == 400
    assert b'Username and password are required' in response.data


# Test for invalid fields during registration (username and password too short)
def test_register_user_invalid_fields(test_client):
    response = test_client.post('/register', json={
        'username': 'usr',  # Invalid username (less than 5 characters)
        'password': 'pwd'   # Invalid password (less than 8 characters)
    })
    assert response.status_code == 400
    assert b'Username must be at least 5 characters and password at least 8 characters' in response.data

# Test for adding a product as an admin
def test_add_product_admin(test_client):
    # First, register and login as admin
    test_client.post('/register', json={
        'username': 'adminuser',
        'password': 'adminpassword',
        'is_admin': True
    })
    login_response = test_client.post('/login', json={
        'username': 'adminuser',
        'password': 'adminpassword'
    })
    assert login_response.status_code == 200

    # Add a product
    response = test_client.post('/products', json={
        'name': 'Test Product',
        'description': 'A product for testing',
        'price': 19.99,
        'stock': 100
    })
    assert response.status_code == 201
    assert b'Product added successfully!' in response.data

# Test for adding a product with the same name
def test_add_product_duplicate_name(test_client):
    # Register and login as admin
    test_client.post('/register', json={
        'username': 'adminuser2',
        'password': 'adminpassword2',
        'is_admin': True
    })
    login_response = test_client.post('/login', json={
        'username': 'adminuser2',
        'password': 'adminpassword2'
    })
    assert login_response.status_code == 200

    # Add a product with a unique name
    test_client.post('/products', json={
        'name': 'Unique Product',
        'description': 'A product with a unique name',
        'price': 29.99,
        'stock': 50
    })

    # Try adding another product with the same name
    response = test_client.post('/products', json={
        'name': 'Unique Product',
        'description': 'Another product with the same name',
        'price': 39.99,
        'stock': 20
    })
    assert response.status_code == 400
    assert b'Product with this name already exists' in response.data

# Test for adding a product with invalid price
def test_add_product_invalid_price(test_client):
    # Register and login as admin
    test_client.post('/register', json={
        'username': 'adminuser3',
        'password': 'adminpassword3',
        'is_admin': True
    })
    login_response = test_client.post('/login', json={
        'username': 'adminuser3',
        'password': 'adminpassword3'
    })
    assert login_response.status_code == 200

    # Try adding a product with a negative price
    response = test_client.post('/products', json={
        'name': 'Invalid Price Product',
        'description': 'A product with invalid price',
        'price': -5.0, 
        'stock': 10
    })
    assert response.status_code == 400
    assert b'Price cannot be negative' in response.data

# Test for adding a product with invalid data type
def test_add_product_invalid_data_type(test_client):
    # Register and login as admin
    test_client.post('/register', json={
        'username': 'adminuser4',
        'password': 'adminpassword4',
        'is_admin': True
    })
    login_response = test_client.post('/login', json={
        'username': 'adminuser4',
        'password': 'adminpassword4'
    })
    assert login_response.status_code == 200

    # Try adding a product with a string as price
    response = test_client.post('/products', json={
        'name': 'Test Product with Invalid Price',
        'description': 'This product has an invalid price format',
        'price': 'invalid_price',
        'stock': 10
    })
    assert response.status_code == 400
    assert b'Invalid data type for price' in response.data

# Test for adding a product without admin privileges
def test_add_product_unauthorized(test_client):
    # Register and login as a regular user
    test_client.post('/register', json={
        'username': 'regularuser',
        'password': 'regularpassword'
    })
    login_response = test_client.post('/login', json={
        'username': 'regularuser',
        'password': 'regularpassword'
    })
    assert login_response.status_code == 200

    # Attempt to add a product
    response = test_client.post('/products', json={
        'name': 'Unauthorized Product',
        'description': 'A product from an unauthorized user',
        'price': 9.99,
        'stock': 10
    })
    assert response.status_code == 403
    assert b'Unauthorized access' in response.data

def test_add_product_no_authentication(test_client):
    # Tente adicionar um produto sem autenticação
    response = test_client.post('/products', json={
        'name': 'No Auth Product',
        'description': 'A product without authentication',
        'price': 10.0,
        'stock': 10
    })
    assert response.status_code == 401 
    assert b'Authentication required' in response.data


