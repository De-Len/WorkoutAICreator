class ApplicationError(Exception):
    """Базовое исключение приложения"""
    pass

class ProfileNotFoundError(ApplicationError):
    def __init__(self, session_id: str):
        self.session_id = session_id
        super().__init__(f"Profile with session_id {session_id} not found")

class IncompleteProfileError(ApplicationError):
    def __init__(self):
        super().__init__("Profile is not complete")

class LLMServiceError(ApplicationError):
    def __init__(self, message: str):
        super().__init__(f"LLM service error: {message}")