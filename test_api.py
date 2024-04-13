from unittest import TestCase

from app import create_app
from flask import session, g
from sqlalchemy import exc
from models import db, connect_db, User, MarvelCharacters,FavoriteCharacters

app = create_app("marvel_test", testing=True)  # this is a different instance of the app
connect_db(app)

db.drop_all()
db.create_all()

class RESTFULApiTesting(TestCase):
    """Test all app APIs"""
    def setUp(self):
        """Register the testing user before each test"""
        User.query.delete()
        MarvelCharacters.query.delete()
        FavoriteCharacters.query.delete()
        db.session.commit()
    def tearDown(self):
        """Remove all records from db tables"""
        db.session.rollback()
    def test_list_characters(self):
        """Does the api show all characters in db"""
        with app.test_client() as client:
            d= {"username": "test",
                   "password": "test123",
                   "email": "test@gmail.com",
                   "first_name": "test",
                   "last_name": "fake",
                   "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)
            user = User.query.filter_by(username=d["username"]).first()
            self.assertIsNotNone(user)
            self.assertEqual('user_username' in session, True)

            resp = client.get("/api/characters", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertIsInstance(data, dict)
            self.assertIn("characters", data)
    def test_show_a_character(self):
        """Does the api show correct Marvel character based on the id?"""
        with app.test_client() as client:
            d= {"username": "test",
                   "password": "test123",
                   "email": "test@gmail.com",
                   "first_name": "test",
                   "last_name": "fake",
                   "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)

            marvel_char = MarvelCharacters(id= 9999, name = "Thor")
            db.session.add(marvel_char)
            db.session.commit()

            resp= client.get(f'/api/characters/{marvel_char.id}', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertIsInstance(data, dict)
            self.assertEqual(data['character']['name'],'Thor')
    def test_list_all_users(self):
        """Does the api show all the users"""
        with app.test_client() as client:
            d= {"username": "test",
                "password": "test123",
                "email": "test@gmail.com",
                "first_name": "test",
                "last_name": "fake",
                "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)
            log_out = client.get('/logout')
            user2= {"username": "test2",
                "password": "test123",
                "email": "test2@gmail.com",
                "first_name": "test2",
                "last_name": "fake2",
                "bio": "Sun god2"}
            resp = client.post('/register', data=user2, follow_redirects=True)
            resp= client.get('/api/users', follow_redirects=True)
            
            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data['users'][0]['first_name'],'test')
            self.assertEqual(data['users'][1]['first_name'],'test2')
    
    def test_user_id(self):
        """Does the api show correct user based on the id?"""
        with app.test_client() as client:
            d= {"username": "test",
                "password": "test123",
                "email": "test@gmail.com",
                "first_name": "test",
                "last_name": "fake",
                "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)
            resp= client.get(f'/api/users/{d["username"]}', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data['user']['email'], d["email"])

    def test_edit_user(self):
        """Is the api able to change user's info in the db?"""
        with app.test_client() as client:
            d= {"username": "test",
                "password": "test123",
                "email": "test@gmail.com",
                "first_name": "test",
                "last_name": "fake",
                "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)
            edit={"username": "test2",
                "password": "test123",
                "email": "test2@gmail.com",
                "first_name": "test2",
                "last_name": "fake2",
                "bio": "Sun god2"}
            resp = client.patch(f'/api/users/{d["username"]}', json=edit, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data['user']['first_name'], edit["first_name"])


