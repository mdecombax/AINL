from fastapi import FastAPI
from modules.reddit_scraper import scrape_reddit
from modules.newsletter_generator import generate_newsletter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all domains. For production, specify actual domains.
    allow_credentials=True,
    allow_methods=["*"],  # This allows all methods.
    allow_headers=["*"],  # This allows all headers. 
)

@app.get("/newsletter/")
def create_newsletter(subreddit: str):
    scraped_data = scrape_reddit(sr=subreddit)
    newsletter_content = generate_newsletter(scraped_data)
    return newsletter_content
