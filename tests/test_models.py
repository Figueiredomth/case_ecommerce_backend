import pytest
from flask import Flask
from models import db, User, Product, Order, init_db
from datetime import datetime

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_ecommerce.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True  # Add the testing method
    init_db(app)

    with app.app_context():
        db.create_all()  # Create the tables before the tests

    yield app

    # Remove all tables after each test
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_user_model(app):
    with app.app_context():
        # create a new user
        new_user = User(username='testuser', password='hashedpassword')
        db.session.add(new_user)
        db.session.commit()
        
        # query the user
        user = User.query.filter_by(username='testuser').first()
        assert user is not None
        assert user.username == 'testuser'
        assert user.password == 'hashedpassword'

def test_product_model(app):
    with app.app_context():
        # create a new product
        new_product = Product(name='Test Product', price=10.0)
        db.session.add(new_product)
        db.session.commit()
        
        # query the product
        product = Product.query.filter_by(name='Test Product').first()
        assert product is not None
        assert product.name == 'Test Product'
        assert product.price == 10.0

def test_order_model(app):
    with app.app_context():
        # create a bew user and product for the order
        user = User(username='testuser', password='hashedpassword')
        product = Product(name='Test Product', price=10.0)
        db.session.add(user)
        db.session.add(product)
        db.session.commit()
        
        # create a new order
        new_order = Order(user_id=user.id, order_date=datetime.utcnow(), total=10.0)
        db.session.add(new_order)
        db.session.commit()
        
        # query the order
        order = Order.query.filter_by(user_id=user.id).first()
        assert order is not None
        assert order.user_id == user.id
        assert order.total == 10.0
