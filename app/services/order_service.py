from app.models import Order, OrderItem, Product, Cart, db
from flask import jsonify

class OrderService:
    @staticmethod
    def place_order(user_id):
        try:
            # Buscar itens do carrinho do usuário
            cart_items = Cart.query.filter_by(user_id=user_id).all()
            if not cart_items:
                return {"message": "Cart is empty"}, 404

            # Calcular o preço total
            total_price = sum(item.quantity * item.product.price for item in cart_items)

            # Criar um novo pedido
            order = Order(user_id=user_id, total=total_price)
            db.session.add(order)
            db.session.commit()

            # Adicionar itens ao pedido
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

                # Atualizar o estoque do produto
                product.stock -= item.quantity
                db.session.add(product)

            # Limpar o carrinho
            Cart.query.filter_by(user_id=user_id).delete()
            db.session.commit()

            return {"message": "Order placed successfully!", "order_id": order.id}, 200
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()  # Reverter qualquer alteração em caso de erro
            return {"message": "Failed to place order"}, 500
