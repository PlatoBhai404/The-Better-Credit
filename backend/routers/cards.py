
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.card import Card
from backend.models.user import User
from backend.schemas.card import CardCreate
from backend.auth_utils import get_current_user

router = APIRouter(
    prefix="/cards",
    tags=["Cards"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def add_card(card: CardCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_card = Card(
        name=card.name,
        bank=card.bank,
        card_type=card.card_type,
        default_reward_rate=card.default_reward_rate,
        user_id=user.id
    )
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return {"message": "Card added successfully!", "card": new_card}

@router.get("/")
def get_cards(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cards = db.query(Card).filter(Card.user_id == user.id).all()
    return {"cards": cards}