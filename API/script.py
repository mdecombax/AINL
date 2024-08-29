import praw
import time
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis un fichier .env
load_dotenv()

## Test de fonction simplifé
def generate_newsletter(scraped_data):
    client = OpenAI()
    
    prompt = f"""
    Créez une newsletter basée sur les données Reddit suivantes :
    {json.dumps(scraped_data, indent=2)}
    
    La newsletter doit suivre ce format :
    1. Titre de la Newsletter
    2. Introduction
    3. Les Trois Sujets Principaux
    4. Trois citations Intéressantes
    5. Conclusion

    Urilises markdown pour formater au mieux cette newsletter.
    Pour les citation met un titre à chaque fois, utilise la langue d'origine de la citation et finit par un lien vers le post.
    Ce formattage est très important, tu devras utiliser le plus d'élément de madown possible pour rendre la newsletter la plus lisible possible.
    Met des smileys pour rendre la newsletter plus agréable à lire.

    Dans ta réponse ne donne aucun autre élément que la newsletter.

    """
    
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "Vous êtes un spécialiste en contenu avec une expertise approfondie en intelligence artificielle."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content


def lire_json(fichier):
    try:
        with open(fichier, 'r', encoding='utf-8') as f:
            contenu = json.load(f)
        return contenu
    except FileNotFoundError:
        return "Le fichier n'a pas été trouvé."
    except json.JSONDecodeError:
        return "Erreur lors de la décodage du JSON."
    except Exception as e:
        return f"Une erreur est survenue: {e}"

# Partie 1 : Scraping de contenu de Reddit
def scrape_reddit(max_comments_per_post=7, sr = "LocalLLaMA"):
    print("start scrape")
    print(os.getenv("REDDIT_CLIENT_ID"))

    reddit = praw.Reddit(client_id=os.getenv("REDDIT_CLIENT_ID"),
                         client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
                         user_agent="autoNL")
    subreddit = reddit.subreddit(sr)
    scraped_data = []

    for post in subreddit.top(time_filter ='week', limit=10):
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
            print(f"Exception API: {e}")
            time.sleep(60)

    return scraped_data

# Partie 2 : Sauvegarde des données scrapées dans un fichier JSON
def save_data_to_json(data, filename='reddit_data.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Partie 3 : Upload du fichier JSON chez OpenAI 
def upload_file_to_openai(filepath):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    client = OpenAI()
    file_response = client.files.create(file=open(filepath, "rb"), purpose="assistants")
    print(file_response)
    return file_response.id

# Partie 4 : Création d'un assistant et fourniture du fichier à cet assistant
def create_assistant_and_ask_question(file_id):
    print("Starting assistant creation")
    client = OpenAI()
    
    try:
        assistant_response = client.beta.assistants.create(
            instructions="""Vous êtes un spécialiste en contenu avec une expertise approfondie en intelligence artificielle. Votre mission est de créer une newsletter détaillée qui capte l'essence des discussions les plus engageantes et informatives extraites d'un subreddit dédié à l'IA. Voici un exemple de la structure de la newsletter

            # Titre de la Newsletter

            ## Introduction
            Cette newsletter est générée par une intelligence artificielle conçue pour analyser les tendances et discussions les plus pertinentes de la semaine.

            ## Les Trois Sujets Principaux
            1. **[Titre du Premier Sujet]** - [Développez sur trois lignes le contenu et l'importance du sujet.](lien-vers-le-post)
            2. **[Titre du Deuxième Sujet]** - [Développez sur trois lignes le contenu et l'importance du sujet.](lien-vers-le-post)
            3. **[Titre du Troisième Sujet]** - [Développez sur trois lignes le contenu et l'importance du sujet.](lien-vers-le-post)

            ## Trois citations Intéressantes
            1. **[Titre de la Première Citation]** - [Texte de la citation dans la langue d'origine]
            2. **[Titre de la Deuxième Citation]** - [Texte de la citation dans la langue d'origine]
            3. **[Titre de la Troisième Citation]** - [Texte de la citation dans la langue d'origine]

            ## Conclusion
            [Résumez en trois lignes les insights clés ou les points saillants de la semaine, capturés par l'intelligence artificielle.]""",
            model="gpt-4o",
            tools=[{"type": "file_search"}, {"type": "code_interpreter"}],
            tool_resources={
                "code_interpreter": {
                    "file_ids": [file_id]
                }
            }

        )
        print("Assistant created successfully!")
        return assistant_response.id
    except Exception as e:
        print(f"Une erreur s'est produite lors de la création de l'assistant : {str(e)}")
        return None
# Partie 5 : Interaction avec l'assistant
def interact_with_assistant(assistant_id):
    print("Starting interaction with assistant")
    try:
        client = OpenAI()
        thread = client.beta.threads.create()
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content="""Propose moi une newsletter""",
        )
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id,
        )

        while run.status in ['queued', 'in_progress', 'cancelling']:
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        if run.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            return messages.data[0].content[0].text.value
        else:
            print(f"Le traitement a échoué avec le statut : {run.status}")
            return None
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        return None


# scraped_data = scrape_reddit()
# save_data_to_json(scraped_data)
# file_id = upload_file_to_openai("reddit_data.json")
# assistant_id = create_assistant_and_ask_question(file_id)
# interact_with_assistant(assistant_id)