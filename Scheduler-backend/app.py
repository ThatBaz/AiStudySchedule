from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from database import Subject, db, User
from flask_migrate import Migrate
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader

app = Flask(__name__)
app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Needed for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/study_schedule_db'  # Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # For file uploads (optional)

# Initialize SQLAlchemy and Flask-Migrate
db.init_app(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate with the app and db

# Enable CORS for cross-origin requests
CORS(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

## Load summarization model
# tokenizer = AutoTokenizer.from_pretrained("flashcard_summarizer")
# model = AutoModelForSeq2SeqLM.from_pretrained("flashcard_summarizer")

@app.route('/')
def home():
    """Renders the welcome page."""
    return "Welcome to the AI-Powered Study Scheduler!"

#def generate_flashcards_from_pdf(filepath):
    """Generates flashcards from a PDF file."""
    flashcards = []
    reader = PdfReader(filepath)
    text = " ".join([page.extract_text() for page in reader.pages])

    # Split text into chunks for summarization
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]

    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(inputs['input_ids'], max_length=128, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
        flashcards.append(summary)

    return flashcards


# # Summarize PDFs into Flashcards
# @app.route('/generate_flashcards', methods=['POST'])
# @login_required
# def generate_flashcards():
#     """Generates flashcards for all subjects associated with the current user."""
#     subjects = Subject.query.filter_by(user_id=current_user.id).all()
    
#     for subject in subjects:
#         if not subject.flashcards:  # If flashcards are not already generated
#             with open(subject.pdf_path, 'r') as f:
#                 content = f.read()
            
#             inputs = tokenizer(content, return_tensors="pt", max_length=512, truncation=True)
#             outputs = model.generate(inputs['input_ids'], max_length=128, num_beams=4, early_stopping=True)
#             flashcards = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
#             subject.flashcards = flashcards
#             db.session.commit()
#     return jsonify(message="Flashcards generated successfully!"), 200

# File upload for flashcard generation
@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles file uploads for generating flashcards."""
    if 'file' not in request.files:
        return "No file uploaded", 400
    file = request.files['file']
    
    # Process file here and generate flashcards
    # (Placeholder example below for file processing)
    generated_flashcards = [{"question": "Sample Q1", "answer": "Sample A1"}]
    return jsonify(status="success", flashcards=generated_flashcards)

# Load the user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Loads the user object for Flask-Login."""
    return User.query.get(int(user_id))

# Signup route
@app.route('/register', methods=['POST'])
def register():
    """Handles user registration."""
    data = request.form
    preferred_hours = int(data['study_hours'])
    study_time = data['study_time']  # e.g., "08:00-10:00"
    subjects = []

    if 'files' in request.files:
        files = request.files.getlist('files')
        for file in files:
            subject_name = data[f'subject_name_{file.filename}']
            study_day = data[f'study_day_{file.filename}']
            
            filename = secure_filename(file.filename)
            # Save uploaded PDF
            filename = secure_filename(file.filename)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            subjects.append({
                "name": subject_name,
                "filename": filename,
                "study_day": study_day
            })

    user = User(
        name = data['name'],
        email=data['email'],
        password=generate_password_hash(data['password']),
        study_hours=preferred_hours,
        study_time=study_time,
        subjects=subjects
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(message="User registered successfully"), 201

# Login route
@app.route('/login', methods=['POST'])
def login():
    """Handles user login."""
    data = request.json
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    login_user(user)
    login_user(user)
    return jsonify({"message": "Login successful"}), 200

# Logout route
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    """Logs out the current user."""
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

# Profile update route
@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    """Updates the user profile."""
    data = request.json
    current_user.study_hours = data.get('study_hours', current_user.study_hours)
    current_user.work_hours = data.get('work_hours', current_user.work_hours)
    current_user.preferred_topics = data.get('preferred_topics', current_user.preferred_topics)
    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200

# # Generate Schedule
# @app.route('/generate_schedule', methods=['POST'])
# @login_required
# def generate_schedule():
#     """Generates a study schedule based on user preferences and available flashcards."""
#     tasks = request.json.get('tasks', [])
#     study_hours = current_user.study_hours
#     study_time = current_user.study_time  # e.g., "08:00-10:00"
#     total_minutes = study_hours * 60
#     flashcards_per_session = total_minutes // 10

#     schedule = []
#     current_date = datetime.now()

#     for subject in current_user.subjects:
#         # Load flashcards for the subject
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], subject['filename'])
        
#         flashcards = generate_flashcards_from_pdf(filepath)

#         # Allocate flashcards for the study day
#         flashcards_allocated = 0
#         for flashcard in flashcards:
#             if flashcards_allocated >= flashcards_per_session:
#                 break

#             schedule.append({
#                 "date": current_date.strftime('%Y-%m-%d'),
#                 "time": study_time,
#                 "subject": subject['name'],
#                 "flashcard": flashcard
#             })
#             flashcards_allocated += 1

#         # Move to the next study day for this subject
#         study_day = subject['study_day']
#         current_date += timedelta(days=(study_day - current_date.weekday() + 7) % 7)

#     return jsonify(schedule=schedule), 200


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
