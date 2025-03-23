from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def extract_text(url):
    """Extracts text from a website using Selenium with better cleaning."""
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode (no UI)
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)
        time.sleep(5)  # Wait for JavaScript content to load

        # Extract visible text from relevant elements
        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        divs = driver.find_elements(By.TAG_NAME, "div")
        spans = driver.find_elements(By.TAG_NAME, "span")

        # Filter out empty and duplicate text
        text_elements = [p.text.strip() for p in paragraphs] + \
                        [d.text.strip() for d in divs] + \
                        [s.text.strip() for s in spans]

        # Remove short/irrelevant texts like "SCROLL" or "LET'S TALK"
        text_elements = [t for t in text_elements if len(t) > 20 and not t.isupper()]

        # Join and clean up spacing
        cleaned_text = " ".join(set(text_elements))  # Remove duplicates
        cleaned_text = " ".join(cleaned_text.split())  # Remove extra spaces

        driver.quit()
        return cleaned_text if cleaned_text else None
    except Exception as e:
        print(f"❌ Selenium failed for {url}: {e}")
        return None

