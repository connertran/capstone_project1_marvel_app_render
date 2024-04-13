"""Testing App posts routes"""

#run these tests like:
# python -m unittest test_posts_routes.py


from unittest import TestCase

from app import create_app
from sqlalchemy import exc
from models import db, connect_db, User, Post

app = create_app("marvel_test", testing=True)  # this is a different instance of the app
connect_db(app)


db.drop_all()
db.create_all()

class PostsRoutesTestCase(TestCase):
    """Test the app posts routes"""
    def setUp(self):
        """Make sure the db is clean before doing the tests"""
        User.query.delete()
        Post.query.delete()
        db.session.commit()
    def tearDown(self):
        """Remove all records from database tables"""
        db.session.rollback()

    #/users/<username>/post' route's tested in the test_forms.py
    def test_posts_list_route(self):
        """Does the routes show posts from db?"""
        with app.test_client() as client:
            d= {"username": "test",
                "password": "test123",
                "email": "test@gmail.com",
                "first_name": "test",
                "last_name": "fake",
                "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)
            new_p = Post(text = "chicken", user_id = d["username"])
            new_p2 = Post(text = "chicken2", user_id = d["username"])
            db.session.add(new_p)
            db.session.add(new_p2)
            db.session.commit()
            resp = client.get('/posts')
            html= resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("chicken", html)
            self.assertIn("chicken2", html)
            self.assertIn("Details", html)

    def test_post_details(self):
        """Does the route the post details?"""
        with app.test_client() as client:
            d= {"username": "test",
                "password": "test123",
                "email": "test@gmail.com",
                "first_name": "test",
                "last_name": "fake",
                "bio": "Sun god"}
            resp = client.post('/register', data=d, follow_redirects=True)
            new_p = Post(text = "chicken", user_id = d["username"])
            db.session.add(new_p)
            db.session.commit()
            post = Post.query.filter_by(text = "chicken").first()
            resp = client.get(f'/posts/{post.id}/details')
            html= resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("chicken", html)
            self.assertIn("Comment", html)
