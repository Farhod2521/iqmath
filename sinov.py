import requests
from datetime import datetime
import pytz

utc_time = datetime(2025, 1, 14, 12, 30, 0, tzinfo=pytz.UTC).isoformat()
print(utc_time)
def submit_quiz_result():
    # API endpoint
    url = "http://127.0.0.1:8000/api/v1/quiz/submit-quiz-result/"

    # Token
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM3MDM5NzgxLCJpYXQiOjE3MzcwMzI1ODEsImp0aSI6ImJhMzdkNTAxODM2ZDQ5YzY5MWFhNWFiMjFkOTViMjUwIiwidXNlcl9pZCI6Nywic3R1ZGVudF9pZCI6Mn0.JOJWYvMRGz44I0NVfiWO_bImhbhf5pR3C0bVTuHF6fI"

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
            {"quiz_id": 3, "answer": "B"},
        ],
        "end_time": "2025-01-16T13:30:00+00:00"
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
