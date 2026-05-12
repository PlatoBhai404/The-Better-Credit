from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "The Better Credit API is Live", "market": "India"}

@app.get("/check-reward")
def check_reward(card: str, amount: float):
    # We will build the logic here soon!
    return {"card": card, "estimated_reward": amount * 0.05}