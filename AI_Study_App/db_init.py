from app import app
from database import db

# Initialize the database
with app.app_context():
    db.create_all()
print("Database initialized successfully!")
