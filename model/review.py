
from datetime import datetime
from sqlalchemy import DateTime, String, Text
from model.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(primary_key = True)

    review_id: Mapped[str] = mapped_column(String(50), unique=True)
    stars: Mapped[float]
    text: Mapped[str] = mapped_column(Text)
    date: Mapped[datetime] = mapped_column(DateTime)
    processed_review = relationship("ProcessedReview", back_populates="review", uselist=False)