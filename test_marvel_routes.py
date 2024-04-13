"""Testing App Marvel routes"""

#run these tests like:
# python -m unittest test_marvel_routes.py


from unittest import TestCase

from app import create_app
from sqlalchemy import exc
from models import db, connect_db, User, MarvelCharacters, FavoriteCharacters

app = create_app("marvel_test", testing=True)  # this is a different instance of the app
connect_db(app)


db.drop_all()
db.create_all()

class PostsRoutesTestCase(TestCase):
    """Test the app Marvel routes"""
    def setUp(self):
        """Make sure the db is clean before doing the tests"""
        User.query.delete()
        MarvelCharacters.query.delete()
        FavoriteCharacters.query.delete()
        db.session.commit()
    def tearDown(self):
        """Remove all records from database tables"""
        db.session.rollback()

    def test_character_route(self):
        """Does the routes show character's details?"""
        with app.test_client() as client:
            d= {"username": "test",
                "password": "test123",
                "email": "test@gmail.com",
                "first_name": "test",
                "last_name": "fake",
                "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)
            new_ch = MarvelCharacters(id = 9999, name = "superhero")
            db.session.add(new_ch)
            db.session.commit()
            resp = client.get('/characters/9999')
            html= resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("superhero", html)

    def test_character_search(self):
        """When the user searches a new Marvel character, how does the app handle it?"""
        with app.test_client() as client:
            d= {"username": "test",
                "password": "test123",
                "email": "test@gmail.com",
                "first_name": "test",
                "last_name": "fake",
                "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)
            resp = client.post('/get-character', data={"characterName":"thanos"}, follow_redirects=True)
            html= resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Thanos", html)

    def test_fav_char_page(self):
        """Does the app show user's favorite characters?"""
        with app.test_client() as client:
            d= {"username": "test",
                "password": "test123",
                "email": "test@gmail.com",
                "first_name": "test",
                "last_name": "fake",
                "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)
            new_ch = MarvelCharacters(id = 9999, name = "superhero")
            db.session.add(new_ch)
            db.session.commit()
            fav_char = FavoriteCharacters(user_id = d["username"], character_id = 9999)
            db.session.add(fav_char)
            db.session.commit()

            resp = client.get(f'/users/{d["username"]}/favorite/characters')
            html= resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("superhero", html)
            self.assertIn("Delete Profile", html)

