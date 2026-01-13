
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Config(BaseModel):
    sqldbUrl: str  = os.getenv("SQLDB_URL") or 'mysql+pymysql://root:root@localhost:3306/yelp_db'
    openaiKey: str | None = os.getenv("OPENAI_API_KEY")

    # Sentiment model configuration
    sentimentModelPath: str = os.getenv("SENTIMENT_MODEL_PATH") or 'models/distilbert_sentiment_classifier'
    sentimentBatchSize: int = int(os.getenv("SENTIMENT_BATCH_SIZE", "16"))
    sentimentMaxLength: int = int(os.getenv("SENTIMENT_MAX_LENGTH", "512"))

def getConfig():
    return Config()