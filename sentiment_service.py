import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import os


class SentimentService:
    def __init__(self, model_path: str = "models/distilbert_sentiment_classifier"):

        self.model_path = model_path
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.max_length = 512
        self.label_names = ['negative', 'neutral', 'positive']

        # Load model and tokenizer
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model not found at {self.model_path}. "
                "Please train the model first using train_sentiment.ipynb"
            )

        self.model = DistilBertForSequenceClassification.from_pretrained(self.model_path)
        self.model.to(self.device)
        self.model.eval()

        self.tokenizer = DistilBertTokenizer.from_pretrained(self.model_path)

    def predict(self, text: str) -> str:
        """
        'negative', 'neutral', or 'positive'
        """
        # Tokenize
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )

        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)

        # Predict
        with torch.no_grad():
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
            prediction = torch.argmax(outputs.logits, dim=1)

        return self.label_names[prediction.item()]
