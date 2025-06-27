from pydantic import BaseModel, ValidationError

class User(BaseModel): # Define a Pydantic model for a User
    id: int
    name: str
    email: str
    age: int | None = None

user1 = {"id": 1, "name": "Alice", "email": "alice@alice.com", "age": 30} # Example user data as a dictionary
user = User(**user1)  # Create a User instance from the "User" dictionary, double * are used to unpack the dictionary

print(user)  # Print the User instance
print(user.model_dump())  # Print the User instance as a dictionary using model_dump
print(user.model_dump_json())  # Print the User instance as a JSON string using model_dump

# Example of validation error
try:
    user2 = {"id": "not an int", "name": "Bob", "email": "example@example.com", "age": 25}
    user_invalid = User(**user2)  # This will raise a validation error  
except ValidationError as e:
    print("Validation error:", e)