import os
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from app import create_app
from app.database import db
from app.models import Carti

app = create_app()

IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'book_images')
os.makedirs(IMAGES_DIR, exist_ok=True)

def fetch_image_for_title(title):
    safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).strip()
    url_title = urllib.parse.quote_plus(safe_title)
    url = f"https://covers.openlibrary.org/b/title/{url_title}-L.jpg"
    
    filepath = os.path.join(IMAGES_DIR, f"{safe_title}.jpg")
    
    if os.path.exists(filepath):
        return
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = response.read()
            if len(data) > 1000:
                with open(filepath, 'wb') as f:
                    f.write(data)
                print(f"Downloaded cover for: {safe_title}")
    except Exception as e:
        print(f"Failed for {title}: {e}")

def main():
    # Delete all existing images
    for filename in os.listdir(IMAGES_DIR):
        file_path = os.path.join(IMAGES_DIR, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            pass

    with app.app_context():
        # Get all unique titles from the DB by stripping after the hyphen
        books = Carti.query.all()
        unique_titles = set()
        for carte in books:
            base_title = carte.titlu.split('-')[0].strip()
            unique_titles.add(base_title)
            
        print(f"Found {len(unique_titles)} unique base titles. Pulling images...")
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(fetch_image_for_title, unique_titles)
            
        print("Finished pulling title-based images!")

if __name__ == "__main__":
    main()
