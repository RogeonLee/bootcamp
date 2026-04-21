from pydantic import BaseModel

class SignupRequest(BaseModel):
    email: str
    password: str # plantext password, not hashed password
    
    
    