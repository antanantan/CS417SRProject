import requests

BASE_URL = 'http://localhost:5000'

USER_CREDENTIALS ={
    "username": "test_user",
    "email": "test@gmail.com",
    "password": "test_password"
}

def test_register():   
    response = requests.post(f'{BASE_URL}/register', json=USER_CREDENTIALS)
    print("Response:", response.json())

def test_login():
    login_Data = {"username": USER_CREDENTIALS["username"], "password": USER_CREDENTIALS["password"]}
    response = requests.post(f'{BASE_URL}/login', json=login_Data)

    if response.status_code == 200:
        token = response.json().get("token")
        print("Response:", response.json())
        return token
    else:
        print("Login failed", response.json())
        return None
    
def test_profile(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f'{BASE_URL}/profile', headers=headers)
    print("Response:", response.json())

if __name__ == '__main__':
    test_register()
    token = test_login()
    if token:
        test_profile(token)