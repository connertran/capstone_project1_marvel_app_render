# ""Testing Marvel's models"""

#run these tests like:
# python -m unittest test_marvel_models.py


from unittest import TestCase

from app import create_app
from sqlalchemy import exc
from models import db, connect_db, MarvelCharacters, MarvelComics, ComicsCharacters, FavoriteCharacters, User

app = create_app("marvel_test", testing=True)  # this is a different instance of the app
connect_db(app)


db.drop_all()
db.create_all()

class MarvelModelTestCase(TestCase):
    """Test all models related to Marvel chacters and comics
    Testing models: MarvelCharacter, MarvelComics, ComicsCharacter and FavoriteCharacters"""
    def setUp(self):
        """create test client, add sample data"""

        MarvelCharacters.query.delete()
        MarvelComics.query.delete()
        ComicsCharacters.query.delete()
        FavoriteCharacters.query.delete()
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """Remove all records from database tables"""
        db.session.rollback()
    
    def test_creating_new_character(self):
        """Does the db create a new Marvel character?"""
        new_char = MarvelCharacters(
            id = 9999, #fake id
            name = "heroTest",
            thumbnail = "https://static.printler.com/cache/b/9/e/c/4/3/b9ec43763fbfb960ef0e68ee8ae291e5549d0969.jpg",
            description = "I am Iron Man.")
        db.session.add(new_char)
        db.session.commit()

        char = MarvelCharacters.query.filter_by(name= "heroTest").first()
        self.assertEqual(char.name, "heroTest")
        self.assertEqual(char.description, "I am Iron Man.")

        new_char2 = MarvelCharacters(
            id = 1111, #fake id
            name = "heroTest2")
        db.session.add(new_char2)
        db.session.commit()
        char2 = MarvelCharacters.query.filter_by(id= 1111).first()
        self.assertEqual(char2.thumbnail, "https://i.pinimg.com/564x/f8/34/20/f834200e7e42ea53b4fba62a17c8f107.jpg")
        self.assertEqual(char2.description, "No description")
    
    def test_creating_new_comics(self):
        """Does the db create a new Marvel comics?"""
        new_com = MarvelComics(
            id = 1234, #fake id
            title = "FakeCom")
        db.session.add(new_com)
        db.session.commit()
        com = MarvelComics.query.filter_by(id= 1234).first()
        self.assertNotEqual(com, None)
        self.assertEqual(com.title, "FakeCom")

    def test_comics_characters(self):
        """Does the db create a new row in comics_characters table?
        Will the row be deleted if character and comics are deleted?"""
        new_char = MarvelCharacters(
            id = 9999, #fake id
            name = "heroTest",
            thumbnail = "https://static.printler.com/cache/b/9/e/c/4/3/b9ec43763fbfb960ef0e68ee8ae291e5549d0969.jpg",
            description = "I am Iron Man.")
        new_com = MarvelComics(
            id = 1234, #fake id
            title = "FakeCom")
        db.session.add(new_char)
        db.session.add(new_com)
        db.session.commit()

        new_com_char = ComicsCharacters(
            character_id = new_char.id, comics_id = new_com.id
        )
        db.session.add(new_com_char)
        db.session.commit()

        com_char= ComicsCharacters.query.filter_by(character_id = 9999, comics_id = 1234).first()
        self.assertNotEqual(com_char, None)

        db.session.delete(new_char)
        db.session.delete(new_com)
        db.session.commit()
        com_char= ComicsCharacters.query.filter_by(character_id = 9999, comics_id = 1234).first()
        self.assertEqual(com_char, None)

    def test_favorite_characters(self):
        """Does the db create a new favorite character?
        Will the favorite character be deleted if the user is deleted?"""
        new_char = MarvelCharacters(
            id = 9999, #fake id
            name = "heroTest",
            thumbnail = "https://static.printler.com/cache/b/9/e/c/4/3/b9ec43763fbfb960ef0e68ee8ae291e5549d0969.jpg",
            description = "I am Iron Man.")
        db.session.add(new_char)
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
        new_fav_char = FavoriteCharacters(user_id = new_user.username, character_id = new_char.id)
        db.session.add(new_fav_char)
        db.session.commit()

        fav_char = FavoriteCharacters.query.filter_by(user_id = new_user.username, character_id = new_char.id).first()
        self.assertNotEqual(fav_char, None)

        user = User.query.get("test")
        db.session.delete(user)
        db.session.commit()
        deleted_fav_char = FavoriteCharacters.query.filter_by(user_id = new_user.username, character_id = new_char.id).first()
        self.assertEqual(deleted_fav_char, None)