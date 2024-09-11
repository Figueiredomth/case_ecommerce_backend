from flask                              import Flask
from app.models                         import db
from app.controllers.user_controller    import user_bp
from app.controllers.account_controller import account_bp
from app.controllers.product_controller import product_bp

def create_app():
    app = Flask(__name__)
    
    # Configures the SQLite database URI and disables modification tracking for performance
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Secret key for session management and security
    app.config['SECRET_KEY'] = 'your_secret_key'

    db.init_app(app)
    
    # Registers blueprints for modular controllers with specific URL prefixes
    app.register_blueprint(user_bp,     url_prefix= '/user')
    app.register_blueprint(account_bp,  url_prefix= '/account')
    app.register_blueprint(product_bp,  url_prefix= '/products')

   
    # Ensures the tables are created in the database when the app context is available
    with app.app_context():
        db.create_all()

    return app

# Main entry point for running the Flask application in debug mode
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
