from rest_framework.test import APITestCase
from users.models import User
from products.models import Product

class ProductViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.seller_data = {
            "username": "vendedor",
            "password": "1234",
            "first_name": "vendedor",
            "last_name": "vendedor",
            "is_seller": True,
            }
        cls.seller_data_two = {
            "username": "vendedor-2",
            "password": "1234",
            "first_name": "vendedor",
            "last_name": "vendedor",
            "is_seller": True,
        }
        cls.not_seller_data = {
            "username": "not-vendedor",
            "password": "1234",
            "first_name": "not-vendedor",
            "last_name": "not-vendedor",
            "is_seller": False,
        }

        cls.seller_login = {
            "username":"vendedor",
            "password":"1234"
        }
        cls.seller_two_login = {
            "username":"vendedor-2",
            "password":"1234"
        }
        cls.not_seller_login = {
            "username": "not-vendedor",
            "password": "1234"
        }

        cls.product_data = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": 15
            }
        cls.wrong_product = {}

        cls.product_with_negative_quantity = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": -2          
        }
        

    def test_only_seller_can_create_product(self):
        
        self.client.post('/api/accounts/',self.seller_data)
        login_seller = self.client.post('/api/login/',self.seller_login)
        # credenciais do vendedor criado acima
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_seller.data['token'])
        product_response = self.client.post('/api/products/',self.product_data)
        
        self.assertEqual(product_response.status_code,201)
        self.assertEqual(product_response.data['description'],"Smartband XYZ 3.0")

        # tentando criar agora com um not seller
        self.client.post('/api/accounts/',self.not_seller_data)
        login_not_seller = self.client.post('/api/login/',self.not_seller_login)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_not_seller.data['token'])
        product_response = self.client.post('/api/products/',self.product_data)
        self.assertEqual(product_response.status_code,403)


    def test_only_owner_can_update_product(self):
        # criando vendedor 1 ,produto do vendedor 1 e atualizando-o
        self.client.post('/api/accounts/',self.seller_data)
        login_seller = self.client.post('/api/login/',self.seller_login)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_seller.data['token'])
        product_response = self.client.post('/api/products/',self.product_data)
        product_patch_seller_one = self.client.patch(f"/api/products/{product_response.data['id']}/",{"description":"patch one"})
        self.assertEqual(product_patch_seller_one.data['description'],'patch one')


        # criando vendedor 2, setando token dele na autorização e tentando atualizalo
        self.client.post('/api/accounts/',self.seller_data_two)
        login_seller_two = self.client.post('/api/login/',self.seller_two_login)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_seller_two.data['token'])
        product_patch_seller_two = self.client.patch(f"/api/products/{product_response.data['id']}/",{"description":"patch dois"})
        self.assertEqual(product_patch_seller_two.status_code,403)

    def test_anyone_can_list_products(self):
        self.client.post('/api/accounts/',self.seller_data)
        login_seller = self.client.post('/api/login/',self.seller_login)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_seller.data['token'])
        product = self.client.post('/api/products/',self.product_data)
        
        # listando todos produtos
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data['results']),1)

        # listando produto especifico

        response = self.client.get(f'/api/products/{product.data["id"]}/')
        self.assertEqual(response.status_code,200)

    def test_different_response_get_and_create(self):
        # produto criado
        self.client.post('/api/accounts/',self.seller_data)
        login_seller = self.client.post('/api/login/',self.seller_login)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_seller.data['token'])
        product = self.client.post('/api/products/',self.product_data)

        # produto listado

        product_listed = self.client.get(f'/api/products/{product.data["id"]}/')
        self.assertNotEqual(product,product_listed)

    def test_wrong_keys(self):
        self.client.post('/api/accounts/',self.seller_data)
        login_seller = self.client.post('/api/login/',self.seller_login)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_seller.data['token'])
        response = self.client.post('/api/products/',self.wrong_product)

        self.assertEqual(response.status_code,400)
    
    def test_create_product_with_negative_quantity(self):
        self.client.post('/api/accounts/',self.seller_data)
        login_seller = self.client.post('/api/login/',self.seller_login)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_seller.data['token'])
        response = self.client.post('/api/products/',self.product_with_negative_quantity)
        self.assertEqual(response.status_code,400)
        


