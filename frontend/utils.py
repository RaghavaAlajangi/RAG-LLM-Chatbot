import os

import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:1050")


def get_current_user(token):
    resp = requests.get(
        f"{BACKEND_URL}/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    if resp.status_code == 200:
        return resp.json()
    return None


def get_login_reponse(user_email, user_password):
    return requests.post(
        f"{BACKEND_URL}/auth/jwt/login",
        data={"username": user_email, "password": user_password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )


def get_signup_response(user_email, user_password):
    response = requests.post(
        f"{BACKEND_URL}/auth/register",
        json={"email": user_email, "password": user_password},
        headers={"Content-Type": "application/json"},
    )
    return response.status_code


def get_model_list():
    response = requests.get(f"{BACKEND_URL}/rag/models")
    if response.status_code == 200:
        return response.json()
    return None


def get_chat_response(token, model_name, chat_history):
    response = requests.post(
        f"{BACKEND_URL}/rag/chat",
        json={
            "model": model_name,
            "chat_history": chat_history,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.status_code == 200:
        return response.json()
    return None


def fetch_chat(token, chat_id):
    response = requests.get(
        f"{BACKEND_URL}/chat_db/fetch_chat/{chat_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.status_code == 200:
        return response.json()
    return None


def update_chat(token, chat_id, messages):
    response = requests.post(
        f"{BACKEND_URL}/chat_db/update_chat/{chat_id}",
        json={"messages": messages},
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.status_code == 200:
        return response.json()
    return None


def get_chat_list(token):
    response = requests.get(
        f"{BACKEND_URL}/chat_db/list_chats",
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.status_code == 200:
        return response.json()
    return []
