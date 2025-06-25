import requests
import base64
import os
from openai import OpenAI

client = OpenAI()

COLLECTION = "fav-in_der_b_cherei"
API_URL = f"https://archive.org/advancedsearch.php?q=collection:{COLLECTION}&fl[]=identifier&fl[]=title&fl[]=description&rows=5&page=1&output=json"

response = requests.get(API_URL)
data = response.json()
books = data['response']['docs']

prompts = []
for book in books:
    title = book.get('title', 'Unbekannter Titel')
    prompt = f"{title}"
    prompts.append({
        'identifier': book.get('identifier'),
        'title': title,
        'prompt': prompt
    })

for p in prompts:
    print(f"Buch: {p['title']}")
    print(f"Prompt: {p['prompt']}")
    img = client.images.generate(
        model="gpt-image-1",
        prompt=p['prompt'],
        n=1,
        size="1024x1024",
        response_format="b64_json"
    )
    image_bytes = base64.b64decode(img.data[0].b64_json)
    safe_title = ''.join(c for c in p['title'] if c.isalnum() or c in (' ', '_', '-')).rstrip()
    filename = f"{safe_title}.png"
    with open(filename, "wb") as f:
        f.write(image_bytes)
    print(f"Bild gespeichert als {filename}\n")
