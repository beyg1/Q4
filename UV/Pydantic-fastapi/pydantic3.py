from pydantic import BaseModel, EmailStr, ValidationError, field_validator

class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    address: Address

    @field_validator('name') # field_validator is used to validate custom fields (Custom Validation)
    def validate_name_greaterthan_2_characters(cls, value): # cls is the class itself, value is the value of the field
        """Validate that the name is greater than 2 characters."""
        if len(value) < 2:
            raise ValueError('Name must be greater than 2 characters')
        return value
    
# Test the User model with valid data
try:
    invalid_user = User( 
        id: 1,
        name: "A",
        "email": "alice@alice.com",
        "age": 30,
        "address": {
            "street": "123 Main St",
            "city": "New York",
            "zip_code": "10001"
        }
    )
except ValidationError as e:
    print("Validation Error:", e)       