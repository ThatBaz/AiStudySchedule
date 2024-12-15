import os
import PyPDF2
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from flask_migrate import Migrate
from database import Subject, db, User
import logging
from flask_jwt_extended.exceptions import NoAuthorizationError

# Initialize the Flask application
app = Flask(__name__)

# Configure application settings
app.config['JWT_SECRET_KEY'] = '7aM4/3Vj3Uv+'  # Change this to a secure random key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/study_schedule_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Enable CORS for cross-origin requests
CORS(app)

# Initialize SQLAlchemy and Flask-Migrate
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
    """
    Handles user registration.
    
    :return: JSON response with success message or error details.
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        required_fields = ['name', 'email', 'password', 'study_hours', 'study_time']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "User with this email already exists"}), 409
        
        hashed_password = generate_password_hash(data['password'])
        new_user = User(
            name=data['name'],
            email=data['email'],
            password=hashed_password,
            study_hours=data['study_hours'],
            study_time=data['study_time']
        )

        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Registered successfully'}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    """
    Handles user login.
    
    :return: JSON response with access token or error details.
    """
    try:
        data = request.json
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        

        user = User.query.filter_by(email=data['email']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401

        token = create_access_token(identity=user.id)
        return jsonify({'token': token, 'user_id': user.id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/verify_token', methods=['POST'])
@jwt_required()
def verify_token():
    """
    Verifies the JWT token provided in the request.
    
    :return: JSON response confirming token validity.
    """
    current_user_id = get_jwt_identity()
    return jsonify({'message': 'Token is valid', 'user_id': current_user_id}), 200

@app.route('/add_subject', methods=['POST'])
@jwt_required()
def add_subject():
    """
    Adds a new subject for the authenticated user.
    
    :return: JSON response with subject details and generated flashcards.
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    name = request.form.get('name')
    allocated_day = request.form.get('allocatedDay')
    file = request.files.get('file')
    

    if not name or not allocated_day or not file:
        return jsonify({"error": "Missing required fields"}), 400
    

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    

    # Generate flashcards from PDF
    flashcards = generate_flashcards_from_pdf(file_path)
    

    new_subject = Subject(
        name=name,
        allocated_day=allocated_day,
        user_id=current_user_id,
        total_flashcards=len(flashcards),
        completed_flashcards=0,
        progress=0
    )
    

    db.session.add(new_subject)
    db.session.commit()
    

    # Here you would typically save the flashcards to the database
    # For simplicity, we're just returning them
    return jsonify({
        "id": new_subject.id,
        "name": new_subject.name,
        "allocated_day": new_subject.allocated_day,
        "progress": new_subject.progress,
        "flashcards_total": new_subject.total_flashcards,
        "flashcards_studied": new_subject.completed_flashcards,
        "flashcards": flashcards
    }), 201

def generate_flashcards_from_pdf(file_path):
    """
    Generates flashcards from a given PDF file.
    
    :param file_path: Path to the PDF file
    :return: List of dictionaries containing flashcard questions and answers
    """
    flashcards = []
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            # This is a very simple flashcard generation.
            # In a real application, you'd want to use more sophisticated NLP techniques.
            sentences = text.split('.')
            for i in range(0, len(sentences), 2):
                if i + 1 < len(sentences):
                    question = sentences[i].strip()
                    answer = sentences[i+1].strip()
                    if question and answer:
                        flashcards.append({"question": question, "answer": answer})
    return flashcards

@app.route('/test_user_data/<int:user_id>', methods=['GET'])
def get_test_user_data(user_id):
    """
    Retrieves test user data for a given user ID.
    
    :param user_id: Integer representing the user ID
    :return: JSON response with user data
    """
    try:
        current_user = User.query.get(user_id)
        if not current_user:
            return jsonify({'error': 'User not found'}), 404

        user_data = {
            'id': current_user.id,
            'name': current_user.name,
            'email': current_user.email,
            'study_hours': current_user.study_hours,
            'study_time': current_user.study_time,
            'subjects': [
                {
                    'id': subject.id,
                    'name': subject.name,
                    'progress': subject.progress,
                    'flashcards_total': subject.total_flashcards,
                    'flashcards_studied': subject.completed_flashcards,
                    'allocated_day': subject.allocated_day
                } for subject in current_user.subjects
            ]
        }
        return jsonify(user_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

## Test function below, keep commented for now.

# @app.route('/user_data', methods=['GET'])
# @jwt_required()
# def get_user_data():
#     try:
#         logging.debug("Attempting to get user data")
#         current_user_id = get_jwt_identity()
#         logging.debug(f"Current user ID: {current_user_id}")
#         current_user = User.query.get(current_user_id)
#         if not current_user:
#             logging.error(f"User not found for ID: {current_user_id}")
#             return jsonify({'error': 'User not found'}), 404

#         user_data = {
#             'id': current_user.id,
#             'name': current_user.name,
#             'email': current_user.email,
#             'study_hours': current_user.study_hours,
#             'study_time': current_user.study_time,
#             'subjects': [
#                 {
#                     'name': subject.name,
#                     'progress': subject.progress,
#                     'flashcards_total': subject.total_flashcards,
#                     'flashcards_studied': subject.completed_flashcards
#                 } for subject in current_user.subjects
#             ]
#         }
#         logging.debug(f"User data retrieved: {user_data}")
#         return jsonify(user_data), 200
#     except NoAuthorizationError:
#         logging.error("No authorization token provided")
#         return jsonify({'error': 'No authorization token provided'}), 401
#     except Exception as e:
#         logging.error(f"Error in get_user_data: {str(e)}")
#         return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
