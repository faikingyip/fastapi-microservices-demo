from src.accounts.domain import models


class AccountsManager:
    def create_account(
        self,
        user_id: str,
    ) -> models.Account:
        account = models.Account(
            user_id=user_id,
            balance=0,
            version=0,
        )
        return account
