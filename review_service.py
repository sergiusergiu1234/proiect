

from llm_service import llm_service
from sentiment_service import SentimentService
from model.processed_review import ProcessedReview
from model.review import Review
from model.review_repository import ReviewRepository
from prompts import prompts

class ReviewService:
    def __init__(self, review_repository: ReviewRepository, llm_service: llm_service, sentiment_service: SentimentService):
        self.review_repository = review_repository
        self.llm_service = llm_service
        self.sentiment_service = sentiment_service

    def check_halucination(self, review_text: str, summary: str):
        # hallucination check prompt
        prompt2 = prompts[1].template.format(review_text=review_text, generated_summary=summary)
        halucination_check_response = self.llm_service.generate_response(prompt2)
        return halucination_check_response


    def process_review(self, review: Review, max_retries: int = 3, ):
        retry_count = 0

        # summarize review
        prompt1 = prompts[0].template.format(review_text=review.text)
        summarizer_response = self.llm_service.generate_response(prompt1)

        # check halucination
        halucination_check_response = self.check_halucination(review_text=review.text,summary=summarizer_response)
        while halucination_check_response.strip().lower().startswith("fail") and retry_count <= max_retries:
            retry_count += 1
            halucination_check_response = self.check_halucination(review_text=review.text,summary=summarizer_response)

        # Check if halucination check passed (either initially or after retries)
        passed_halucination_check = halucination_check_response.strip().lower().startswith("pass")
        actual_halucination_check_response = None

        # if halucination is neither pass or fail, we save the actual response for later
        if not halucination_check_response.strip().lower().startswith("pass") and not halucination_check_response.strip().lower().startswith("fail"):
            passed_halucination_check = None
            actual_halucination_check_response = halucination_check_response

        # check sentiment with LLM
        prompt3 = prompts[2].template.format(review_text=review.text)
        sentiment_analysis_response = self.llm_service.generate_response(prompt3)
        print("LLM Sentiment:", sentiment_analysis_response)

        # check sentiment with deep learning model
        dl_sentiment = self.sentiment_service.predict(review.text)
        print("DL Sentiment:", dl_sentiment)

        processed_review = ProcessedReview(
             review_id = review.review_id,
             summary = summarizer_response,
             passed_halucination_check = passed_halucination_check,
             actual_halucination_check_response = actual_halucination_check_response,
             llm_sentiment = sentiment_analysis_response,
             dl_sentiment = dl_sentiment
        )
        return processed_review

