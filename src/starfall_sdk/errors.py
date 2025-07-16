class StarFallSDKError(Exception):
    def __init__(self, message: str, status_code: int, *args: object) -> None:
        super().__init__(message, *args)

        self.status_code = status_code
        self.message = message
