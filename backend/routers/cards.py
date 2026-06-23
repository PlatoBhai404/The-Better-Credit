from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.card import Card
from backend.models.user import User
from backend.models.user_card import UserCard
from backend.models.card_request import CardRequest
from backend.auth_utils import get_current_user
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/cards",
    tags=["Cards"]
)

class AddCardToWalletRequest(BaseModel):
    card_id: int

class RequestNewCardSchema(BaseModel):
    card_name: str

# ── Wallet ───────────────────────────────────────────────────────────────────

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

@router.delete("/{user_card_id}")
def remove_from_wallet(user_card_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_card = db.query(UserCard).filter(UserCard.id == user_card_id, UserCard.user_id == current_user.id).first()
    if not user_card:
        raise HTTPException(status_code=404, detail="Card not found in wallet")
    db.delete(user_card)
    db.commit()
    return {"message": "Card removed from wallet"}

# ── Search ───────────────────────────────────────────────────────────────────

@router.get("/search")
def search_cards(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    cards = db.query(Card).filter(Card.name.ilike(f"%{q}%")).all()
    return cards

@router.get("/all")
def get_all_cards(db: Session = Depends(get_db)):
    return db.query(Card).all()

# ── Card request ──────────────────────────────────────────────────────────────

@router.post("/request")
def request_card(
    payload: RequestNewCardSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check for duplicate pending request from this user for the same card
    existing = db.query(CardRequest).filter(
        CardRequest.user_id == current_user.id,
        CardRequest.card_name == payload.card_name,
        CardRequest.status == "pending"
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="You already have a pending request for this card")

    new_request = CardRequest(
        card_name=payload.card_name,
        user_id=current_user.id,
    )
    db.add(new_request)
    db.commit()
    return {"message": "Request submitted. We'll review and add it within 24 hours."}