from scraper import extract_text
from analyzer import analyze_content
from storage import update_google_sheet
from email_sender import send_email

def verify_agency(agency_name, website, contact_email):
    print(f"Checking {agency_name}...")
    
    website_text = extract_text(website)
    if website_text:
        is_valid_agency = analyze_content(website_text)
        
        decision = "Approved" if is_valid_agency else "Rejected"
        update_google_sheet(agency_name, website, decision)
        
        send_email(contact_email, agency_name, decision)
        print(f"{agency_name} - {decision}")
    else:
        print(f"Failed to extract content from {website}")

# Example usage:
if __name__ == "__main__":
    verify_agency("Baun Fire", "https://www.baunfire.com/", "agency@example.com")
