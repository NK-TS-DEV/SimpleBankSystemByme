from models.user import  User
from service.file_manager import FileManager



class Userservice :

    def create_user(self, user_id: int, user_name: str, surname: str)-> User:
        pass

    @staticmethod
    def get_user(user_id: int)-> User:
        return User.get_user_id(user_id)

    # def update_user(self, user_id: int, user_name: str, surname: str)-> User:
    #     pass
    #
    # def delete_user(self, user_id: int)-> None:
    #     pass
    #
    # def edit_user(self, user_name: str, surname: str)-> User:
    #     pass

    @staticmethod
    def register(args):
        users = FileManager.load_all_users()
        new_id = max([u.user_id for u in users], default=0) + 1
        user = User(user_id=new_id, username=args.username, surname=args.surname)
        users.append(user)
        FileManager.save_all_users(users)
        print(f"New user registered: {user.username} {user.surname}, ID: {new_id}")

    @staticmethod
    def login(args):
        users = FileManager.load_all_users()
        user = next((u for u in users if u.user_id == args.user_id), None)
        if user:
            print(f"Hi, {user.username} {user.surname}!")
        else:
            print("User not found")
