"""Testing App users' routes"""

#run these tests like:
# python -m unittest test_users_routes.py


from unittest import TestCase

from app import create_app
from sqlalchemy import exc
from models import db, connect_db, User

app = create_app("marvel_test", testing=True)  # this is a different instance of the app
connect_db(app)


db.drop_all()
db.create_all()

class RoutesTestCase(TestCase):
    """Test the app users routes"""
    def setUp(self):
        User.query.delete()
        db.session.commit()

    def tearDown(self):
        """Remove all records from database tables"""
        db.session.rollback()

    def test_home_page(self):
        """Does the app show the hompage?
        The app shows the login page when the user is not logged in."""
        with app.test_client() as client:
            resp = client.get('/', follow_redirects=True)
            html= resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Login", html)

            d= {"username": "test",
                "password": "test123",
                "email": "test@gmail.com",
                "first_name": "test",
                "last_name": "fake",
                "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)
            html= resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Marvel App", html)

    def test_logout_route(self):
        """How does the app handle logout route?"""
        with app.test_client() as client:
            resp = client.get('/logout', follow_redirects=True)
            html= resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Login", html)
    def test_users_page(self):
        """Does the app show the users' profile page?"""
        with app.test_client() as client:
            d= {"username": "test",
                    "password": "test123",
                    "email": "test@gmail.com",
                    "first_name": "test",
                    "last_name": "fake",
                    "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)
            resp = client.get(f'/users/{d["username"]}', follow_redirects=True)
            html= resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Delete Profile", html)

    #/users/<username>/edit route's been tested in the test_forms.py
    
    def test_delete_user(self):
        """Does the route delete the user from db?"""
        with app.test_client() as client:
            d= {"username": "test",
                    "password": "test123",
                    "email": "test@gmail.com",
                    "first_name": "test",
                    "last_name": "fake",
                    "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)
            resp = client.post(f'/users/{d["username"]}/delete', follow_redirects =True)
            html= resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Login", html)

            #try to login
            login_data = {"username": "test",
                          "password": "test123"}
            resp = client.post('/login', data=login_data, follow_redirects=True)
            html= resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Login", html)
            self.assertIn("Submit", html)




