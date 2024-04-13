"""Testing Forms"""

#run these tests like:
# python -m unittest test_forms.py

from unittest import TestCase
from flask import session

from app import create_app
from sqlalchemy import exc
from models import db, connect_db, User
from forms import RegisterForm, LoginForm, EditForm, PostForm

app = create_app("marvel_test", testing=True)  # this is a different instance of the app
connect_db(app)

class TestingAppWTForms(TestCase):
    """Do the forms work with valid data?
    Do they fail with INVALID data?"""
    def setUp(self):
        """delete the testing user from db"""
        User.query.delete()
        db.session.commit()
        
    def test_register_form_view(self):
        """Does the app show the form?"""        
        with app.test_client() as client:
            resp = client.get('/register')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('for="username">Username</label>', html)
    def test_register_form_post_valid(self):
        """Does the register form work with valid data?"""
        with app.test_client() as client:
            d= {"username": "test",
                   "password": "test123",
                   "email": "test@gmail.com",
                   "first_name": "test",
                   "last_name": "fake",
                   "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('href="/logout"', html)

    def test_register_form_post_invalid(self):
        """Does the register form fail with invalid data?"""
        with app.test_client() as client:
            d= {"username": "test",
                   "email": "test@gmail.com",
                   "first_name": "test",
                   "last_name": "fake",
                   "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Register', html)
    
    def test_login_form(self):
        """Test the login form with valid and invalid data.
        First register to the system. Then logout. Finally log in with valid data"""
        with app.test_client() as client:
            d= {"username": "test",
                   "password": "test123",
                   "email": "test@gmail.com",
                   "first_name": "test",
                   "last_name": "fake",
                   "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)
            #after redirection the user is at the homepage
            resp = client.get('/logout', follow_redirects=True)
            #after redirection the user is at the login page
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Login', html)

            #after successfully saving a new user to db
            login_valid = {"username": "test",
                           "password": "test123"}
            resp = client.post('/login', data=login_valid, follow_redirects=True)
            html = resp.get_data(as_text = True)

            # the user now is at the homepage
            self.assertEqual(resp.status_code, 200)
            self.assertIn('href="/logout"', html)

            #logout again
            resp = client.get('/logout', follow_redirects=True)
            #after redirection the user is at the login page
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Login', html)

            login_invalid = {"username": "test",
                             "password": "test321"}
            resp = client.post('/login', data=login_invalid, follow_redirects=True)
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Login', html)

    def test_edit_form(self):
        """Does the app show the form?
        Does the form work (can it change the database)?
        Does"""
        with app.test_client() as client:
            d= {"username": "test",
                   "password": "test123",
                   "email": "test@gmail.com",
                   "first_name": "test",
                   "last_name": "fake",
                   "image_url": "https://cdn.pixabay.com/photo/2023/02/08/02/40/iron-man-7775599_960_720.jpg",
                   "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)
            #after redirection the user is at the homepage
            resp = client.get(f'/users/{d["username"]}/edit', follow_redirects=True)
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('for="email"', html)

            edit_d = {"username": "test_user",
                   "password": "test123",
                   "email": "test@gmail.com",
                   "first_name": "test",
                   "last_name": "fake",
                   "image_url": "https://cdn.pixabay.com/photo/2023/02/08/02/40/iron-man-7775599_960_720.jpg",
                   "bio": "Sun god"}
            resp = client.post(f'/users/{d["username"]}/edit', data=edit_d, follow_redirects=True)
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('test_user', html)

            #go back to the edit form
            #but this time enter a wrong password
            resp = client.get(f'/users/{edit_d["username"]}/edit', follow_redirects=True)
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('for="email"', html)
            
            edit_d_wrong_pass = {"username": "test_user_wrong",
                                 "password": "321test",
                                 "email": "test@gmail.com",
                                 "first_name": "test",
                                 "last_name": "fake","image_url": "https://cdn.pixabay.com/photo/2023/02/08/02/40/iron-man-7775599_960_720.jpg",
                                 "bio": "Sun god"}
            resp = client.post(f'/users/{d["username"]}/edit', data=edit_d_wrong_pass, follow_redirects=True)
            # the user is still at the edit form
            self.assertEqual(resp.status_code, 200)
            self.assertIn('for="email"', html)

    def test_post_form(self):
        """Does the app show the form?
        Does the form send data to db?"""
        with app.test_client() as client:
            d= {"username": "test",
                   "password": "test123",
                   "email": "test@gmail.com",
                   "first_name": "test",
                   "last_name": "fake",
                   "image_url": "https://cdn.pixabay.com/photo/2023/02/08/02/40/iron-man-7775599_960_720.jpg",
                   "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)
            resp = client.get(f'/users/{d["username"]}/post', follow_redirects=True)
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('for="text"', html)

            form_d = {"text": "superhero"}
            resp = client.post(f'/users/{d["username"]}/post', data=form_d, follow_redirects=True)
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('superhero', html)




