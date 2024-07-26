from src.auth.domain import models
from src.utils import hash as h


class UsersManager:
    def signup(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
    ) -> models.User:
        user = models.User(
            email=email,
            password_hash=h.bcrypt(password),
            first_name=first_name,
            last_name=last_name,
        )
        return user
