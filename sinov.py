import requests

def submit_quiz_result():
    # API endpoint
    url = "http://127.0.0.1:8000/api/v1/quiz/submit-quiz-result/"

    # Token
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM2OTI0NjYxLCJpYXQiOjE3MzY5MTc0NjEsImp0aSI6IjBkYWI5ODkwNTViNzQ2NjVhZDZlZDQzMGIyMDg0NDIzIiwidXNlcl9pZCI6Nywic3R1ZGVudF9pZCI6Mn0.8DgqFaaULyL8AlIdvKdqlK5ez7FTBNaB4zqBCCAp9lQ"

    # Authorization header
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # POST so‘rov ma'lumotlari
    data = {
        "answers": [
            {"quiz_id": 1, "answer": "B"},
            {"quiz_id": 2, "answer": "A"},
            {"quiz_id": 3, "answer": "A"},
        ],
        "end_time": "2025-01-14T12:30:00Z"
    }

    # POST so‘rov yuborish
    response = requests.post(url, headers=headers, json=data)

    # Natijani chop qilish
    if response.status_code == 201:
        print("Natija muvaffaqiyatli yuborildi:", response.json())
    else:
        print(f"Xatolik yuz berdi: {response.status_code}")
        print("Ma'lumot:", response.text)

# Funksiyani chaqirish
submit_quiz_result()
