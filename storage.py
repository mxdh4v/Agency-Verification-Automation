import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets API Setup
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDENTIALS_FILE = "google_credentials.json"

# Connect to Google Sheets
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPES)
client = gspread.authorize(creds)
sheet = client.open("Agency Verification").sheet1  # Open the first sheet

def update_google_sheet(agency_name, website, decision):
    """Store verification decision in Google Sheets"""
    sheet.append_row([agency_name, website, decision])
    print(f"Updated Google Sheet: {agency_name} - {decision}")

# Example usage:
if __name__ == "__main__":
    update_google_sheet("Digital Silk", "https://www.digitalsilk.com/", "Approved")
