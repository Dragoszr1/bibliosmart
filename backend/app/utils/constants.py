import os
import re

ALLOWED_EXTENSIONS = frozenset({'png', 'jpg', 'jpeg', 'gif', 'webp'})
ALLOWED_EMAIL_DOMAIN = 'cni-sv.ro'
VALID_ROLES = frozenset({'user', 'bibliotecar'})
ALLOWED_BOOK_FIELDS = frozenset({'titlu', 'autor', 'ISBN', 'stoc_total', 'stoc_disponibil', 'gen', 'pozitie', 'cod'})
ALLOWED_ANUNT_FIELDS = frozenset({'titlu', 'anunt'})

ROLE_ALIASES = {
    '1': 'bibliotecar',
    'administrator': 'bibliotecar',
    'admin': 'bibliotecar',
    'bibliotecar': 'bibliotecar',
    'user': 'user'
}

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._%+\-]{0,62}[A-Za-z0-9])?@([A-Za-z0-9\-]+\.)+[A-Za-z]{2,63}$")
USERNAME_REGEX = re.compile(r"^[A-Za-z0-9ăîâșțĂÎÂȘȚ\s._-]{3,50}$")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROFILE_PICTURES_DIR = os.path.join(BASE_DIR, 'profile_pictures')
BOOK_IMAGES_DIR = os.path.join(BASE_DIR, 'book_images')
BOOK_PDFS_DIR = os.path.join(BASE_DIR, 'book_pdfs')
CLUB_ANNOUNCEMENT_IMAGES_DIR = os.path.join(BASE_DIR, 'imagini_anunturi_club')
