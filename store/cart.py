from decimal import Decimal

from store.models import Product

CART_SESSION_KEY = 'cart'


class Cart:
    """Simple session-backed shopping cart: {product_id: {"quantity": int}}"""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if cart is None:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session[CART_SESSION_KEY] = {}
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = {str(p.id): p for p in Product.objects.filter(id__in=product_ids)}
        for product_id, item in self.cart.items():
            product = products.get(product_id)
            if product is None:
                continue
            unit_price = product.sale_price if product.is_sale and product.sale_price is not None else product.price
            quantity = item['quantity']
            yield {
                'product': product,
                'quantity': quantity,
                'unit_price': unit_price,
                'subtotal': unit_price * quantity,
            }

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum((item['subtotal'] for item in self), Decimal('0'))
