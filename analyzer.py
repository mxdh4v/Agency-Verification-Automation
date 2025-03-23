import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import re

# Load DistilBERT model and tokenizer
MODEL_PATH = "distilbert-base-uncased"  # Ensure this model is available
tokenizer = DistilBertTokenizer.from_pretrained(MODEL_PATH)
model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH, num_labels=2)
model.eval()

# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Keywords for verification
KEYWORDS = ["web design", "web development", "SEO", "digital marketing", "branding", "advertising", "agency"]

def clean_text(text):
    """Cleans extracted text by removing special characters and extra spaces."""
    text = re.sub(r'\s+', ' ', text)
    return text.lower().strip()

def classify_text(text):
    """Classifies text using AI model."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        prediction = torch.argmax(logits, dim=-1).item()

    return "Approved" if prediction == 1 else "Rejected"

def analyze_content(text, model, tokenizer):
    """Analyze text with keyword matching first, AI as a secondary validator."""
    text = clean_text(text)

    # Keyword matching (case-insensitive)
    found_keywords = [kw for kw in KEYWORDS if kw.lower() in text]

    # ✅ REJECT IMMEDIATELY IF NO KEYWORDS FOUND
    if not found_keywords:
        return "Rejected", found_keywords  

    # ✅ APPROVE IMMEDIATELY IF 3 OR MORE KEYWORDS FOUND
    if len(found_keywords) >= 3:
        return "Approved", found_keywords  

    # 🔹 AI DECIDES ONLY IF 1-2 KEYWORDS ARE FOUND
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=1).item()

    if prediction == 1:  # AI thinks it's relevant
        return "Approved", found_keywords
    else:
        return "Rejected", found_keywords  # Default rejection if AI says no

