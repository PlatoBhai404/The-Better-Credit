from pydantic import BaseModel
from typing import Optional

class CardCreate(BaseModel):
    name: str                    # e.g. "HDFC Regalia"
    bank: str                    # e.g. "HDFC"
    card_type: str               # e.g. "cashback" or "travel"
    default_reward_rate: float   # e.g. 1.5 (meaning 1.5% cashback)