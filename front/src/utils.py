import requests

FASTAPI_URL = "http://localhost:8000"


def get_current_user(token):
    resp = requests.get(
        f"{FASTAPI_URL}/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    if resp.status_code == 200:
        return resp.json()
    return None


def get_login_reponse(user_email, user_password):
    return requests.post(
        f"{FASTAPI_URL}/auth/jwt/login",
        data={"username": user_email, "password": user_password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
