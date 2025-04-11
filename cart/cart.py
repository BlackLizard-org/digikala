from shop.models import Product, Profile
from decimal import Decimal


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')
        if not cart:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        if product_id in self.cart:
            self.cart[product_id] += int(quantity)
        else:
            self.cart[product_id] = int(quantity)
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            db_cart = str(self.cart).replace('\'', '\"')
            current_user.update(old_cart=str(db_cart))

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id] += int(quantity)
        else:
            self.cart[product_id] = int(quantity)
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            db_cart = str(self.cart).replace('\'', '\"')
            current_user.update(old_cart=str(db_cart))

    def __len__(self):
        return sum(self.cart.values())

    def get_prods(self):
        product_ids = self.cart.keys()
        return Product.objects.filter(id__in=product_ids)

    def get_quants(self):
        return {product_id: quantity for product_id, quantity in self.cart.items()}

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        ourcart = self.cart
        ourcart[product_id] = product_qty
        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            db_cart = str(self.cart).replace('\'', '\"')
            current_user.update(old_cart=str(db_cart))
        return self.cart

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            db_cart = str(self.cart).replace('\'', '\"')
            current_user.update(old_cart=str(db_cart))

    def get_quants(self):
        quatities = self.cart
        return quatities

    # def get_total(self):
    #     product_ids = self.cart.keys()
    #     products = Product.objects.filter(id__in=product_ids)
    #     total = 0
    #     for key, value in self.cart.items():
    #         key = int(key)
    #         for product in products:
    #             if product.id == key:
    #                 if product.is_sale:
    #                     total = total + (product.sale_price * value)
    #                 else:
    #                     total = total + (product.price * value)
    #
    #     return total
    def get_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        total = Decimal('0.00')

        for key, value in self.cart.items():
            try:
                quantity = Decimal(value)
            except:
                quantity = Decimal('1')

            product_id = int(key)
            for product in products:
                if product.id == product_id:
                    if product.is_sale:
                        total += product.sale_price * quantity
                    else:
                        total += product.price * quantity

        return total
