import random
from app import create_app
from app.database import db
from app.models import Carti

app = create_app()

romanian_authors = [
    "Mihai Eminescu", "Ion Creangă", "I.L. Caragiale", "Ioan Slavici",
    "George Bacovia", "Lucian Blaga", "Tudor Arghezi", "Ion Barbu",
    "Liviu Rebreanu", "Camil Petrescu", "George Călinescu", "Marin Preda",
    "Mircea Eliade", "Mihail Sadoveanu", "Nichita Stănescu", "Mircea Cărtărescu"
]

universal_authors = [
    "William Shakespeare", "Fiodor Dostoievski", "Lev Tolstoi", "Victor Hugo",
    "Charles Dickens", "Jane Austen", "Mark Twain", "Ernest Hemingway",
    "Franz Kafka", "Gabriel Garcia Marquez", "Homer", "Dante Alighieri",
    "Johann Wolfgang von Goethe", "Albert Camus", "J.R.R. Tolkien", "George Orwell"
]

educational_authors = [
    "Mihai Ștefănescu", "Ion Popescu", "Maria Ionescu", "Elena Radu",
    "Alexandru Mitru", "Dan Barbilian", "Nicolae Manolescu", "Eugen Lovinescu"
]

romanian_books = [
    "Poezii", "Amintiri din copilărie", "O scrisoare pierdută", "Moara cu noroc",
    "Plumb", "Poemele luminii", "Flori de mucigai", "Joc secund",
    "Ion", "Răscoala", "Pădurea spânzuraților", "Ultima noapte de dragoste",
    "Patul lui Procust", "Enigma Otiliei", "Moromeții", "Cel mai iubit dintre pământeni",
    "Maitreyi", "Baltagul", "Frații Jderi", "Necuvintele", "Levantul"
]

universal_books = [
    "Hamlet", "Romeo și Julieta", "Crimă și pedeapsă", "Frații Karamazov",
    "Război și pace", "Anna Karenina", "Mizerabilii", "Marile speranțe",
    "Mândrie și prejudecată", "Aventurile lui Huckleberry Finn", "Bătrânul și marea",
    "Procesul", "Un veac de singurătate", "Iliada", "Divina Comedie",
    "Faust", "Străinul", "Stăpânul Inelelor", "1984", "Ferma animalelor"
]

educational_books = [
    "Culegere de Matematică pentru clasa a IX-a", "Culegere de Matematică pentru clasa a X-a",
    "Culegere de Matematică pentru clasa a XI-a", "Culegere de Matematică pentru clasa a XII-a",
    "Fizică - Probleme și teste pentru bacalaureat", "Chimie Organică - Exerciții",
    "Biologie - Anatomia omului", "Istoria Românilor - Sinteze",
    "Geografia României - Teste", "Informatica - Algoritmi și structuri de date",
    "Limba și literatura română - Eseuri pentru bac", "Culegere de Informatică C++",
    "Gramatica limbii române", "Teste de pregătire pentru admitere Poli",
    "Manual de Filosofie", "Manual de Logică", "Sinteze de Psihologie"
]

genres = ["Beletristică", "Roman", "Poezie", "Dramaturgie", "Educațional", "Științe Exacte", "Umaniste", "Clasic", "Ficțiune Istorică", "Fantezie", "Science Fiction"]

def generate_books(count):
    books = []
    for i in range(count):
        # 40% romanian, 40% universal, 20% educational
        category_roll = random.random()
        
        if category_roll < 0.4:
            titlu = random.choice(romanian_books)
            autor = random.choice(romanian_authors)
            gen = random.choice(["Roman", "Poezie", "Dramaturgie", "Clasic", "Beletristică"])
        elif category_roll < 0.8:
            titlu = random.choice(universal_books)
            autor = random.choice(universal_authors)
            gen = random.choice(["Roman", "Clasic", "Ficțiune Istorică", "Fantezie", "Science Fiction"])
        else:
            titlu = random.choice(educational_books)
            autor = random.choice(educational_authors)
            gen = random.choice(["Educațional", "Științe Exacte", "Umaniste"])
            
        # Add edition/volume to guarantee uniqueness / variety
        titlu_final = f"{titlu} - Ed. {random.randint(1990, 2024)} ({i+1})"
        if len(titlu_final) > 45:
            titlu_final = titlu_final[:45]
        
        isbn = str(random.randint(1000000000000, 9999999999999))
        cod = f"C{i}"
        
        stoc_tot = random.randint(1, 15)
        stoc_disp = random.randint(0, stoc_tot)
        
        carte = Carti(
            titlu=titlu_final,
            autor=autor,
            gen=gen,
            ISBN=isbn,
            cod=cod,
            stoc_total=stoc_tot,
            stoc_disponibil=stoc_disp
        )
        books.append(carte)
    return books

with app.app_context():
    print("Generating 2500 books for the database...")
    books = generate_books(2500)
    
    print("Inserting into database (this might take a moment)...")
    db.session.bulk_save_objects(books)
    db.session.commit()
    print("Successfully inserted 2500 books!")
