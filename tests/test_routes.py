import pytest
from app import app
from models import db, User, Product, Order, init_db
from werkzeug.security import generate_password_hash


@pytest.fixture(scope='module')
def test_client():
    # Configure the app for testing and use SQLite as the test database
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Create a test client to simulate HTTP requests
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all() # Create the tables before the tests
        yield testing_client

    # # Remove all tables after each test
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
