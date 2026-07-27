from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"This is my first api"}


@app.get("/customers")
def get_customer():
    return "get all customers"

