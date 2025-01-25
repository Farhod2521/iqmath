import requests

# URL manzili
url = "https://jetmind.uz/api/v1/quiz/submit-quiz-result/"

# Bearer token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM3ODAzMDQzLCJpYXQiOjE3Mzc3OTIyNDMsImp0aSI6IjU5MmU2NTdhNjQyMzQ2NGQ4YzBmYzZjZjhiNDcxZjM1IiwidXNlcl9pZCI6NTYsInN0dWRlbnRfaWQiOjU0fQ.F5__yR741iELgzXqDvDLVrZ8TQjfbte98i2-P4TaWio"

# So'rov sarlavhalari
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Yuboriladigan ma'lumotlar
data = {
    "answers": [
        {"quiz_id": 5, "answer": "A"}, 
        {"quiz_id": 6, "answer": "B"}, 
        {"quiz_id": 9, "answer": "D"}
    ],
    "test_time": 26
}

# POST so'rovi
response = requests.post(url, headers=headers, json=data)

# Javobni chiqarish
print("Status code:", response.status_code)
print("Response data:", response.json())