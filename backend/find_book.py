import pymysql
conn = pymysql.connect(host='localhost', user='root', password='rootpass112', db='biblioteca')
cursor = conn.cursor(pymysql.cursors.DictCursor)
cursor.execute("SELECT carte_id, titlu FROM carti WHERE titlu LIKE '%1984%' LIMIT 10")
for row in cursor.fetchall():
    print(row['carte_id'], row['titlu'])
