"""Separate the API test file to different parts due to the API test duration"""

from unittest import TestCase

from app import create_app
from flask import session, g
from sqlalchemy import exc
from models import db, connect_db, User, MarvelCharacters,FavoriteCharacters, Post

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
    
    def test_delete_post(self):
        """Is the api able to delete user's post from the db?"""
        with app.test_client() as client:
            d= {"username": "test",
                "password": "test123",
                "email": "test@gmail.com",
                "first_name": "test",
                "last_name": "fake",
                "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)

            new_post = Post(text= "chicken",
                        user_id = d["username"])
            db.session.add(new_post)
            db.session.commit()
            post = Post.query.filter_by(text= "chicken").first()
            resp = client.delete(f'/api/posts/{post.id}', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data['message'], "Deleted!")

    def test_like(self):
        """Is the api able to add and delete a new like to db?"""
        with app.test_client() as client:
            d= {"username": "test",
                "password": "test123",
                "email": "test@gmail.com",
                "first_name": "test",
                "last_name": "fake",
                "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)

            new_post = Post(text= "chicken",
                        user_id = d["username"])
            db.session.add(new_post)
            db.session.commit()
            post = Post.query.filter_by(text= "chicken").first()
            resp = client.post(f'/api/posts/{post.id}/like', follow_redirects=True)

            self.assertEqual(resp.status_code, 201)
            data = resp.json
            self.assertEqual(data['like']['user_id'], "test")
            self.assertEqual(data['like']['post_id'], post.id)

            resp = client.delete(f'/api/posts/{post.id}/like', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data['message'], "Deleted!")
    
    def test_comment(self):
        """Is the api able to post a new comment?
        Can the api show a list of comments?"""
        with app.test_client() as client:
            d= {"username": "test",
                    "password": "test123",
                    "email": "test@gmail.com",
                    "first_name": "test",
                    "last_name": "fake",
                    "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)

            new_post = Post(text= "chicken",
                            user_id = d["username"])
            db.session.add(new_post)
            db.session.commit()
            post = Post.query.filter_by(text= "chicken").first()
            #before adding a comment
            resp = client.get(f'/api/posts/{post.id}/comments')
            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data['comments'], [])

            #adding a comment
            comment = {"text": "hello"}
            resp = client.post(f'/api/posts/{post.id}/comments', json=comment, follow_redirects=True)
            self.assertEqual(resp.status_code, 201)
            data = resp.json
            self.assertEqual(data['comment']['text'], "hello")

            #after adding a comment
            resp = client.get(f'/api/posts/{post.id}/comments')
            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertNotEqual(data['comments'], [])
