from re import S
from django.test import TestCase
from users.models import User
from products.models import Product


class ProductModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "username": "adrieldev",
            "password": "abcd",
            "first_name": "adriel",
            "last_name": "alberto",
            "is_seller": True,
            }
        cls.user = User.objects.create_user(**cls.user_data)
        cls.product_data = {
                "description": "Smartband XYZ 3.0",
                "price": 100.99,
                "quantity": 15,
                "seller":cls.user
                }
        cls.product = Product.objects.create(**cls.product_data)

    def test_description_max_length(self):
        max_length = self.product._meta.get_field('description').max_length
        self.assertEqual(max_length, 300)
    
    def test_price_max_digits(self):
        max_length = self.product._meta.get_field('price').max_digits
        self.assertEqual(max_length,10)
    
    def test_price_decimal_places(self):
        decimal_places = self.product._meta.get_field('price').decimal_places
        self.assertEqual(decimal_places,2)

    def test_description_not_null(self):
        self.assertIsNotNone(self.product._meta.get_field('description'))

    def test_price_not_null(self):
        self.assertIsNotNone(self.product._meta.get_field('price'))
    
    def test_quantity_not_null(self):
        self.assertIsNotNone(self.product._meta.get_field('quantity'))

    def test_is_active_not_null(self):
        self.assertIsNotNone(self.product._meta.get_field('is_active'))
    
    def test_seller_not_null(self):
        self.assertIsNotNone(self.product._meta.get_field('seller'))
    
    #relation tests
    def test_seller_owns_product(self):
        user = User.objects.get(id=self.product.seller.id)
        self.assertEqual(user,self.user)

    def test_seller_can_owns_many_products(self):
        product_two_data = {
                "description": "Smartband XYZ 3.0",
                "price": 100.99,
                "quantity": 15,
                "seller":self.user
                }
        product_two = Product.objects.create(**product_two_data)
        self.assertEqual(product_two.seller,self.product.seller)
    