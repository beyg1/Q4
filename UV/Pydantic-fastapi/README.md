uv init
uv add "fastapi[standard]" -- standard for uvicorn & httpx.

create a Basic Pydantic Model in pydantic1.py
run it by uv run pydantic1.py

create an example of Nested Models in pydantic2.py
run it by uv run pydantic2.py

create an example of Custom Validators in pydantic3.py
run it by uv run pydantic3.py

create a full blown fastapi app
run it by fastapi dev main.py

uv add --dev pytest pytest-asyncio to run pytest which tests apis
--dev will make it a dev dependency. it wont be there in production.
uv run pytest test_chat.py -v // can only run pytest, too, as it will check for any
file name begining with test and run scripts named test..

uv add openai-agents to test with pydantic. to get the best out of structured output.
pydantic4 is deep into the concepts so it isnt working for now.
let's try a simpler one in pydantic5