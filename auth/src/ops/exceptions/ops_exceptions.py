class OpsBaseError(Exception):
    def __init__(self, original_exception):
        super().__init__(str(original_exception))


class CreateUserError(OpsBaseError):
    def __init__(self, original_exception):
        super().__init__(str(original_exception))


class DeleteUserError(OpsBaseError):
    def __init__(self, original_exception):
        super().__init__(str(original_exception))


class ChangePasswordError(OpsBaseError):
    def __init__(self, original_exception):
        super().__init__(str(original_exception))


class GetUserListError(OpsBaseError):
    def __init__(self, original_exception):
        super().__init__(str(original_exception))


class GetUserByIdError(OpsBaseError):
    def __init__(self, original_exception):
        super().__init__(str(original_exception))


class GetUserByUsernameError(OpsBaseError):
    def __init__(self, original_exception):
        super().__init__(str(original_exception))
