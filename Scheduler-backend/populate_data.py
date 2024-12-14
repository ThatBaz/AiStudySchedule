from database import db, User, Subject
from app import app
from datetime import datetime, timezone

def populate_user_data():
    with app.app_context():
        # Check if user 1 exists, if not create it
        user = User.query.get(1)
        if not user:
            user = User(
                id=1,
                name="John Doe",
                email="john@example.com",
                study_hours=4,
                study_time="14:00"
            )
            user.set_password("password123")
            db.session.add(user)
            db.session.commit()

        # Create subjects with flashcards
        subjects = [
            {
                "name": "Mathematics",
                "allocated_day": "Monday",
                "flashcards": [
                    {"question": "What is 2 + 2?", "answer": "4"},
                    {"question": "What is the square root of 16?", "answer": "4"},
                    {"question": "What is the formula for the area of a circle?", "answer": "πr²"}
                ]
            },
            {
                "name": "History",
                "allocated_day": "Wednesday",
                "flashcards": [
                    {"question": "Who was the first President of the United States?", "answer": "George Washington"},
                    {"question": "In what year did World War II end?", "answer": "1945"},
                    {"question": "What was the name of the ship that brought the Pilgrims to America?", "answer": "Mayflower"}
                ]
            },
            {
                "name": "Biology",
                "allocated_day": "Friday",
                "flashcards": [
                    {"question": "What is the powerhouse of the cell?", "answer": "Mitochondria"},
                    {"question": "What is the process by which plants make their food?", "answer": "Photosynthesis"},
                    {"question": "What is the largest organ in the human body?", "answer": "Skin"}
                ]
            }
        ]

        for subject_data in subjects:
            subject = Subject(
                name=subject_data["name"],
                allocated_day=subject_data["allocated_day"],
                user_id=user.id,
                total_flashcards=len(subject_data["flashcards"]),
                completed_flashcards=0,
                progress=0,
                flashcards=subject_data["flashcards"],
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            db.session.add(subject)

        db.session.commit()
        print("User data populated successfully!")

if __name__ == "__main__":
    populate_user_data()