"""Custom errors that will be handled by the middleware.
These errors should not be caught by the calling code
when raised. Instead, we let them propagate to the
middleware, which can handle all types of CustomError
generically."""

from abc import ABC, abstractmethod


class CustomError(Exception, ABC):
    def __init__(self):
        super().__init__()

    @property
    def status_code(self):
        pass

    @abstractmethod
    def detail(self):
        pass


class AppServiceError(CustomError):
    """Errors raised due to system errors such as a
    loss in database connection, are raised using this
    class."""

    def __init__(self, message, data):
        self.message = message
        self.data = data
        super().__init__()

    @property
    def status_code(self):
        return 500

    def detail(self):
        return [
            {
                "msg": self.message,
                "data": self.data,
            },
        ]


class BusinessValidationError(CustomError):
    """Represents errors related to business validation,
    such as email already in use during sign up.
    These errors are different from the data validation
    errors caught by pydantic."""

    def __init__(self):
        super().__init__()
        self.error_keys = {}

    def add_error(self, key, message, data):
        """Sets the error key.
        The key is the identifier for the type
        of error and the message and data
        are the details of the error associated
        with the key. If the key does not already
        exist then it will be created. If the key
        already exists then it will be assigned a
        new object value."""
        self.error_keys[key] = {
            "msg": message,
            "data": data,
        }

    @property
    def status_code(self):
        return 400

    def detail(self):
        return [
            self.error_keys,
        ]


class UnauthorizedError(CustomError):
    """Errors raised due to resource unauthorized."""

    def __init__(self, message):
        self.message = message
        super().__init__()

    @property
    def status_code(self):
        return 401

    def detail(self):
        return [
            {
                "msg": self.message,
            },
        ]


class NotFoundError(CustomError):
    """Errors raised due to resource not found."""

    def __init__(self, message):
        self.message = message
        super().__init__()

    @property
    def status_code(self):
        return 404

    def detail(self):
        return [
            {
                "msg": self.message,
            },
        ]
