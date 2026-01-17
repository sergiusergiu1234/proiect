
from typing import Optional, Sequence
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select

from model.review import Review


class ReviewRepository:
    def __init__(self, session: Session):
        self.session = session


    def create(self,
               review_id: str,
               stars: float,
               text: str,
               date: datetime,
               ):
        """Create new review."""
        try:
            review = Review(
                review_id=review_id,
                stars=stars,
                text=text,
                date=date,
            )
            self.session.add(review)
            self.session.commit()
            self.session.flush()
            self.session.refresh(review)
            return review
        except Exception as e:
            self.session.rollback()
            print(f"Error creating review with review_id {review_id}: {str(e)}. Skipping it.")
            return None

    def get_by_review_id(self, review_id: str) -> Optional[Review]:
        stmt = select(Review).where(Review.review_id == review_id)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_all(self, limit: int = 100, offset: int = 0) -> Sequence[Review]:
        stmt = select(Review).limit(limit).offset(offset)
        return self.session.execute(stmt).scalars().all()
