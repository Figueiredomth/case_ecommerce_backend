from app.models import Cart, Product, db
from flask import session, jsonify

class CartService:
    @staticmethod
    def add_to_cart(user_id, product_id, quantity):
        # Ensure product ID is provided and quantity is greater than 0
        if not product_id or quantity <= 0:
            return {"message": "Product ID and valid quantity are required"}, 400

        # Retrieve the product from the database by ID
        product = Product.query.get(product_id)
        if not product:
            # Return error if the product is not found
            return {"message": "Product not found"}, 404

        # Check if there is enough stock for the requested quantity
        if product.stock < quantity:
            return {"message": "Not enough stock available"}, 400

        try:
            # Create a new cart item with the given product and quantity
            cart_item = Cart(user_id=user_id, product_id=product.id, quantity=quantity)
            db.session.add(cart_item)
            db.session.commit()  # Commit the cart item to the database
            return {"message": "Product added to cart successfully!"}, 201
        except Exception as e:
            print(f"Error: {e}")
            # Handle any errors that occur during the process
            return {"message": "Failed to add product to cart"}, 500

    @staticmethod
    def view_cart(user_id):
        try:
            # Retrieve all cart items for the given user from the database
            cart_items = Cart.query.filter_by(user_id=user_id).all()
            if not cart_items:
                # Return message if the cart is empty
                return {"message": "Cart is empty"}, 404

            # Create a list of items in the cart with product details and total price
            cart_list = [{
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price_per_item": item.product.price,
                "total_price": item.quantity * item.product.price
            } for item in cart_items]

            return {"items": cart_list}, 200
        except Exception as e:
            print(f"Error: {e}")
            # Handle errors during cart retrieval
            return {"message": "Failed to retrieve cart items"}, 500
