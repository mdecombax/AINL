import praw
import os
import time
from dotenv import load_dotenv
import json

# Load environment variables from the .env file
load_dotenv()

def scrape_subreddits_posts(max_comments_per_post=7, subreddits=["LocalLLaMA"]):
    reddit = praw.Reddit(client_id=os.getenv("REDDIT_CLIENT_ID"),
                         client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
                         user_agent="autoNL")

    scraped_data = []

    for sr in subreddits:
        print("Start scraping subreddit:", sr)
        subreddit = reddit.subreddit(sr)

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
                print(f"API Exception for subreddit {sr}: {e}")
                time.sleep(60)

    return scraped_data

def scrape_subreddit_posts(max_comments_per_post=7, sr="LocalLLaMA"):
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

def scrape_posts_from_theme(theme: str, subreddit_limit: int = 5, post_limit: int = 2):
    reddit = praw.Reddit(client_id=os.getenv("REDDIT_CLIENT_ID"),
                         client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
                         user_agent="autoNL")
    try:
        print(f"Recherche des subreddits pour le thème '{theme}'...")
        subreddits = reddit.subreddits.search(query=theme, limit=50)
        subreddit_list = list(subreddits)

        # Diviser le thème en mots-clés individuels
        keywords = theme.lower().split()

        detailed_subreddits = []
        for subreddit in subreddit_list:
            try:
                # Vérifier si au moins un des mots-clés est présent dans le nom ou la description du subreddit
                if any(keyword in subreddit.display_name.lower() or keyword in subreddit.public_description.lower() for keyword in keywords):
                    detailed_subreddits.append({
                        'name': subreddit.display_name,
                        'subscribers': subreddit.subscribers,
                        'public_description': subreddit.public_description,
                        'created_utc': subreddit.created_utc
                    })
            except Exception as e:
                print(f"Erreur lors de la récupération des informations pour {subreddit.display_name} : {e}")
    except Exception as e:
        print(f"Erreur lors de la recherche des subreddits : {e}")
        return []

    try:
        print(f"Subreddits trouvés pour le thème '{theme}' :")
        for subreddit in detailed_subreddits:
            print(f"- {subreddit['name']} (Abonnés : {subreddit['subscribers']})")
    except Exception as e:
        print(f"Erreur lors de l'affichage des subreddits : {e}")
    
    try:
        # Tri des subreddits par nombre d'abonnés, en gérant les NoneType
        sorted_subreddits = sorted(
            detailed_subreddits,
            key=lambda s: s['subscribers'] if s['subscribers'] is not None else 0,
            reverse=True
        )
        top_subreddits = sorted_subreddits[:subreddit_limit]

        print(f"\nTop {subreddit_limit} subreddits sélectionnés :")
        for subreddit in top_subreddits:
            print(f"- {subreddit['name']} (Abonnés : {subreddit['subscribers']})")
    except Exception as e:
        print(f"Erreur lors du tri des subreddits : {e}")
        return []

    results = []
    
    for subreddit in top_subreddits:
        try:
            print(f"\nRécupération des top {post_limit} posts du mois pour le subreddit '{subreddit['name']}'...")
            subreddit_obj = reddit.subreddit(subreddit['name'])
            top_posts = subreddit_obj.top(time_filter='month', limit=post_limit)
        except Exception as e:
            print(f"Erreur lors de la récupération des posts pour '{subreddit['name']}' : {e}")
            continue

        try:
            for post in top_posts:
                post_metadata = {
                    'subreddit': subreddit['name'],
                    'post_title': post.title,
                    'post_id': post.id,
                    'post_url': post.url
                }
                print(f"   - Post trouvé : {post.title}")
                results.append(post_metadata)
        except Exception as e:
            print(f"Erreur lors de l'ajout des posts pour '{subreddit['name']}' : {e}")
    
    print("\nRécupération des posts terminée.\n")
    return json.dumps(results, indent=4)
 
