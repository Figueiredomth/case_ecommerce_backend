from app.models import Order, OrderItem, Product, Cart, db
from flask import jsonify

class OrderService:
    @staticmethod
    def place_order(user_id):
        try:
            # Search for user itens in cart
            cart_items = Cart.query.filter_by(user_id=user_id).all()
            if not cart_items:
                return {"message": "Cart is empty"}, 404

            # Calculate the total price
            total_price = sum(item.quantity * item.product.price for item in cart_items)

            # Create a new order
            order = Order(user_id=user_id, total=total_price)
            db.session.add(order)
            db.session.commit()

            # add item on the order
            for item in cart_items:
                product = Product.query.get(item.product_id)
                if product is None:
                    return {"message": f"Product with ID {item.product_id} not found"}, 404

                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=product.price
                )
                db.session.add(order_item)

                # Update the stock 
                product.stock -= item.quantity
                db.session.add(product)

            # clean the cart
            Cart.query.filter_by(user_id=user_id).delete()
            db.session.commit()

            return {"message": "Order placed successfully!", "order_id": order.id}, 200
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()  # Rollback if error
            return {"message": "Failed to place order"}, 500
