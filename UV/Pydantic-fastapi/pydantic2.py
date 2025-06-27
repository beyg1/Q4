from pydantic import BaseModel, EmailStr

# Pydantic supports nested models, which allows you to create complex data structures.

class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int | None = None
    address: Address | None = None  # Nested model for address

# Example user data with nested address
user = {
    "id": 1,
    "name": "Alice",
    "email": "alice@alice.com",
    "age": 30,
    "address": {"street": "123 Main St", "city": "NewYork", "zip_code": "10"} # Nested dictionary from Address Class
       }

user_instance = User.model_validate(user)  # model_validate is used to validate and parse the data before creating an instance
print(user_instance.model_dump())          # also don't need ** for model_validate