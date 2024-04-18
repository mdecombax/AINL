import praw
import time
import json
from openai import OpenAI
import os


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
    reddit = praw.Reddit(client_id="36NF-OTGo2EWrhkg22o0Zw",
                         client_secret="XZ1KEyXmNnKj7tewYxAKvVpSnJSw4Q",
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
    os.environ["OPENAI_API_KEY"] = "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"
    client = OpenAI()
    file_response = client.files.create(file=open(filepath, "rb"), purpose="assistants")
    return file_response.id

# Partie 4 : Création d'un assistant et fourniture du fichier à cet assistant
def create_assistant_and_ask_question(file_id):
    client = OpenAI()
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
        model="gpt-4-turbo-preview",
        tools=[{"type": "retrieval"}, {"type": "code_interpreter"}],
        file_ids=[file_id]
    )
    # return 123
    return assistant_response.id

# Partie 5 : Interaction avec l'assistant
def interact_with_assistant(assistant_id):

    # chemin_fichier = 'example_NL.json'
    # resultat = lire_json(chemin_fichier)
    # return(resultat)

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
        # instructions="Propose moi une newsletter"
    )

    while run.status in ['queued', 'in_progress', 'cancelling']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        return messages.data[0].content[0].text.value
    else:
        print(f"Le traitement a échoué avec le statut : {run.status}")


# scraped_data = scrape_reddit()
# save_data_to_json(scraped_data)
# file_id = upload_file_to_openai("reddit_data.json")
# assistant_id = create_assistant_and_ask_question(file_id)
# interact_with_assistant(assistant_id)