"""Testing User's models"""

#run these tests like:
# python -m unittest test_user_models.py


from unittest import TestCase

from app import create_app
from sqlalchemy import exc
from models import db, connect_db, User, Post, Like, Comment

app = create_app("marvel_test", testing=True)  # this is a different instance of the app
connect_db(app)


db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Test all models related to users
    Testing models: User, Post, Like and Comment"""
    def setUp(self):
        """create test client, add sample data"""

        User.query.delete()
        Post.query.delete()
        Like.query.delete()
        Comment.query.delete()
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """Remove all records from database tables"""
        db.session.rollback()


    def test_creating_new_user_valid(self):
        """Does the db create a new user if passed in data is VALID?"""
        new_user = User(
            username = "test",
            email = "test@gmail.com",
            first_name = "testF",
            last_name = "testL",
            bio = "I am a chicken.",
            image_url = "",
            password = "secret")
        db.session.add(new_user)
        db.session.commit()

        self.assertEqual(new_user.username, "test")
        self.assertEqual(new_user.email, "test@gmail.com")
        self.assertEqual(new_user.first_name, "testF")
        self.assertEqual(new_user.last_name, "testL")
        self.assertEqual(new_user.greet(), "username: test; email: test@gmail.com; first_name: testF; last_name: testL")

    def test_creating_new_user_invalid(self):
        """Does the db create a new user if passed in data is INVALID?
        The email is null."""
        new_user = User(
            username = "test",
            first_name = "testF",
            last_name = "testL",
            bio = "I am a chicken.",
            image_url = "",
            password = "secret")
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.add(new_user)
            db.session.commit()

    def test_register(self):
        """test if register encrypts the password"""
        password = User.register('secret')

        self.assertNotEqual(password.password, "secret")
    def test_authentication(self):
        """test login feature
        the test should pass if the user enter the right data
        the test returns False if the user enter invalid data"""
        username = "test"
        password= "test123"
        email= "test@gmail.com"
        first_name = "test"
        last_name = "account"
        bio = "ignore me"
        image_url = "https://hips.hearstapps.com/hmg-prod/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg?crop=0.752xw:1.00xh;0.175xw,0&resize=1200:*"

        hashed_password = User.register(password)
        hashed_password = hashed_password.password

        new_user = User(username= username, password=hashed_password, email=email, first_name=first_name, last_name=last_name, bio=bio, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()

        user= User.authenticate("test", "test123")
        self.assertEqual(user.username, "test")
        self.assertEqual(user.last_name, "account")

        wrong_user= User.authenticate("test", "test1234")
        self.assertEqual(wrong_user, False)

    def test_post_model(self):
        """test the db successfully create a new post
        test the realtionship between the user and the post
        the post should be deleted once the user is deleted"""
        username = "test"
        password= "test123"
        email= "test@gmail.com"
        first_name = "test"
        last_name = "account"
        bio = "ignore me"
        image_url = "https://hips.hearstapps.com/hmg-prod/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg?crop=0.752xw:1.00xh;0.175xw,0&resize=1200:*"

        hashed_password = User.register(password)
        hashed_password = hashed_password.password

        new_user = User(username= username, password=hashed_password, email=email, first_name=first_name, last_name=last_name, bio=bio, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()

        
        user = User.query.filter_by(username= username).first()
        new_post = Post(text= "chicken",
                        user_id = user.username)
        db.session.add(new_post)
        db.session.commit()
        
        post = Post.query.filter_by(text = "chicken").first()
        self.assertEqual(post.text, "chicken")

        # the post should be deleted once the user is deleted
        db.session.delete(user)
        db.session.commit()
        self.assertEqual(Post.query.filter_by(text = "chicken").first(), None)

    def test_like_model(self):
        """test the db successfully create a new post like
        test the realtionship between the user, the post and like
        the like should be deleted once the user and post are deleted"""
        username = "test"
        password= "test123"
        email= "test@gmail.com"
        first_name = "test"
        last_name = "account"
        bio = "ignore me"
        image_url = "https://hips.hearstapps.com/hmg-prod/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg?crop=0.752xw:1.00xh;0.175xw,0&resize=1200:*"

        hashed_password = User.register(password)
        hashed_password = hashed_password.password

        new_user = User(username= username, password=hashed_password, email=email, first_name=first_name, last_name=last_name, bio=bio, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()

        user = User.query.filter_by(username= username).first()
        new_post = Post(text= "chicken",
                        user_id = user.username)
        db.session.add(new_post)
        db.session.commit()

        post = Post.query.filter_by(text = "chicken").first()
        new_like = Like(user_id = user.username, post_id = post.id)
        db.session.add(new_like)
        db.session.commit()

        self.assertNotEqual(Like.query.filter_by(user_id = user.username, post_id = post.id).first(), None)

        # the like should be deleted once the user and post are deleted
        db.session.delete(user)
        db.session.commit()
        self.assertEqual(Like.query.filter_by(user_id = user.username, post_id = post.id).first(), None)

    def test_comment_model(self):
        """test the db successfully create a new post comment
        test the realtionship between the user, the post and comment
        the comment should be deleted once the user and post are deleted"""
        username = "test"
        password= "test123"
        email= "test@gmail.com"
        first_name = "test"
        last_name = "account"
        bio = "ignore me"
        image_url = "https://hips.hearstapps.com/hmg-prod/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg?crop=0.752xw:1.00xh;0.175xw,0&resize=1200:*"

        hashed_password = User.register(password)
        hashed_password = hashed_password.password

        new_user = User(username= username, password=hashed_password, email=email, first_name=first_name, last_name=last_name, bio=bio, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()

        user = User.query.filter_by(username= username).first()
        new_post = Post(text= "chicken",
                        user_id = user.username)
        db.session.add(new_post)
        db.session.commit()

        post = Post.query.filter_by(text = "chicken").first()
        new_comment = Comment(text= "hello", user_id = user.username, post_id = post.id)
        db.session.add(new_comment)
        db.session.commit()

        self.assertNotEqual(Comment.query.filter_by(text = "hello", user_id = user.username, post_id = post.id).first(), None)