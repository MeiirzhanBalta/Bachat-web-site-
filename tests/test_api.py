import json
from flask_testing import TestCase
from app import app, db

class TestAPI(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_registration(self):
        response = self.client.post('/users', data=json.dumps({
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john@example.com',
            'password': 'securepassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 302)  # Перенаправление на главную страницу

    def test_login(self):
        # Предполагаем, что пользователь уже зарегистрирован
        response = self.client.post('/login', data=json.dumps({
            'email': 'john@example.com',
            'password': 'securepassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Logged in successfully', response.data.decode())

if __name__ == "__main__":
    import pytest
    pytest.main()

# В качестве дополнения можно добавить больше тестов для других эндпоинтов
