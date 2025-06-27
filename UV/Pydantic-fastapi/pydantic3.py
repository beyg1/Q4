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
        id=1,
        name="A",
        email="alice@alice.com",
        address={
            "street": "123 Main St",
            "city": "New York",
            "zip_code": "10001"
        }
    )
    print("invalid User:", invalid_user) # This will not be printed due to validation error. invalid_user will not have a value
except ValidationError as e: # Catch the validation error
    print("Validation Error:", e) # This will print the validation error message

# Test the User model with valid data
try:
    valid_user = User(
        id=1,
        name="Alice",
        email="alice@alice.com",
        address={
            "street": "123 Main St",
            "city": "New York",
            "zip_code": "10001"
        }
    )
    print("Valid User:", valid_user) # This will print the valid user data
except ValidationError as e: # Catch the validation error
    # This block will not be executed since the data is valid
    print("Validation Error:", e)
    