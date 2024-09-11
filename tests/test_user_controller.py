import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_register(client):
    response = client.post('/user/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User registered successfully!'

def test_login(client):
    # Register user
    client.post('/user/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })

    response = client.post('/user/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    # Verifique se a mensagem de boas-vindas está presente
    assert 'Welcome back' in response.json['message']


def test_login_failure(client):
    response = client.post('/user/login', json={
        'username': 'nonexistentuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert response.json['message'] == 'Invalid username or password'
