class CaptchaError(Exception):
    def __init__(self) -> None:
        super().__init__('Google CAPTCHA has been detected!')
        
class ResultsError(Exception):
    def __init__(self) -> None:
        super().__init__('List empty. No content found.')