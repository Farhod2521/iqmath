import requests
from requests.exceptions import RequestException

def submit_quiz_result(api_url, token, quiz_id, end_time):
    """Submit quiz results with error handling."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "quiz_id": quiz_id,
        "answers": [
    {"quiz_id": 1, "answer": "A"},
    {"quiz_id": 2, "answer": "A"},
    {"quiz_id": 2, "answer": "A"},
],
        "end_time": end_time
    }

    try:
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except RequestException as e:
        print(f"Error submitting quiz result: {e}")
        return {"error": "Failed to submit quiz result"}

# Example usage
api_url = "http://127.0.0.1:8000/api/v1/quiz/submit-quiz-result/"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM2Njg3OTg3LCJpYXQiOjE3MzY2ODA3ODcsImp0aSI6IjllMzQ4NjMzYThiNjRmMWI4MzFhN2UyNWFjMTQwN2Q1IiwidXNlcl9pZCI6Nywic3R1ZGVudF9pZCI6Mn0.2QxXMARm2XGj2lT2f4qEBTkOTLxDPu_wb7RyArcEZoU"
quiz_id = 1

end_time = "2025-01-12T12:00:00Z"

result = submit_quiz_result(api_url, token, quiz_id, end_time)
print(result)
