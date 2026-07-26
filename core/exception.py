class AppException(Exception):
    def __init__(self, status_code: int, error_code: str, message:str, details: dict | None = None):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.details = details or {}

        super().__init__(message)

class PredictionNotFound(AppException):
    def __init__(self, prediction_id) :
        self.prediction_id = prediction_id

        super().__init__(status_code=404, error_code="PREDICTION_NOT_FOUND", message=f"Prediction with id {prediction_id} was not found.", details = {"prediction_id": prediction_id})

class UserAlreadyExists(AppException):
    def __init__(self, information):
        self.information = information

        super().__init__(status_code=409, error_code="USER_ALREADY_EXISTS", message=f"User with {self.information} already exists", details = {"information": information})

class InvalidCredentials(AppException):
        def __init__(self):
            super().__init__(status_code=401, error_code="UNAUTHORIZED", message="Incorrect email or password")

class Forbidden(AppException):
     def __init__(self, role: str):
          self.role = role
          super().__init__(status_code=403, error_code="FORBIDDEN", message="You do not have permission to access this resource.", details={"role": role})
