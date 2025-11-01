# main.py
from fastapi import FastAPI
from routes import violation

app = FastAPI()

# Route root
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# Include router từ file routes/items.py
app.include_router(violation.router)
