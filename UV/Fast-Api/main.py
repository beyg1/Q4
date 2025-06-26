from fastapi import FastAPI

app = FastAPI()

@app.get("/")     # This decorator defines a GET endpoint at the root URL ("/")
def read_root():  # This function handles requests to the root endpoint
    return {"Hello": "World"} # Returns a JSON response with a greeting


@app.get("/items/{item_id}")  # This decorator defines a GET endpoint with a path parameter 'item_id'
def read_item(item_id: int, q: str | None = None): # This function handles requests to the '/items/{item_id}' endpoint, with an optional query parameter 'q'
    return {"item_id": item_id, "q": q}  # Returns a JSON response with the item_id and the value of 'q'