from django.test import TestCase
from users.models import User

class UserModelTest(TestCase):

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


    def test_username_not_null(self):
        self.assertIsNotNone(self.user._meta.get_field('username'))

    def test_seller_not_null(self):
        self.assertIsNotNone(self.user._meta.get_field('is_seller'))

    def test_date_joined_not_null(self):
        self.assertIsNotNone(self.user._meta.get_field('date_joined'))

    def test_password_is_not_null(self):
        self.assertIsNotNone(self.user._meta.get_field('password'))

    def test_first_name_max_length(self):
        max_length = self.user._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 50)

    def test_last_name_max_length(self):
        max_length = self.user._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 50)

    

    
    
    