import pytest
from app import create_app, db
from app.models import User, Product, Cart, Order, OrderItem

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Cria um usuário admin para os testes
            user = User(username='admin', password='admin123', is_admin=True)
            db.session.add(user)
            db.session.commit()
            
            # Cria um produto para os testes
            product = Product(name='Test Product', price=10.99, stock=100, description='Test description')
            db.session.add(product)
            db.session.commit()
        
        yield client
        
        with app.app_context():
            db.drop_all()

def simulate_user_session(client, user_id):
    with client.session_transaction() as session:
        session['user_id'] = user_id

def test_add_to_cart_service(client):
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


from app.models import Order, OrderItem, Product, Cart, db

def test_checkout(client):
    # Simula uma sessão de usuário
    simulate_user_session(client, user_id=1)
    
    # Adiciona um produto com todos os campos obrigatórios
    response = client.post('/products/add', json={
        'name': 'Test Product',
        'price': 10.99,
        'stock': 100,
        'description': 'Test description'
    })
    assert response.status_code == 201

    # Adiciona o produto ao carrinho
    response = client.post('/cart/add', json={
        'product_id': 1,  # Supondo que o produto adicionado tem ID 1
        'quantity': 2
    })
    assert response.status_code == 201

    # Realiza o checkout
    response = client.post('/orders/checkout')  # Atualizado para a rota correta
    assert response.status_code == 200
    response_json = response.get_json()

    assert response_json is not None, "Response JSON is None"
    assert response_json.get('message') == 'Order placed successfully!', "Unexpected message in response"

    # Verifica se o pedido foi realmente criado e o estoque foi atualizado
    order_id = response_json.get('order_id')
    assert order_id is not None, "Order ID not found in response"

    # Verifica se o pedido e os itens foram salvos no banco de dados
    order = Order.query.get(order_id)
    assert order is not None, "Order not found in database"
    assert order.user_id == 1, "Order user ID does not match"
    assert order.total == 21.98, "Total price does not match"

    order_items = OrderItem.query.filter_by(order_id=order_id).all()
    assert len(order_items) == 1, "Order items count does not match"
    assert order_items[0].product_id == 1, "Product ID in order item does not match"
    assert order_items[0].quantity == 2, "Quantity in order item does not match"

    # Verifica se o estoque do produto foi atualizado corretamente
    product = Product.query.get(1)
    assert product is not None, "Product not found in database"
    assert product.stock == 98, "Product stock was not updated correctly"

    # Verifica se o carrinho foi limpo
    cart_items = Cart.query.filter_by(user_id=1).all()
    assert len(cart_items) == 0, "Cart was not cleared after checkout"

