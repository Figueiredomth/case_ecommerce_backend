import pytest
from app import create_app, db
from app.models import User, Product

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create an admin user for the tests
            user = User(username='admin', password='admin123', is_admin=True)
            db.session.add(user)
            db.session.commit()

            # Create a product for the tests
            product = Product(name='Test Product', price=10.99, stock=100, description='Test description')
            db.session.add(product)
            db.session.commit()
            
            yield client
            db.drop_all()  # Clean up the database after tests


def simulate_user_session(client, user_id):
    with client.session_transaction() as session:
        session['user_id'] = user_id

def test_add_product(client):
    simulate_user_session(client, user_id=1)
    response = client.post('/products/add', json={
        'name': 'Test Product',
        'price': 10.99,
        'stock': 100,
        'description': 'Test description'  
    })
    assert response.status_code == 201
    response_json = response.get_json()
    assert response_json is not None, "Response JSON is None"
    assert response_json.get('message') == 'Product added successfully!'

def test_edit_product(client):
    simulate_user_session(client, user_id=1)
    response = client.put('/products/edit', json={
        'product_id': 1,
        'name': 'Updated Product',
        'price': 12.99,
        'stock': 150
    })
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json is not None, "Response JSON is None"
    assert response_json.get('message') == 'Product updated successfully!'

def test_delete_product(client):
    simulate_user_session(client, user_id=1)
    response = client.delete('/products/delete', json={'product_id': 1})
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json is not None, "Response JSON is None"
    assert response_json.get('message') == 'Product deleted successfully!'

def test_list_products(client):
    simulate_user_session(client, user_id=1)
    response = client.get('/products/list')
    assert response.status_code == 200
    response_json = response.get_json()                                    
    assert response_json is not None, "Response JSON is None"              # Check if response is not None
    assert isinstance(response_json, list), "Response JSON is not a list"  # Check if it is a list
    assert len(response_json) > 0, "Product list is empty"                 # Ensure list is not empty

def test_details_products(client):
    simulate_user_session(client, user_id=1)
    response = client.get('/products/details')
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json is not None, "Response JSON is None"
