import os
import random

directory = "C:/Users/zimbr/Downloads/drive-download"
sql_file = "C:/Users/zimbr/biblioteca-repo/insert_books.sql"

def parse_filename(filename):
    name = filename.replace('.pdf', '')
    name = name.replace('descarca-', '')
    name = name.replace('-', ' ')
    name = name.replace('_', ' ')
    
    parts = name.split(' ')
    if len(parts) >= 2:
        author = " ".join(parts[:2])
        title = " ".join(parts[2:])
        if not title:
            title = name
    else:
        author = "Autor Necunoscut"
        title = name
        
    author = author.title().strip()[:50]
    title = title.title().strip()[:50]
    return title, author

with open(sql_file, 'w', encoding='utf-8') as f:
    isbn_start = 9789000000000
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
    else:
        for i, filename in enumerate(os.listdir(directory)):
            if filename.endswith('.pdf'):
                title, author = parse_filename(filename)
                isbn = str(isbn_start + i)
                raft = f"Raft {random.randint(1, 10)}, Etaj {random.randint(1, 5)}"
                
                title = title.replace("'", "''")
                author = author.replace("'", "''")
                safe_filename = filename.replace("'", "''")
                
                sql = f"INSERT INTO carti (titlu, autor, ISBN, stoc_total, stoc_disponibil, imprumutat, gen, pozitie, cod, pdf_filename) VALUES ('{title}', '{author}', '{isbn}', 5, 5, 0, 'General', '{raft}', 'COD-{1000+i}', '{safe_filename}');\n"
                f.write(sql)
