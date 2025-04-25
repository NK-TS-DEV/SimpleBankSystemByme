from models.account import Bankaccount
from service.file_manager import FileManager

class AccountService:

    @staticmethod
    def create_bank_account(account_id: int, initial_balance: float = 0.0, currency: str = "USD") -> Bankaccount:
        return Bankaccount(account_id, initial_balance, currency)

    @staticmethod
    def deposit_to_account(account: Bankaccount, amount: float, currency: str) -> None:
        return account.deposit(amount, currency)

    @staticmethod
    def withdraw_from_account(account: Bankaccount, amount: float, currency: str) -> bool:
        return account.withdraw(amount, currency)

    @staticmethod
    def transfer_between_accounts(from_account: Bankaccount, to_account: Bankaccount, amount: float, currency: str) -> bool:
        return from_account.transfer(to_account, amount, currency)

    @staticmethod
    def withdraw(args):
        users = FileManager.load_all_users()
        user = next((u for u in users if u.user_id == args.user_id), None)
        if not user:
            print("User not found")
            return

        account = user.get_account_by_id(args.account_id)
        if account:
            result = account.withdraw(args.amount, account.currency)
            FileManager.save_all_users(users)
            print(f"💸 {result}")
        else:
            print("Account not found")







    @staticmethod
    def create_account(args):
        users = FileManager.load_all_users()
        user = next((u for u in users if u.user_id == args.user_id), None)
        if not user:
            print("❌ Користувача не знайдено")
            return

        account = Bankaccount(account_id=args.account_id, balance=0.0, currency=args.currency)
        user.accounts.append(account)
        FileManager.save_all_users(users)
        print(f"🏦 Створено рахунок ID {args.account_id} для користувача {user.username}")

    @staticmethod
    def deposit(args):
        users = FileManager.load_all_users()
        user = next((u for u in users if u.user_id == args.user_id), None)
        if not user:
            print("❌ Користувача не знайдено")
            return

        account = user.get_account_by_id(args.account_id)
        if account:
            account.deposit(args.amount, account.currency)  # <-- ВАЖНО! Прямой вызов метода у объекта
            FileManager.save_all_users(users)
            print(f"💰 Поповнено рахунок {args.account_id} на {args.amount}")
        else:
            print("❌ Рахунок не знайдено")

    @staticmethod
    def transfer(args):
        users = FileManager.load_all_users()
        user = next((u for u in users if u.user_id == args.user_id), None)
        if not user:
            print("❌ Користувача не знайдено")
            return

        from_acc = user.get_account_by_id(args.from_id)
        to_acc = user.get_account_by_id(args.to_id)
        if from_acc and to_acc:
            result = from_acc.transfer(to_acc, args.amount, from_acc.currency)
            FileManager.save_all_users(users)
            print(result)
        else:
            print("❌ Один із рахунків не знайдено")
