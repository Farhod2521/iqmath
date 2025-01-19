import requests
from datetime import datetime
import pytz

# UTC vaqtini olish
utc_time = datetime(2025, 1, 14, 12, 30, 0, tzinfo=pytz.UTC).isoformat()

def submit_quiz_result():
    # API endpoint
    url = "http://127.0.0.1:8000/api/v1/quiz/submit-quiz-result/"

    # Token
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM3MjgxNjEwLCJpYXQiOjE3MzcyODEwMTAsImp0aSI6IjU2MjgyYzRmYWE4OTRjYzM4NDU2MmZlMzU3ZjFjZjg2IiwidXNlcl9pZCI6OCwic3R1ZGVudF9pZCI6M30.Mv2iF0NciCuRxBQLdZb-S_GokgivJcKEOLVoIg50O14"

    # Authorization header
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # POST so‘rov ma'lumotlari
    data = {
        "answers": [
            {"quiz_id": 1, "answer": "A"},
            {"quiz_id": 2, "answer": "A"},
            {"quiz_id": 3, "answer": "B"}
        ],
        "random_answers": [
            {"question_id": 1, "score": 2.1},
            {"question_id": 3, "score": 5.1},
            {"question_id": 5, "score": 3.1}
        ],

        "test_time": 30  # Agar test vaqti ham yuborilishi kerak bo'lsa
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
