from flask import Flask
from models import db, User, Product, Order, init_db

app = Flask(__name__)

# Define a secret key to secure the session
app.secret_key = 'your_secret_key' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializing the databse
init_db(app)


if __name__ == '__main__':
    app.run(debug=True)
