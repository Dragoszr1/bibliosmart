import os
import json
import bcrypt
import logging
from sqlalchemy import text
from app import create_app
from app.database import db
from unittest.mock import patch

logging.basicConfig(level=logging.ERROR)

def print_interaction(step_name, method, url, req_payload, status_code, res_payload):
    """Helper to format the input/output of each test step clearly."""
    interaction = {
        "step": step_name,
        "request": {
            "method": method,
            "url": url,
            "payload": req_payload
        },
        "response": {
            "status_code": status_code,
            "payload": res_payload
        }
    }
    print(json.dumps(interaction, indent=2))
    print("-" * 60)

def setup_test_data(app):
    with app.app_context():
        db.create_all()
        
        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS coduri_verificare (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                code VARCHAR(10) NOT NULL,
                temp_token VARCHAR(255) NOT NULL,
                expires_at DATETIME NOT NULL
            )
        """))
        db.session.commit()
        
        admin_email = "admin_test_auto@cni-sv.ro"
        user_email = "user_test_auto@cni-sv.ro"
        password = "password123"
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        for email, username, rol in [(admin_email, 'AdminTest', 'bibliotecar'), (user_email, 'UserTest', 'user')]:
            exists = db.session.execute(text("SELECT user_id FROM users WHERE email = :e"), {'e': email}).fetchone()
            if not exists:
                db.session.execute(
                    text("INSERT INTO users (username, email, hashed_password, rol, club) VALUES (:u, :e, :h, :r, 1)"),
                    {'u': username, 'e': email, 'h': hashed, 'r': rol}
                )
            else:
                db.session.execute(
                    text("UPDATE users SET club = 1, hashed_password = :h WHERE email = :e"),
                    {'h': hashed, 'e': email}
                )
        
        book = db.session.execute(text("SELECT carte_id FROM carti LIMIT 1")).fetchone()
        if not book:
            db.session.execute(
                text("INSERT INTO carti (titlu, autor, ISBN, stoc_total, stoc_disponibil, imprumutat, gen) "
                     "VALUES ('Carte Test', 'Autor Test', '1234567890123', 5, 5, 0, 'Fictiune')")
            )
        db.session.commit()
        
        book = db.session.execute(text("SELECT carte_id FROM carti LIMIT 1")).fetchone()
        return book[0]

def login_flow(app, email, password="password123"):
    client = app.test_client()
    with app.app_context():
        req_payload = {'email': email, 'password': password}
        with patch('app.controllers.auth_controller.send_email') as mock_send_email:
            res1 = client.post('/api/auth/login', json=req_payload)
            assert res1.status_code == 200, f"Login request failed: {res1.get_data(as_text=True)}"
            
        data1 = res1.get_json()
        print_interaction(f"Login Init ({email})", "POST", "/api/auth/login", req_payload, res1.status_code, data1)
        
        temp_token = data1['temp_token']
        
        row = db.session.execute(
            text("SELECT code FROM coduri_verificare WHERE temp_token = :t"),
            {'t': temp_token}
        ).fetchone()
        code = row[0]
        
        req2_payload = {'temp_token': temp_token, 'code': code}
        res2 = client.post('/api/auth/verify-code', json=req2_payload)
        data2 = res2.get_json()
        print_interaction(f"OTP Verify ({email})", "POST", "/api/auth/verify-code", req2_payload, res2.status_code, data2)
        assert res2.status_code == 200, "OTP verification failed"
        
        return client

def run_workflow():
    app = create_app()
    app.testing = True
    
    print("=" * 60)
    print("INTEGRATION TESTS EXECUTION REPORT")
    print("=" * 60)
    
    book_id = setup_test_data(app)
    
    admin_client = login_flow(app, "admin_test_auto@cni-sv.ro")
    user_client = login_flow(app, "user_test_auto@cni-sv.ro")
    
    # 1. Club Activities
    req_activity = {'titlu': 'Test Activity', 'continut': 'Test content', 'tip': 'anunt', 'saptamana': 'curenta'}
    res = admin_client.post('/api/club/activitati', json=req_activity)
    print_interaction("Create Club Activity", "POST", "/api/club/activitati", req_activity, res.status_code, res.get_json())
    activity_id = res.get_json().get('activitate_id')
    
    # 2. Club Comments
    req_comment = {'continut': 'Test comment'}
    res = user_client.post(f'/api/club/activitati/{activity_id}/comentarii', json=req_comment)
    print_interaction("Post Comment", "POST", f"/api/club/activitati/{activity_id}/comentarii", req_comment, res.status_code, res.get_json())
    
    # 3. Club Threads
    req_thread = {'titlu': 'Test Thread', 'continut': 'Test thread content'}
    res = user_client.post('/api/club/threads', json=req_thread)
    print_interaction("Create Thread", "POST", "/api/club/threads", req_thread, res.status_code, res.get_json())
    thread_id = res.get_json().get('thread_id')
    
    # 4. Approve Thread
    res = admin_client.post(f'/api/club/threads/{thread_id}/approve')
    print_interaction("Approve Thread", "POST", f"/api/club/threads/{thread_id}/approve", None, res.status_code, res.get_json())
    
    # 5. Book Request
    res = user_client.post(f'/api/books/{book_id}/request-fizic')
    try:
        res_payload = res.get_json()
    except:
        res_payload = res.get_data(as_text=True)
    print_interaction("Request Book", "POST", f"/api/books/{book_id}/request-fizic", None, res.status_code, res_payload)
    
    # 6. View Requests
    res = admin_client.get('/api/book-requests/')
    print_interaction("Fetch Book Requests", "GET", "/api/book-requests/", None, res.status_code, res.get_json())
    
    json_data = res.get_json()
    requests_list = json_data.get('cereri', [])
    req_id = None
    for r in requests_list:
        if r['carte_id'] == book_id and r['email'] == "user_test_auto@cni-sv.ro":
            req_id = r['cerere_id']
            break
    
    # 7. Approve Book Request
    if req_id:
        req_approve = {
            'status': 'approved',
            'ridicare_de_la': '2026-12-01 10:00',
            'ridicare_pana_la': '2026-12-01 12:00'
        }
        res = admin_client.put(f'/api/book-requests/{req_id}', json=req_approve)
        try:
            res_payload = res.get_json()
        except:
            res_payload = res.get_data(as_text=True)
        print_interaction("Approve Book Request", "PUT", f"/api/book-requests/{req_id}", req_approve, res.status_code, res_payload)
    
    # 8. AI Recommendations
    res = user_client.get('/api/ai/recommend')
    try:
        res_payload = res.get_json()
    except:
        res_payload = res.get_data(as_text=True)
    print_interaction("Fetch AI Recommendations", "GET", "/api/ai/recommend", None, res.status_code, res_payload)

if __name__ == "__main__":
    run_workflow()
