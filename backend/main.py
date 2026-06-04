from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import cards, suggest, auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cards.router)
app.include_router(suggest.router)
app.include_router(auth.router)