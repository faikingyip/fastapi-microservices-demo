class AppServiceError(Exception):
    """Errors raised due to system errors such as a
    loss in database connection, are raised using this
    class."""

    def __init__(self, message, data: dict):
        super().__init__(message)
        self.data = data


class BusinessValidationError(Exception):
    """Represents errors related to business validation,
    such as email already in use during sign up.
    These errors are different from the data validation
    errors caught by pydantic."""

    def __init__(self):
        self.errorKeys = {}

    def add_error(self, key, message, data):
        """Sets the error key.
        The key is the identifier for the type
        of error and the message and data
        are the details of the error associated
        with the key. If the key does not already
        exist then it will be created. If the key
        already exists then it will be assigned a
        new object value."""
        self.errorKeys[key] = {
            "message": message,
            "data": data,
        }
