import requests
from datetime import datetime
import pytz

utc_time = datetime(2025, 1, 14, 12, 30, 0, tzinfo=pytz.UTC).isoformat()
print(utc_time)
def submit_quiz_result():
    # API endpoint
    url = "https://jetmind.uz/api/v1/quiz/submit-quiz-result/"

    # Token
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM2OTI0ODUyLCJpYXQiOjE3MzY5MTc2NTIsImp0aSI6IjIzNjg1YThkOTk2MzQ2ZmU4OGRlMmEyMDkwNjE2NDA1IiwidXNlcl9pZCI6MTMsInN0dWRlbnRfaWQiOjExfQ.OW2ZU83yOsW1teRvlvbt22tVV0GWVKRXHgc9W5Rp8F8"

    # Authorization header
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # POST so‘rov ma'lumotlari
    data = {
        "answers": [

            {"quiz_id": 7, "answer": "A"},
        ],
        "end_time": "2025-01-14T12:30:00+00:00"
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
