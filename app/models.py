from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy for database management
db = SQLAlchemy()

# User model for storing user information
class User(db.Model):
    __tablename__ = 'users'
    id =         db.Column(db.Integer, primary_key=True)                  # Primary key for user identification
    username =   db.Column(db.String(80), nullable=False, unique=True)    # Unique username
    password =   db.Column(db.String(128), nullable=False)                # Password storage
    is_admin =   db.Column(db.Boolean, default=False)                     # Indicates if the user is an admin
    
    # One-to-many relationship with Order and Cart models
    orders =     db.relationship('Order', backref='user', lazy=True)
    cart_items = db.relationship('Cart', backref='user', lazy=True)
    def __repr__(self):
        return f"<User {self.username}>"

# Product model for storing product information
class Product(db.Model):
    __tablename__ = 'products'
    id =           db.Column(db.Integer, primary_key=True)                 # Primary key for product identification
    name =         db.Column(db.String(100), nullable=False, unique=True)  # Product name
    description =  db.Column(db.String(150), nullable=False)               # Product description
    price =        db.Column(db.Float, nullable=False)                     # Product price
    stock =        db.Column(db.Integer, nullable=False)                   # Product stock quantity
    
    def __repr__(self):
        return f"<Product {self.name}>"

# Cart model for managing user cart items
class Cart(db.Model):
    __tablename__ = 'cart'
    id =         db.Column(db.Integer, primary_key=True)                              # Primary key for cart item identification
    user_id =    db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)     # Foreign key linking to the user
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  # Foreign key linking to the product
    quantity =   db.Column(db.Integer, nullable=False, default=1)                     # Quantity of the product in the cart
    product =    db.relationship('Product')                                           # Relationship to the Product model
    
    def __repr__(self):
        return f"<Cart Item: {self.quantity} of {self.product.name} for User {self.user_id}>"

# Order model for managing user orders
class Order(db.Model):
    __tablename__ = 'orders'
    id =          db.Column(db.Integer, primary_key=True)                           # Primary key for order identification
    user_id =     db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key linking to the user
    order_date =  db.Column(db.DateTime, nullable=False, default=datetime.utcnow)   # Order creation timestamp
    total =       db.Column(db.Float, nullable=False)                               # Total price of the order

    # One-to-many relationship with OrderItem model
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    
    def __repr__(self):
        return f"<Order {self.id} by User {self.user_id}>"

# OrderItem model for managing items within an order
class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id =         db.Column(db.Integer, primary_key=True)                              # Primary key for order item identification
    order_id =   db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)    # Foreign key linking to the order
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  # Foreign key linking to the product
    quantity =   db.Column(db.Integer, nullable=False)                                # Quantity of the product in the order
    price =      db.Column(db.Float, nullable=False)                                  # Price of the product at the time of order
    product =    db.relationship('Product')                                           # Relationship to the Product model
    
    def __repr__(self):
        return f"<OrderItem {self.quantity} of {self.product.name} in Order {self.order_id}>"
