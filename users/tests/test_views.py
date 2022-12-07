from rest_framework.test import APITestCase
from users.models import User


class UsersViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.seller_data = {
            "username": "vendedor",
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
        cls.seller_wrong_key_data = {

        }
        cls.not_seller_wrong_key_data = {

        }
        cls.seller_login = {
            "username":"vendedor",
            "password":"1234"
        }
        cls.not_seller_login = {
            "username": "not-vendedor",
            "password": "1234"
        }
        cls.adm_data = {
            "username":"adrieldev",
            "password":"1234",
            "first_name":"adriel",
            "last_name":"alberto"
        }
        cls.adm_login = {
            "username":"adrieldev",
            "password":"1234"
        }

    def test_can_create_seller_account(self):
        response = self.client.post('/api/accounts/',self.seller_data)
        users_length = User.objects.count()
        user = response.data
        self.assertEqual(user['username'],'vendedor')
        self.assertFalse(user['is_superuser'])
        self.assertTrue(user['is_seller'])
        self.assertEqual(users_length,1)
        self.assertEqual(response.status_code,201)

    def test_can_create_not_seller_account(self):
        response = self.client.post('/api/accounts/',self.not_seller_data)
        users_length = User.objects.count()
        user = response.data
        self.assertFalse(user['is_seller'])
        self.assertEqual(users_length,1)
        self.assertEqual(response.status_code,201)
    
    def test_wrong_keys_seller_account(self):
        response = self.client.post('/api/accounts/',self.seller_wrong_key_data)
        self.assertEqual(response.status_code,400)

    def test_wrong_keys_not_seller_account(self):
        response = self.client.post('/api/accounts/',self.not_seller_wrong_key_data)
        self.assertEqual(response.status_code,400)
    
    def test_login_seller(self):
       
        self.client.post('/api/accounts/',self.seller_data)
        response = self.client.post('/api/login/',self.seller_login)
        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(response.data['token'])

    def test_login_not_seller(self):
         self.client.post('/api/accounts/',self.not_seller_data)
         response = self.client.post('/api/login/',self.not_seller_login)
         self.assertEqual(response.status_code,200)
         self.assertIsNotNone(response.data['token'])

    def test_owner_account_can_update(self):
        client = self.client.post('/api/accounts/',self.seller_data)
        id = client.data['id']
        token = self.client.post('/api/login/',self.seller_login)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.data['token'])
        response = self.client.patch(f'/api/accounts/{id}/',{"username":"vendedor-patch"})
        self.assertEqual(response.data['username'],'vendedor-patch')

    def test_cannot_update_account_without_token(self):
        client = self.client.post('/api/accounts/',self.seller_data)
        id = client.data['id']
        response = self.client.patch(f'/api/accounts/{id}/',{"username":"vendedor-patch"})
        self.assertEqual(response.status_code,401)
    
    def test_cannot_update_account_without_being_its_owner(self):
        seller = self.client.post('/api/accounts/',self.seller_data)
        self.client.post('/api/accounts/',self.not_seller_data)
        id = seller.data['id']
        login_not_seller = self.client.post('/api/login/',self.not_seller_login)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_not_seller.data['token'])
        response = self.client.patch(f'/api/accounts/{id}/',{"username":"vendedor-patch"})
        self.assertEqual(response.status_code,403)


    def test_adm_can_update_is_active_and_reactive(self):
        user = self.client.post('/api/accounts/',self.seller_data)
        id = user.data['id']
        User.objects.create_superuser(**self.adm_data)
        login_adm = self.client.post('/api/login/',self.adm_login)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_adm.data['token'])
        # setting to false
        update_user_to_is_active_false = self.client.patch(f'/api/accounts/{id}/management/')
        self.assertFalse(update_user_to_is_active_false.data['is_active'])
        # setting to true
        update_user_to_is_active_true = self.client.patch(f'/api/accounts/{id}/management/')
        self.assertTrue(update_user_to_is_active_true.data['is_active'])

    def test_user_cannot_update_is_active(self):
        user = self.client.post('/api/accounts/',self.seller_data)
        id = user.data['id']
        login_user = self.client.post('/api/login/',self.seller_login)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_user.data['token'])
        
        # usando a rota /management que é a ideal para soft delete temos 403
        update_user_to_is_active= self.client.patch(f'/api/accounts/{id}/management/')
        self.assertEqual(update_user_to_is_active.status_code,403)

        # usando a rota /patch usual não veremos mudança no is_active
        update_user_to_is_active = self.client.patch(f'/api/accounts/{id}/',{"is_active":False})
        self.assertTrue(update_user_to_is_active.data['is_active'])

    def test_anyone_can_list_accounts(self):
        self.client.post('/api/accounts/',self.seller_data)
        response = self.client.get('/api/accounts/')
        self.assertEqual(len(response.data['results']),1)