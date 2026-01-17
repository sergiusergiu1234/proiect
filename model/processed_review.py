from sqlalchemy import Boolean, ForeignKey, String, Text
from model.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class ProcessedReview(Base):
    __tablename__ = 'processed_review'

    id: Mapped[int] = mapped_column(primary_key=True)

    review_id: Mapped[str] = mapped_column(String(50), ForeignKey("review.review_id"), unique=True)
    summary: Mapped[str] = mapped_column(Text)
    passed_halucination_check: Mapped[bool] = mapped_column(Boolean, nullable=True)
    actual_halucination_check_response: Mapped[str] = mapped_column(String(50), nullable=True)
    llm_sentiment: Mapped[str] = mapped_column(String(50))
    dl_sentiment: Mapped[str] = mapped_column(String(50), nullable=True)
    
    review = relationship("Review", back_populates="processed_review")
    