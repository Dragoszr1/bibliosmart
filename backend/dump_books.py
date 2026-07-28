import pymysql
import json

conn = pymysql.connect(host='localhost', user='root', password='rootpass112', db='biblioteca')
cursor = conn.cursor(pymysql.cursors.DictCursor)
cursor.execute('SELECT carte_id, titlu FROM carti LIMIT 10')
with open('books_out.json', 'w', encoding='utf-8') as f:
    json.dump(cursor.fetchall(), f)
