from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """
    Represents a user in the system.
    
    Attributes:
    id (int): Unique identifier for the user.
    name (str): User's full name.
    email (str): User's email address.
    password (str): Hashed password for authentication.
    preferred_study_hours (int): Number of hours the user prefers to study.
    preferred_study_time (str): Preferred study time in HH:MM format.
    subjects (list): List of subjects associated with the user.
    created_at (datetime): Timestamp when the user account was created.
    updated_at (datetime): Timestamp when the user account was last updated.
    """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password = db.Column(db.String(150), nullable=False)
    preferred_study_hours = db.Column(db.Integer, nullable=False, default=2)
    preferred_study_time = db.Column(db.String(10), nullable=False, default="18:00")  # Default study time is 6 PM
    subjects = db.relationship('Subject', backref='user', lazy=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def set_password(self, password):
        """Hashes the password before storing it."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verifies if the provided password matches the stored hash."""
        return check_password_hash(self.password, password)

class Subject(db.Model):
    """
    Represents a subject in the study application.
    
    Attributes:
    id (int): Unique identifier for the subject.
    name (str): Name of the subject.
    pdf_path (str): File path to the subject's PDF resource.
    allocated_day (str): Day of the week when the subject is allocated.
    flashcards (list): List of flashcards associated with the subject.
    progress (int): Current study progress as a percentage.
    completed_flashcards (int): Number of flashcards completed.
    total_flashcards (int): Total number of flashcards in the subject.
    user_id (int): Foreign key referencing the associated User model.
    created_at (datetime): Timestamp when the subject was created.
    updated_at (datetime): Timestamp when the subject was last updated.
    """

    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    pdf_path = db.Column(db.String(200), nullable=False)  # Path to the uploaded PDF
    allocated_day = db.Column(db.String(10), nullable=False)  # Day of the week (e.g., "Monday")
    flashcards = db.Column(db.JSON, nullable=True, default=[])  # JSON field to store flashcards
    progress = db.Column(db.Integer, nullable=False, default=0)  # Study progress in percentage
    completed_flashcards = db.Column(db.Integer, nullable=False, default=0)
    total_flashcards = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=datetime.now(timezone.utc))
