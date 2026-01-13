from pydantic import BaseModel


class PromptNode(BaseModel):
    prompt_name: str
    template: str
    description: str
        
prompts: list[PromptNode] = [
    PromptNode(
        prompt_name="summarization",
        template="""Summarize the following Yelp review in max 250 words, focusing only on the main points of the customer's experience.
        Review:\n\n{review_text}""",
            description="Generates a concise summary of the provided text.",
    ),
     PromptNode(
        prompt_name="halucination_check",
        template="""You are a critical fact-checker. You must compare the Original Text with the Generated Summary.
         Check the summary for inaccuracies, facts not present in the original text, or names/figures that do not match (hallucinations).
         Your goal is to verify factual fidelity.
         Original Text:\n\n{review_text}
         Generated Summary:\n\n{generated_summary}\n\n

         Based ONLY on the original text, evaluate the summary.
         Respond with ONLY 'PASS' if the summary is factually accurate, or 'FAIL' if you identify any inaccuracy or hallucination.""",
        description="Checks the generated summary for factual accuracy against the original text.",
    ),
    PromptNode(
        prompt_name="sentiment_analysis",
        template="""Analyze the sentiment of the following Yelp review. The analysis must be based on the text content, regardless of the star rating.
        Respond with ONLY one of the following words: positive, negative, or neutral.
        Review:\n\n{review_text}""",
        description="Determines the sentiment (positive, negative, neutral) of the provided text.",
    )
   
]
  