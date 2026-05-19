from fastapi import APIRouter
from backend.schemas.card import CardCreate

router = APIRouter(
    prefix="/cards",
    tags=["Cards"]
)

# In-memory storage for now — we'll replace this with a database later
cards_db = []

@router.post("/")
def add_card(card: CardCreate):
    card_dict = card.model_dump()
    card_dict["id"] = len(cards_db) + 1
    cards_db.append(card_dict)
    return {"message": "Card added successfully!", "card": card_dict}

@router.get("/")
def get_cards():
    return {"cards": cards_db}