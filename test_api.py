import unittest
import json
import unittest

from app import app
import config

app.config.from_object('config.TestingConfig')


class APITests(unittest.TestCase):
    """Tests all functionality of the API"""


    def setUp(self):
        """Initialize important variables and makes them easily availabe through the self keyword"""
        app.testing = True
        self.app = app.test_client()
        self.data = json.dumps({"username" : "balotelli", "email" : "balotelli@gmail.com",
                           "password" : "secret12345", "confirm_password" : "secret12345"})
        self.existing_user = self.app.post('/api/v1/auth/signup', data=self.data, content_type='application/json')
       
    def test_get_all_users(self):
        """Tests successfully getting all users through the users endpoint"""
        response = self.app.get('/api/v1/auth/signup')
        self.assertEqual(response.status_code, 200)

    def test_successful_user_creation(self):
        """Tests successfully creating a new user through the users endpoint"""
        data = json.dumps({"username" : "marcus", "email" : "marcusrahford@gmail.com",
                           "password" : "secret12345", "confirm_password" : "secret12345"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("username"), "marcus")
        self.assertEqual(result.get("email"), "marcusrahford@gmail.com")
        self.assertEqual(result.get("password"), "secret12345")
        self.assertEqual(response.status_code, 201)
    
    def test_create_user_using_existing_email(self):
        """Tests unsuccessfully creating a new user because of existing email"""
        data = json.dumps({"username" : "john", "email" : "johnmuiya@gmail.com",
                           "password" : "secret12345", "confirm_password" : "secret12345"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        response2 = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response2.data)
        self.assertEqual(result.get("message"), "User with that email already exists")

    def test_create_user_using_unmatching_passwords(self):
        """Tests unsuccessfully creating a new user because of unmatching passwords"""
        data = json.dumps({"username" : "felix", "email" : "felixmutua@gmail.com",
                           "password" : "secret12345", "confirm_password" : "password12345"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), "Password and confirm_password should be identical")

    def test_create_user_using_short_passwords(self):
        """Tests unsuccessfully creating a new user because of too short passwords"""
        data = json.dumps({"username" : "moses", "email" : "musamutua@gmail.com",
                           "password" : "123", "confirm_password" : "123"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), "Password should be at least 8 characters")

    def test_create_user_empty_username(self):
        """Tests unsuccessfully creating a new user because of empty username"""
        data = json.dumps({"email" : "lennykmutua@gmail.com", "password" : "secret", "confirm_password" : "secret"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"username": "no username provided"})
    
    def test_create_user_empty_email(self):
        """Tests unsuccessfully creating a new user because of empty email"""
        data = json.dumps({"username" : "lenny", "password" : "secret", "confirm_password" : "secret"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"email": "no email provided"})
    
    def test_create_user_invalid_email(self):
        """Tests unsuccessfully creating a new user because of invalid email"""
        data = json.dumps({"username" : "lenny", "email" : "lennykmugmail.com",
                           "password" : "secret", "confirm_password" : "secret"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"email": "no email provided"})

    def test_create_user_empty_password(self):
        """Tests unsuccessfully creating a new user because of empty password"""
        data = json.dumps({"username" : "lenny", "email" : "lennymutush@gmail.com",
                           "confirm_password" : "secret"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"password": "no password provided"})

    def test_create_user_empty_confirm_password(self):
        """Tests unsuccessfully creating a new user because of empty confirm_password"""
        data = json.dumps({"username" : "lenny", "email" : "lennykmutua@gmail.com",
                           "password" : "secret"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"confirm_password": "no password confirmation provided"})
    
    def test_successfully_getting_one_user(self):
        """Test getting one user using the user's id"""
        response = self.app.get('/api/v1/users/1')
        self.assertEqual(response.status_code, 200)
    
    def test_getting_non_existing_user(self):
        """Test getting a user while provideing non-existing id"""
        response = self.app.get('/api/v1/users/57')
        self.assertEqual(response.status_code, 404)
    
    def test_successfully_updating_existing_user(self):
        """Test a successful user update"""
        data = json.dumps({"username" : "balotelli", "email" : "mariobalotelli@gmail.com",
                           "password" : "secret12345", "confirm_password" : "secret12345"})
        response = self.app.put('/api/v1/users/1', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_updating_non_existing_user(self):
        """Test a successful user update"""
        data = json.dumps({"username" : "balotelli", "email" : "mariobalotelli@gmail.com",
                           "password" : "secret12345", "confirm_password" : "secret12345"})
        response = self.app.put('/api/v1/users/99', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_successfully_deleting_one_user(self):
        """Test a successful user delete"""
        response = self.app.delete('/api/v1/users/2')
        self.assertEqual(response.status_code, 200)
    
    def test_deleting_non_existing_user(self):
        """Test a deleting user that does not exist"""
        response = self.app.delete('/api/v1/users/15')
        self.assertEqual(response.status_code, 404)

# testing Meals

    def test_get_all_meals(self):
        """Tests successfully getting all meals through the meals endpoint"""
        response = self.app.get('/api/v1/meals')
        self.assertEqual(response.status_code, 200)

    def test_successful_meal_creation(self):
        """Tests successfully creating a new meal through the meals endpoint"""
        data = json.dumps({"name" : "Rice and Beans", "price" : 400})
        response = self.app.post('/api/v1/meals', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("name"), "Rice and Beans")
        self.assertEqual(result.get("price"), '400')
        self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()
