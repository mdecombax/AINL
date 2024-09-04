import praw
import os
import time
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def scrape_reddit(max_comments_per_post=7, sr="LocalLLaMA"):
    print("Start scraping subreddit:", sr)
    reddit = praw.Reddit(client_id=os.getenv("REDDIT_CLIENT_ID"),
                         client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
                         user_agent="autoNL")
    
    subreddit = reddit.subreddit(sr)
    scraped_data = []

    for post in subreddit.top(time_filter='week', limit=10):
        post_data = {
            "title": post.title,
            "url": post.url,
            "content": post.selftext,
            "comments": []
        }

        try:
            post.comments.replace_more(limit=0)
            comments = post.comments.list()[:max_comments_per_post]

            for comment in comments:
                post_data["comments"].append(comment.body)

            scraped_data.append(post_data)

        except praw.exceptions.APIException as e:
            print(f"API Exception: {e}")
            time.sleep(60)

    return scraped_data
