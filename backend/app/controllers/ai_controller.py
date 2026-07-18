from flask import request, jsonify, current_app
from sqlalchemy import text
from app.database import db
from groq import Groq
from app.middlewares.auth import get_current_user
import logging

logger = logging.getLogger(__name__)

GROQ_MODEL = 'llama-3.3-70b-versatile'

def _get_groq_client():
    api_key = current_app.config.get('GROQ_API_KEY', '')
    if not api_key:
        return None
    return Groq(api_key=api_key)

def _groq_chat(client, prompt, system_message=None):
    messages = []
    if system_message:
        messages.append({'role': 'system', 'content': system_message})
    messages.append({'role': 'user', 'content': prompt})
    
    logger.info('Prompt Groq: %s', prompt[:300])
    raspuns = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        max_tokens=1024,
        temperature=0.7
    )
    return raspuns.choices[0].message.content.strip()

def ai_recommend(user):
    user_id = user['user_id']

    client = _get_groq_client()
    if not client:
        return jsonify({'success': False, 'message': 'AI neconfigurat'}), 503

    try:
        all_rows = db.session.execute(
            text("SELECT carte_id, titlu, autor, gen, stoc_disponibil FROM carti ORDER BY titlu")
        ).fetchall()

        read_rows = db.session.execute(
            text("SELECT c.carte_id, c.titlu, c.autor, c.gen FROM carti_citite cc JOIN carti c ON cc.carte_id = c.carte_id WHERE cc.user_id = :uid"),
            {'uid': user_id}
        ).fetchall()

        borrowed_rows = db.session.execute(
            text("SELECT c.carte_id, c.titlu, c.autor FROM cereri_carti cc JOIN carti c ON cc.carte_id = c.carte_id WHERE cc.user_id = :uid AND cc.status IN ('pending', 'approved')"),
            {'uid': user_id}
        ).fetchall()

        if not read_rows:
            return jsonify({'success': True, 'recommendations': '', 'no_history': True}), 200

        read_list = '\n'.join(f'- {r[1]} de {r[2]} (gen: {r[3]})' for r in read_rows)
        borrowed_list = '\n'.join(f'- {r[1]} de {r[2]}' for r in borrowed_rows) or 'niciuna'
        lib_list = '\n'.join(
            f'- [ID:{r[0]}] {r[1]} de {r[2]} (gen: {r[3]}) — {"disponibil" if r[4] > 0 else "indisponibil"}'
            for r in all_rows
        )

        system_prompt = (
            "Ești bibliotecar la o școală. Ai acces la catalogul COMPLET al bibliotecii de mai jos.\n"
            "Recomandă DOAR cărți care există în catalog și sunt marcate ca 'disponibil'.\n"
            "Nu inventa cărți sau autori care nu sunt în catalog.\n\n"
            f"CATALOG COMPLET AL BIBLIOTECII:\n{lib_list}"
        )
        user_prompt = (
            f"Cărți citite de elev (nu le recomanda din nou):\n{read_list}\n\n"
            f"Cărți deja împrumutate/solicitate de elev:\n{borrowed_list}\n\n"
            "Recomandă 3-4 cărți disponibile din catalog pe care elevul nu le-a citit și nu le are deja. "
            "Pentru fiecare menționează titlul exact din catalog, autorul și de ce i-ar plăcea elevului (1-2 propoziții). "
            "Răspunde în română, prietenos."
        )

        raspuns_ai = _groq_chat(client, user_prompt, system_message=system_prompt)
        return jsonify({'success': True, 'recommendations': raspuns_ai}), 200
    except Exception:
        logger.exception('Eroare AI recommend')
        return jsonify({'success': False, 'message': 'Cererea AI a eșuat'}), 500

