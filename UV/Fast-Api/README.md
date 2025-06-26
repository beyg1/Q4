uv init
uv add "fastapi[standard]" -- standard for uvicorn & httpx.
Create your first API route.
Run Server -- uv run fastapi dev main.py
api endpoints work. but realise there is validation/schema errors
reason is because we did'nt use pydantic.