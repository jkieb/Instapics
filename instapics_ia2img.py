import requests
import json
import time
from urllib.parse import quote
# from craiyon import Craiyon  # Entfernt, da nicht mehr benötigt
import base64
from io import BytesIO
from PIL import Image
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

# 1. Metadaten der ersten fünf Bücher aus der Collection abrufen
COLLECTION = "fav-in_der_b_cherei"
API_URL = f"https://archive.org/advancedsearch.php?q=collection:{COLLECTION}&fl[]=identifier&fl[]=title&fl[]=description&rows=5&page=1&output=json"

response = requests.get(API_URL)
data = response.json()
books = data.response.docs

# 2. Für jedes Buch einen Prompt generieren
prompts = []
for book in books:
    title = book.get('title', 'Unbekannter Titel')
    description = book.get('description', '')
    if description:
        prompt = f"{title}: Eine prominente Szene aus dem Buch als künstlerisches Instagram-Foto. Beschreibung: {description}"
    else:
        prompt = f"{title}: Eine prominente Szene aus dem Buch als künstlerisches Instagram-Foto."
    prompts.append({
        'identifier': book.get('identifier'),
        'title': title,
        'prompt': prompt
    })

# 3. Prompts ausgeben (Debug)
for p in prompts:
    print(f"Buch: {p['title']}")
    print(f"Prompt: {p['prompt']}\n")

OPENAI_API_KEY = "REMOVED_OPENAI_KEY"  # <-- Hier deinen OpenAI API-Key eintragen

# Funktion zum Bildgenerieren via OpenAI DALL·E API (dall-e-2)
def generate_image(prompt, filename):
    try:
        print(f"Sende Prompt an OpenAI DALL·E: {prompt}")
        response = client.images.generate(prompt=prompt,
        n=1,
        size="1024x1024",  # oder "512x512" für günstiger
        model="dall-e-2"   # günstigstes Modell)
        image_url = response.data[0].url
        img_data = requests.get(image_url).content
        with open(filename, 'wb') as handler:
            handler.write(img_data)
        print(f"Bild gespeichert als {filename}\n")
    except Exception as e:
        print(f"Fehler bei der Bildgenerierung: {e}\n")

# 4. Für jeden Prompt ein Bild generieren und speichern
for p in prompts:
    # Dateiname aus Titel generieren (nur Buchstaben/Zahlen)
    safe_title = ''.join(c for c in p['title'] if c.isalnum() or c in (' ', '_', '-')).rstrip()
    filename = f"{safe_title}.jpg"
    generate_image(p['prompt'], filename)
    # Wartezeit, um API-Limits nicht zu überschreiten
    time.sleep(10) 