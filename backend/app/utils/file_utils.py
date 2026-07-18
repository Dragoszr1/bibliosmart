import os
from .constants import ALLOWED_EXTENSIONS, CLUB_ANNOUNCEMENT_IMAGES_DIR

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def _find_files_by_prefix(directory, prefix):
    os.makedirs(directory, exist_ok=True)
    rezultate = []
    for fisier in os.listdir(directory):
        if not fisier.startswith(prefix + '.'):
            continue
        ext = fisier.rsplit('.', 1)[1].lower() if '.' in fisier else ''
        if ext in ALLOWED_EXTENSIONS:
            rezultate.append(fisier)
    return rezultate

def _save_club_activity_image(file, activitate_id):
    if not file or not file.filename:
        return None
    if not allowed_file(file.filename):
        return None

    os.makedirs(CLUB_ANNOUNCEMENT_IMAGES_DIR, exist_ok=True)
    for old in _find_files_by_prefix(CLUB_ANNOUNCEMENT_IMAGES_DIR, str(activitate_id)):
        try:
            os.remove(os.path.join(CLUB_ANNOUNCEMENT_IMAGES_DIR, old))
        except OSError:
            pass

    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{activitate_id}.{ext}"
    filepath = os.path.join(CLUB_ANNOUNCEMENT_IMAGES_DIR, filename)
    file.save(filepath)
    return filename
