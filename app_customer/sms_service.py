# sms_service.py
import requests

EMAIL = 'abdiarimovfarhod2109@gmail.com'
PASSWORD = 'U2scC3eCcOAahLIcZsxawY8Tqa5vwCZwfQb76KDZ'

def get_token():
    """Authenticate and get the API token."""
    url = 'https://notify.eskiz.uz/api/auth/login'
    data = {'email': EMAIL, 'password': PASSWORD}
    response = requests.post(url, data=data)
    response_data = response.json()
    if response.status_code == 200 and 'data' in response_data:
        return response_data['data']['token']
    else:
        raise Exception(f"Failed to get token: {response_data.get('message', 'Unknown error')}")

def send_sms(phone, message):
    """Send SMS using Eskiz API."""
    token = get_token()
    url = 'https://notify.eskiz.uz/api/message/sms/send'
    headers = {'Authorization': f'Bearer {token}'}
    
    # Use one of the predefined allowed messages
    
    
    data = {
        'mobile_phone': phone,
        'message': message,
        'from': '4546',  # Validated sender name
        'callback_url': 'http://your_callback_url.uz'  # Optional
    }
    
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        print("SMS successfully sent.")
    else:
        raise Exception(f"Failed to send SMS: {response.json()}")
