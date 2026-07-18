from flask import request
from .constants import ROLE_ALIASES, VALID_ROLES, EMAIL_REGEX, ALLOWED_EMAIL_DOMAIN

def normalize_role(raw_role):
    if raw_role is None:
        return 'user'

    rol_normalizat = ROLE_ALIASES.get(str(raw_role).strip().lower())
    return rol_normalizat if rol_normalizat in VALID_ROLES else 'user'

def normalize_cni_email(email):
    if not isinstance(email, str):
        return None

    email_normalizat = email.strip().lower()
    if not email_normalizat or len(email_normalizat) > 254:
        return None

    if not EMAIL_REGEX.fullmatch(email_normalizat):
        return None

    parte_locala, _, domeniu = email_normalizat.rpartition('@')
    if not parte_locala or '..' in parte_locala or domeniu != ALLOWED_EMAIL_DOMAIN:
        return None

    return email_normalizat

def _get_request_data():
    if request.content_type and request.content_type.startswith('multipart/form-data'):
        return request.form.to_dict()
    return request.get_json(silent=True) or {}
