from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes="bcrypt", deprecated="auto")
def bcrypt(self, password: str):
    """
    Performs bcrypt hash on the specified password string.

    - *password* The string to hash
    """
    return pwd_cxt.hash(password)


def verify_bcrypt(self, password: str, hashed_password: str):
    """
    Checks if the plain password and the hashed password is a match.

    - *password* The plain password
    - *hashed_password* The hashed string to check with the plain password
    """
    return pwd_cxt.verify(password, hashed_password)
