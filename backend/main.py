from fastapi import FastAPI
from backend.routers import cards, suggest, auth

app = FastAPI(
    title="The Better Credit",
    description="India's smartest credit card reward optimizer",
    version="0.1.0"
)

app.include_router(cards.router)
app.include_router(suggest.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to The Better Credit API 🚀"}