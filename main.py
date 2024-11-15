from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests

# Function to extract the direct media URL from an Instagram Reel link
def get_instagram_reel_url(instagram_url):
    if "instagram.com/reel" in instagram_url:
        changing_url = instagram_url.split("/")
        url_code = changing_url[4]
        url = f"https://instagram.com/reels/{url_code}"
        
    # Set up the Selenium WebDriver with iPhone user agent
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        time.sleep(1)  # Wait for the page to load
        
        # Find all video elements
        video_elements = driver.find_elements(By.TAG_NAME, 'video')
        
        for video in video_elements:
            video_url = video.get_attribute('src')
            if video_url:
                return video_url
        
        return "Video URL not found."
    except Exception as e:
        return f"An error occurred: {e}"
    finally:
        driver.quit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Provide link to Instagram reel')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text
    if "instagram.com/reel" in url:
        direct_media_url = get_instagram_reel_url(url)
        
        if direct_media_url:
            response = requests.get(direct_media_url)
            
            if response.status_code == 200:
                with open('reel.mp4', 'wb') as file:
                    file.write(response.content)
                await update.message.reply_video(video=open('reel.mp4', 'rb'))
            else:
                await update.message.reply_text('Something went wrong')
        else:
            await update.message.reply_text('Something went wrong')
    else:
        pass

def main() -> None:
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token('').build()

    # Add handlers for the /start command and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()

