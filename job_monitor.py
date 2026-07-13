import requests
from bs4 import BeautifulSoup
import telebot
import time

# --- CONFIGURATION ---
# Replace with your actual credentials
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
TARGET_URL = "https://example.com/jobs"

bot = telebot.TeleBot(BOT_TOKEN)

def fetch_job_listings():
    """Fetches job listings from the target website."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(TARGET_URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Searching for job elements
        jobs = soup.find_all('div', class_='job-item')
        
        job_list = []
        for job in jobs[:3]:
            title = job.find('h2').get_text(strip=True)
            job_list.append(title)
            
        return job_list
    except Exception as e:
        print(f"Error occurred: {e}")
        return []

def run_monitor():
    """Monitors and sends alerts via Telegram."""
    print("Monitoring started...")
    while True:
        listings = fetch_job_listings()
        
        for job_title in listings:
            bot.send_message(CHAT_ID, f"🆕 New Job Alert: {job_title}")
        
        # Wait for 1 hour before checking again
        time.sleep(3600)

if __name__ == "__main__":
    run_monitor()
