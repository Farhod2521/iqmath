import requests

def get_token(email, password):
    """Get authentication token from Eskiz API."""
    url = 'https://notify.eskiz.uz/api/auth/login'
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(url, data=data)
    response_data = response.json()
    if response.status_code == 200 and 'data' in response_data:
        return response_data['data']['token']
    else:
        raise Exception(f"Failed to get token: {response_data}")

def send_sms(token, phone, message):
    """Send SMS using Eskiz API."""
    url = 'https://notify.eskiz.uz/api/message/sms/send'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    data = {
        'mobile_phone': phone,
        'message': message,
        'from': '4546',  # Test rejimi uchun tasdiqlangan nom
        'callback_url': 'http://your_callback_url.uz'  # Ixtiyoriy
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print("SMS sent successfully.")
    else:
        print(f"Failed to send SMS: {response.json()}")

if __name__ == '__main__':
    # User credentials for Eskiz API
    email = 'abdiarimovfarhod2109@gmail.com'
    password = 'U2scC3eCcOAahLIcZsxawY8Tqa5vwCZwfQb76KDZ'
    
    # Example usage
    try:
        token = get_token(email, password)
        phone_number = '+998906762920'
        message = 'Bu Eskiz dan test '  # Test matni
        send_sms(token, phone_number, message)
    except Exception as e:
        print(e)



####################   REGISTER ################
{
  "full_name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "998915812109",
  "region": 1,
  "districts": 1,
  "address": "Tashkent, Uzbekistan",
  "brithday": "1990-01-01",
  "academy_or_school": "Litsey",
  "class_name": "10-A"
}
######## VERIFIKATION ##############
{
  "phone": "998915812109",
  "sms_code": "000000"
}
######   LOGIN #############
{
  "phone": "998915812109",
  "password": "IJ6AiGX3"
}



from django.contrib.auth.models import User
User.objects.create_superuser(
    username="998994252521",
    email="example@example.com",
    password="1"
)
