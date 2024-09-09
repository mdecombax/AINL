import json

def lire_json(fichier):
    try:
        with open(fichier, 'r', encoding='utf-8') as f:
            contenu = json.load(f)
        return contenu
    except FileNotFoundError:
        return "File not found."
    except json.JSONDecodeError:
        return "Error decoding JSON."
    except Exception as e:
        return f"An error occurred: {e}"