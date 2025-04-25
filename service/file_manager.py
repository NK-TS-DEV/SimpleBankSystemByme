import os
import json
from models.user import User

class FileManager:
    USERS_FILE = 'data/users.json'

    @staticmethod
    def save_all_users(users: list[User]) -> None:
        os.makedirs('data', exist_ok=True)
        data = [user.to_dict() for user in users]
        with open(FileManager.USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def load_all_users() -> list[User]:
        if not os.path.exists(FileManager.USERS_FILE):
            return []
        with open(FileManager.USERS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return [User.from_dict(user_data) for user_data in data]
