from app import create_app
from models import connect_db

app = create_app("marvel_db")
connect_db(app)