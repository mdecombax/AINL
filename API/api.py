from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time

# Import existing functions
from script import scrape_reddit, save_data_to_json, upload_file_to_openai, create_assistant_and_ask_question, interact_with_assistant



app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all domains. For production, specify actual domains.
    allow_credentials=True,
    allow_methods=["*"],  # This allows all methods.
    allow_headers=["*"],  # This allows all headers. 
)

@app.get("/newsletters/")
def do_nothing():
    time.sleep(20)
    return "zozo"

@app.get("/newsletter/")
def create_newsletter(subreddit: str):
    try:
        print(f"Subreddit: {subreddit}")
        # Step 1: Scrape Reddit using the provided subreddit name
        scraped_data = scrape_reddit(sr = subreddit)
        print("data have been scraped successfully")
        # return {"newsletter": scraped_data}
        exit(1)

        
        # Step 2: Save scraped data to a JSON file
        a = save_data_to_json(scraped_data)
        print(f"data have been saved to JSON file successfully")
        
        # Step 3: Upload the JSON file to OpenAI
        file_id = upload_file_to_openai("reddit_data.json")
        print(f"data have been uploaded to OpenAI successfully")
        
        # Step 4: Create an assistant and setup with the file
        assistant_id = create_assistant_and_ask_question(file_id)
        print(f"assistant have been created successfully")
        
        # Step 5: Interact with the assistant to generate the newsletter
        newsletter_content = interact_with_assistant(assistant_id)
        print(newsletter_content)
        return newsletter_content
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
