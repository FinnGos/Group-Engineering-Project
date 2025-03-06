class NotEnoughPoints(Exception):
    """Exception raised when subtracting too many points
    
    Attributes:
        message (str): Explanation of the error message (default message if not provided)
        error_code (int): Custom error code for backend processing (not HTTP-related)
    """
    
    def __init__(self, message="Not enough points to subtract", error_code=None):
        #I am not sure if we need an error code, but we can set it if needed
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)  # pass the message up
        
    def __str__(self):
        return f"{self.message} (Error Code: {self.error_code})"

class NegativePoints(Exception):
    """Exception raised when adding or subtracting negative points for consistency
    
    Attributes:
        message (str): Flag the problem when logged
        error_code (int): custom error code incase required for processing"""
    def __init__(self, message="Please do not use negative points", error_code=None):
        self.message = message 
        self.error_code = error_code
        super().__init__(self.message) #pass the message up
        
    def __str__(self):
        return f"{self.message} (Error Code: {self.error_code})"