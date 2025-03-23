import os
import pandas as pd
import requests
import gspread
from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# ✅ Google Sheets API Setup
GOOGLE_SHEET_NAME = "Agency Verification"

# Load credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("google_credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open(GOOGLE_SHEET_NAME).sheet1  # Select the first sheet

# ✅ Load AI model
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# ✅ Predefined keywords for verification
KEYWORDS = ["marketing", "SEO", "advertising", "branding", "PPC", "social media", "content marketing"]

# ✅ Function to scrape website content
def scrape_website(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = [p.text.strip() for p in soup.find_all("p")]
        headings = [h.text.strip() for h in soup.find_all(["h1", "h2", "h3"])]
        content = " ".join(paragraphs + headings)
        return content if content else None
    except Exception as e:
        print("❌ Error fetching content:", e)
        return None

# ✅ Function to analyze content using keywords
def analyze_keywords(text):
    found_keywords = [kw for kw in KEYWORDS if kw.lower() in text.lower()]
    return found_keywords

# ✅ Function to classify text using AI
def classify_using_ai(text):
    inputs = tokenizer(text[:512], return_tensors="pt", truncation=True, padding=True).to(device)
    outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=1).item()
    return "Approved" if prediction == 1 else "Rejected"

# ✅ Function to determine approval or rejection
def determine_status(url):
    content = scrape_website(url)
    if not content:
        return "Rejected", []

    keywords_found = analyze_keywords(content)

    # Rule: If no keywords, reject immediately
    if len(keywords_found) == 0:
        return "Rejected", []

    # Rule: If 3+ keywords, approve immediately
    if len(keywords_found) >= 3:
        return "Approved", keywords_found

    # Rule: If 1-2 keywords, use AI classification
    ai_prediction = classify_using_ai(content)
    return (ai_prediction, keywords_found)

# ✅ Function to update Google Sheet
def update_google_sheets(url, status, keywords):
    try:
        sheet.append_row([url, status, ", ".join(keywords)])
        print(f"✅ Updated Google Sheet: {url} - {status}")
    except Exception as e:
        print(f"❌ Error updating Google Sheet: {e}")

# ✅ API Route for verification
@app.route("/check", methods=["POST"])
def check_website():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"message": "No URL provided"}), 400

    status, keywords = determine_status(url)
    update_google_sheets(url, status, keywords)

    return jsonify({"status": status, "keywords": keywords})

# ✅ Route for frontend UI
@app.route("/")
def index():
    return render_template("index.html")

# ✅ Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
