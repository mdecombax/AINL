def scrape_reddit(max_comments_per_post=7):
    """Useful to scrape reddit content, including posts and their top comments."""
    import praw  # Make sure to import praw
    import time  # Importing time for handling API exceptions

    reddit = praw.Reddit(
        client_id="36NF-OTGo2EWrhkg22o0Zw",
        client_secret="XZ1KEyXmNnKj7tewYxAKvVpSnJSw4Q",
        user_agent="autoNL",
    )

    subreddit = reddit.subreddit("LocalLLaMA")
    scraped_data = []

    for post in subreddit.hot(limit=11):
        # Include the post's selftext in the data.
        post_data = {"title": post.title, "url": post.url, "content": post.selftext, "comments": []}

        try:
            post.comments.replace_more(limit=0)  # Load top-level comments only
            comments = post.comments.list()
            if max_comments_per_post is not None:
                comments = comments[:max_comments_per_post]  # Use the variable correctly

            for comment in comments:
                post_data["comments"].append(comment.body)

            scraped_data.append(post_data)

        except praw.exceptions.APIException as e:
            print(f"API Exception: {e}")
            time.sleep(60)  # Sleep for 1 minute before retrying

    return scraped_data


import json

# Supposons que scraped_data est votre liste de données recueillies
scraped_data = scrape_reddit()  # Votre fonction de scraping

# Spécifiez le nom de fichier pour l'export JSON
filename = 'reddit_data.json'

# Utilisez json.dump pour écrire les données dans un fichier
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(scrape_reddit(), f, ensure_ascii=False, indent=4)

print(f"Les données ont été exportées avec succès dans {filename}.")


from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "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"
client = OpenAI()

# Replace 'path/to/your/document' with the actual file path and 'your_file_type' with the file type (e.g., 'text/plain')
file_response = client.files.create(
  file=open("reddit_data.json", "rb"),
  purpose="assistants"
)

file_id = file_response.id

assistant_response = client.beta.assistants.create(
  instructions="""Vous êtes un spécialiste en contenu avec une expertise approfondie en intelligence artificielle. Votre mission est de créer une newsletter détaillée qui capte l'essence des discussions les plus engageantes et informatives extraites d'un subreddit dédié à l'IA. La newsletter devrait inclure :

Un résumé des tendances actuelles et des débats clés sur l'IA.
Des liens vers les discussions les plus populaires ou les plus pertinentes.
Une analyse des implications de ces tendances pour les professionnels de l'IA et les passionnés.
Des citations directes des contributions les plus perspicaces des utilisateurs du subreddit.
Assurez-vous de présenter les informations de manière organisée, avec des sections bien définies, et d'adopter un ton engageant qui stimule l'intérêt et la participation des lecteurs""",
  model="gpt-4-turbo-preview",
  tools=[{"type": "retrieval"}, {"type": "code_interpreter"}],  # Specify the tool type you want to use
  file_ids=[file_id]
)

assistant_id = assistant_response.id

thread = client.beta.threads.create()

file_response = client.files.create(
  file=open("prompt.txt", "rb"),
  purpose="assistants"
)

file_id = file_response.id

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="qu'est qu'il y a dans le document que je viens d'uploader dans cette discussion?",
    file_ids=[file_id]  # Assurez-vous de remplacer 'file_id' par l'ID de fichier réel
)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant_id,
  instructions="Please address the user as Jane Doe. The user has a premium account."
)

import time

while run.status in ['queued', 'in_progress', 'cancelling']:
  time.sleep(1)  # Attendre 1 seconde
  run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
  )

if run.status == 'completed': 
  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )
  print(messages.data)
else:
  print(run.status)


messages.data[0].content[0].text.value