class CustomException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class EmailAlreadyExistsException(CustomException):
    def __init__(self):
        super().__init__(
            message="Email already exists",
            status_code=400
        )


class UserNotFoundException(CustomException):
    def __init__(self):
        super().__init__(
            message="User not found",
            status_code=404
        )        