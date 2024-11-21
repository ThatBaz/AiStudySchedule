from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from flask_migrate import Migrate
from database import Subject, db, User

app = Flask(__name__)
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
    current_user_id = get_jwt_identity()
    return jsonify({'message': 'Token is valid', 'user_id': current_user_id}), 200

@app.route('/user_data', methods=['GET'])
@jwt_required()
def get_user_data():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
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
                    'name': subject.name,
                    'progress': subject.progress,
                    'flashcards_total': subject.total_flashcards,
                    'flashcards_studied': subject.completed_flashcards
                } for subject in current_user.subjects
            ]
        }
        return jsonify(user_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)