import json
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI content expert."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content
