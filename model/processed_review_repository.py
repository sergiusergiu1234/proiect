from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional

from model.processed_review import ProcessedReview


class ProcessedReviewRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self,
               review_id: str,
               summary: str,
               passed_halucination_check: bool,
               llm_sentiment: str,
               dl_sentiment: str
               ):
        """Create new processed review."""
        try:
            processed_review = ProcessedReview(
                review_id=review_id,
                summary=summary,
                passed_halucination_check=passed_halucination_check,
                llm_sentiment=llm_sentiment,
                dl_sentiment=dl_sentiment
            )
            self.session.add(processed_review)
            self.session.commit()
            self.session.flush()
            self.session.refresh(processed_review)
            return processed_review
        except Exception as e:
            self.session.rollback()
            print(f"Error creating processed review for review_id {review_id}: {str(e)}. Skipping it.")
            return None

    def get_by_review_id(self, review_id: str) -> Optional[ProcessedReview]:
        """Get processed review by review_id."""
        stmt = select(ProcessedReview).where(ProcessedReview.review_id == review_id)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_all(self, limit: int = 100, offset: int = 0):
        """Get all processed reviews with pagination."""
        stmt = select(ProcessedReview).limit(limit).offset(offset)
        return self.session.execute(stmt).scalars().all()

    def get_by_id(self, id: int) -> Optional[ProcessedReview]:
        """Get processed review by its primary key ID."""
        stmt = select(ProcessedReview).where(ProcessedReview.id == id)
        return self.session.execute(stmt).scalar_one_or_none()