def ai_review_assist():
    data = request.get_json(silent=True) or {}
    ciorna = (data.get('draft') or '').strip()
    titlu_carte = (data.get('titlu') or '').strip()

    if not ciorna:
        return jsonify({'success': False, 'message': 'ciorna (draft) este obligatorie'}), 400

    client = _get_groq_client()
    if not client:
        return jsonify({'success': False, 'message': 'AI neconfigurat'}), 503

    try:
        system_prompt = (
            "Ești un asistent pentru recenzii de carte. "
            "Rescrie ciorna de recenzie a elevului ca o recenzie coerentă, bine scrisă, de 2-4 propoziții. "
            "Păstrează exact opinia și tonul original al elevului — nu schimba dacă e pozitivă sau negativă. "
            "Nu adăuga informații inventate. Răspunde DOAR cu textul recenziei, fără explicații."
        )
        user_prompt = f'Carte: "{titlu_carte}"\nGândul brut al elevului:\n"{ciorna}"'
        raspuns_ai = _groq_chat(client, user_prompt, system_message=system_prompt)
        return jsonify({'success': True, 'review': raspuns_ai}), 200
    except Exception:
        logger.exception('Eroare AI review-assist')
        return jsonify({'success': False, 'message': 'Cererea AI a eșuat'}), 500

def ai_book_summary(carte_id):
    client = _get_groq_client()
    if not client:
        return jsonify({'success': False, 'message': 'AI neconfigurat'}), 503

    try:
        book_row = db.session.execute(
            text("SELECT titlu, autor FROM carti WHERE carte_id = :id"), {'id': carte_id}
        ).fetchone()
        if not book_row:
            return jsonify({'success': False, 'message': 'Cartea nu a fost găsită'}), 404

        reviews = db.session.execute(
            text("SELECT nota, comentariu FROM recenzii WHERE carte_id = :id LIMIT 20"), {'id': carte_id}
        ).fetchall()

        if not reviews:
            return jsonify({'success': True, 'summary': '', 'no_reviews': True}), 200

        review_text = '\n'.join(f'- Nota {r[0]}/5: {r[1]}' for r in reviews)
        system_prompt = (
            "Ești un asistent de bibliotecă. Rezumă opinia generală a cititorilor despre o carte pe baza recenziilor primite. "
            "Scrie un rezumat de 2-3 propoziții. "
            "Menționează dacă e apreciată sau nu și de ce. Răspunde în română."
        )
        user_prompt = (
            f'Carte: "{book_row[0]}" de {book_row[1]}\n'
            f"Recenzii de la cititori:\n{review_text}"
        )
        raspuns_ai = _groq_chat(client, user_prompt, system_message=system_prompt)
        return jsonify({'success': True, 'summary': raspuns_ai}), 200
    except Exception:
        logger.exception('Eroare AI book-summary pentru carte_id=%d', carte_id)
        return jsonify({'success': False, 'message': 'Cererea AI a eșuat'}), 500

def ai_chat():
    data = request.get_json(silent=True) or {}
    message = (data.get('message') or '').strip()
    if not message:
        return jsonify({'success': False, 'message': 'mesajul este obligatoriu'}), 400

    client = _get_groq_client()
    if not client:
        return jsonify({'success': False, 'message': 'AI neconfigurat'}), 503

    try:
        books = db.session.execute(
            text("SELECT carte_id, titlu, autor, gen, stoc_disponibil FROM carti ORDER BY titlu")
        ).fetchall()
        book_list = '\n'.join(
            f'- [ID:{r[0]}] {r[1]} de {r[2]} (gen: {r[3]}) — {"disponibil" if r[4] > 0 else "indisponibil"}'
            for r in books
        )

        user = get_current_user()
        context_utilizator = ''
        if user:
            read_rows = db.session.execute(
                text("SELECT c.titlu, c.autor FROM carti_citite cc JOIN carti c ON cc.carte_id = c.carte_id WHERE cc.user_id = :uid"),
                {'uid': user['user_id']}
            ).fetchall()
            if read_rows:
                context_utilizator = '\nCărți citite de utilizatorul curent: ' + ', '.join(f'"{r[0]}"' for r in read_rows) + '\n'

        system_prompt = (
            "Ești asistentul virtual al bibliotecii școlii CNI Suceava. "
            "Răspunzi scurt, prietenos și în română. "
            "Folosește DOAR informațiile din catalogul de mai jos — nu inventa cărți sau autori.\n\n"
            f"CATALOG COMPLET:\n{book_list}\n"
            f"{context_utilizator}"
        )
        raspuns_ai = _groq_chat(client, message, system_message=system_prompt)
        return jsonify({'success': True, 'reply': raspuns_ai}), 200
    except Exception:
        logger.exception('Eroare AI chat')
        return jsonify({'success': False, 'message': 'Cererea AI a eșuat'}), 500
