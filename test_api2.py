"""Separate the API test file to different parts due to the API test duration"""

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
    def test_delete_fav_char(self):
        """Is the api able to delete user's favorite character in the db?"""
        with app.test_client() as client:
            d= {"username": "test",
                "password": "test123",
                "email": "test@gmail.com",
                "first_name": "test",
                "last_name": "fake",
                "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)
            new_char = MarvelCharacters(id = 9999, #fake id
                                        name = "heroTest")
            db.session.add(new_char)
            new_fav_char = FavoriteCharacters(user_id = d["username"], character_id = new_char.id)
            db.session.add(new_fav_char)
            db.session.commit()

            resp = client.delete('/api/favorite-characters/9999', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            data= resp.json
            self.assertEqual(data['message'], "Deleted!")

    def test_add_fav_char(self):
        """Does the api add a new favorite character?"""
        with app.test_client() as client:
            d= {"username": "test",
                "password": "test123",
                "email": "test@gmail.com",
                "first_name": "test",
                "last_name": "fake",
                "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)
            new_char = MarvelCharacters(id = 9999, #fake id
                                        name = "heroTest")
            db.session.add(new_char)
            db.session.commit()

            resp = client.post('/api/favorite-characters/9999', follow_redirects=True)
            self.assertEqual(resp.status_code, 201)
            data= resp.json
            self.assertEqual(data['added']['user_id'], d['username'])
            self.assertEqual(data['added']['character_id'], 9999)


