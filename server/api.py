from fastapi import FastAPI
from modules.reddit_scraper import scrape_subreddit_posts, scrape_posts_from_theme, scrape_subreddits_posts
from modules.newsletter_generator import generate_newsletter
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all domains. For production, specify actual domains.
    allow_credentials=True,
    allow_methods=["*"],  # This allows all methods.
    allow_headers=["*"],  # This allows all headers. 
)

@app.get("/newsletter_from_subreddits/")
def create_newsletter(subreddits: str):
    subreddit_list = subreddits.split(",")
    scraped_data = scrape_subreddits_posts(subreddits=subreddit_list)
    newsletter_content = generate_newsletter(scraped_data)
    return newsletter_content

@app.get("/newsletter_from_subreddit/")
def create_newsletter(subreddit: str):
    scraped_data = scrape_subreddit_posts(sr=subreddit)
    newsletter_content = generate_newsletter(scraped_data)
    return newsletter_content

@app.get("/test/")
def return_test(subreddits: str):
    time.sleep(15)
    return """# 📰 AI Insights Newsletter\n\n---\n\n## Bienvenue à notre édition spéciale AI Insights !\n\nBonjour à tous ! 🌟 Dans cette édition, nous allons explorer l'univers fascinant de l'Intelligence Artificielle à travers des discussions passionnantes sur Reddit. Préparez-vous à plonger dans les débats et les dernières nouveautés du monde de l'IA. 🎉\n\n---\n\n## Les Trois Sujets Principaux\n\n### 1. 🔍 Qui sont les vrais influenceurs de l'IA ? \nUne image satirique des soi-disant "personnes les plus influentes en IA" a suscité beaucoup de réactions sur Reddit. Les utilisateurs ont vivement contesté l'authenticité et la pertinence des noms figurant sur cette liste, critiquant l'absence des véritables acteurs du domaine comme Sam Altman et Geoffrey Hinton. Pour en savoir plus, cliquez ici.\n\n### 2. 🆕 Un modèle open source révolutionnaire\nUn nouveau modèle d'IA open source basé sur Llama 3.1 fait parler de lui pour ses performances exceptionnelles. Il utilise une nouvelle technique qui surpasserait même certains modèles fermés de référence. Découvrez les détails et les commentaires enthousiastes de la communauté ici.\n\n### 3. 💸 Abonnements de luxe chez OpenAI\nOpenAI envisage de proposer des abonnements à des prix exorbitants, allant jusqu'à 2000 $ par mois, pour ses modèles d'IA de prochaine génération. Les spéculations et réactions fusent autour de ce prix, certains le considérant purement marketing. Plus d'infos ici.\n\n---\n\n## Trois Citations Intéressantes\n\n### 1. "Une Image Déconcertante"\n> AI Researchers: "Are we a joke to you?" \n> Lien vers la discussion \n\n### 2. "Une Technologique Incroyable" \n> Commentaire sur le modèle open-source: "Reflection 70B holds its own against even the top closed-source models (Claude 3.5 Sonnet, GPT-4o)." \n> Lien vers la discussion \n\n### 3. "L'Ironie des Abonnements"\n> Réaction face aux tarifs d'OpenAI: "That's a price point for an employee, not a chatbot. The only way it would make any sense is if it was legit AGI." \n> Lien vers la discussion \n\n---\n\n## Conclusion\n\nMerci d'avoir lu cette édition spéciale de notre Newsletter AI Insights! 🌐 Nous espérons que vous avez apprécié cette plongée dans les discussions les plus brûlantes et les sujets d'actualité du monde de l'IA. Restez connectés pour plus de mises à jour passionnantes. À la prochaine ! 🚀\n\n---"""

@app.get("/posts_from_theme/")
def get_posts_from_theme(keyword: str):
    return scrape_posts_from_theme(theme=keyword)
