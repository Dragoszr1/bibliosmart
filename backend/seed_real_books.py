import os
import urllib.request
import urllib.parse
import json
import random
from concurrent.futures import ThreadPoolExecutor
from app import create_app
from app.database import db
from app.models import Carti
from sqlalchemy import text

app = create_app()
IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'book_images')
os.makedirs(IMAGES_DIR, exist_ok=True)

def safe_name(title):
    return "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).strip()

def download_image(cover_i, safe_title):
    url = f"https://covers.openlibrary.org/b/id/{cover_i}-L.jpg"
    filepath = os.path.join(IMAGES_DIR, f"{safe_title}.jpg")
    if os.path.exists(filepath): return
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = response.read()
            if len(data) > 1000:
                with open(filepath, 'wb') as f:
                    f.write(data)
    except:
        pass

def get_books(query, limit=300):
    url = f"https://openlibrary.org/search.json?q={urllib.parse.quote(query)}&limit={limit}&has_fulltext=true"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read())
            return data.get('docs', [])
    except Exception as e:
        print(f"Failed to fetch {query}: {e}")
        return []

def main():
    # expanded queries to get lots of books
    queries = ["classic literature", "science fiction", "fantasy", "history", "romanian literature", "mystery", "thriller", "romance", "non-fiction", "biography", "philosophy", "young adult", "poetry", "children"]
    
    unique_books_data = []
    seen_titles = set()
    
    print("Fetching books from OpenLibrary API... (This might take a few seconds)")
    
    for q in queries:
        docs = get_books(q, limit=200)
        for doc in docs:
            title = doc.get('title')
            if not title: continue
            if len(title) > 45: title = title[:45]
            if title.lower() in seen_titles: continue
            
            author = doc.get('author_name', ['Unknown'])[0]
            if len(author) > 50: author = author[:50]
            
            cover_i = doc.get('cover_i')
            if not cover_i: continue # Only take books with real covers!
            
            seen_titles.add(title.lower())
            unique_books_data.append({
                'title': title,
                'author': author,
                'cover_i': cover_i,
                'gen': q.title()
            })

    print(f"Found {len(unique_books_data)} unique books with covers.")
    
    with app.app_context():
        print("Clearing old books...")
        try:
            db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
            db.session.execute(text("TRUNCATE TABLE carti;"))
            db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
            db.session.commit()
        except Exception as e:
            print("Truncate failed, attempting delete:", e)
            db.session.query(Carti).delete()
            db.session.commit()
        
        print("Inserting new books...")
        books_to_insert = []
        for i, b in enumerate(unique_books_data):
            isbn = str(random.randint(1000000000000, 9999999999999))
            cod = f"B{i}"
            stoc_tot = random.randint(1, 15)
            stoc_disp = random.randint(0, stoc_tot)
            
            carte = Carti(
                titlu=b['title'],
                autor=b['author'],
                gen=b['gen'],
                ISBN=isbn,
                cod=cod,
                stoc_total=stoc_tot,
                stoc_disponibil=stoc_disp
            )
            books_to_insert.append(carte)
            
        db.session.bulk_save_objects(books_to_insert)
        db.session.commit()
        
        print("Deleting old generic images...")
        for filename in os.listdir(IMAGES_DIR):
            try:
                os.unlink(os.path.join(IMAGES_DIR, filename))
            except: pass
            
        print("Downloading exact covers for all unique books in background...")
        with ThreadPoolExecutor(max_workers=30) as executor:
            for b in unique_books_data:
                executor.submit(download_image, b['cover_i'], safe_name(b['title']))
                
        print("All done!")

if __name__ == "__main__":
    main()
