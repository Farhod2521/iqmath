import requests

# API endpoint
url = "https://jetmind.uz/api/v1/student/profile/"

# Bearer token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM3Mzk3ODgxLCJpYXQiOjE3MzczODcwODEsImp0aSI6IjE5MTMwNDg5M2ZhYjRiZDU4YTVhY2NhMGQxMjI3MGRkIiwidXNlcl9pZCI6NTYsInN0dWRlbnRfaWQiOjU0fQ.KJaC2sNRNFNVcpBSFZQmh1PXuR8LvD77-vKEVWyKO48"

# So'rov sarlavhalari
headers = {
    "Authorization": f"Bearer {token}",
}

# GET so'rovini yuborish
response = requests.get(url, headers=headers)

# Javobni tekshirish
if response.status_code == 200:
    print("Muvaffaqiyatli so'rov:")
    print(response.json())  # JSON javobni ko'rsatadi
else:
    print(f"Xatolik yuz berdi: {response.status_code}")
    print(response.text)
