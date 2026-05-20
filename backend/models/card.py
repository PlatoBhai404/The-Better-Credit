from sqlalchemy import Column, Integer, String, Float, ForeignKey
from backend.database import Base

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    bank = Column(String, nullable=False)
    card_type = Column(String, nullable=False)
    default_reward_rate = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)