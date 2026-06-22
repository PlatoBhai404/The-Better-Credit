from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.card import Card
from backend.models.user import User
from backend.models.user_card import UserCard
from backend.auth_utils import get_current_user
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/cards",
    tags=["Cards"]
)

class CardRequest(BaseModel):
    card_name: str
    bank: str
    card_type: Optional[str] = None
    requested_by: Optional[str] = None

# Get user's wallet
@router.get("/")
def get_wallet(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_cards = db.query(UserCard).filter(UserCard.user_id == current_user.id).all()
    
    result = []
    for uc in user_cards:
        card = db.query(Card).filter(Card.id == uc.card_id).first()
        if card:
            result.append({
                "id": uc.id,
                "card_id": card.id,
                "name": card.name,
                "bank": card.bank,
                "card_type": card.card_type
            })
    return result

# Add card to wallet
@router.post("/")
def add_to_wallet(card_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    existing = db.query(UserCard).filter(UserCard.user_id == current_user.id, UserCard.card_id == card_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Card already in wallet")
    user_card = UserCard(user_id=current_user.id, card_id=card_id)
    db.add(user_card)
    db.commit()
    return {"message": "Card added to wallet"}

# Remove card from wallet
@router.delete("/{user_card_id}")
def remove_from_wallet(user_card_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_card = db.query(UserCard).filter(UserCard.id == user_card_id, UserCard.user_id == current_user.id).first()
    if not user_card:
        raise HTTPException(status_code=404, detail="Card not found in wallet")
    db.delete(user_card)
    db.commit()
    return {"message": "Card removed from wallet"}

# Search master card list
@router.get("/search")
def search_cards(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    cards = db.query(Card).filter(Card.name.ilike(f"%{q}%")).all()
    return cards

# Get all cards
@router.get("/all")
def get_all_cards(db: Session = Depends(get_db)):
    return db.query(Card).all()

# Request a new card
@router.post("/request")
def request_card(payload: CardRequest, db: Session = Depends(get_db)):
    from sqlalchemy import text
    db.execute(text("""
        INSERT INTO card_requests (card_name, bank, card_type, requested_by)
        VALUES (:card_name, :bank, :card_type, :requested_by)
    """), {
        "card_name": payload.card_name,
        "bank": payload.bank,
        "card_type": payload.card_type,
        "requested_by": payload.requested_by
    })
    db.commit()
    return {"message": "Card request submitted. We'll add it within 24 hours!"}