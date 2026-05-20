import sqlite3
conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute("CREATE TABLE hash_infos (username_full text, username text)")
c.execute("INSERT INTO hash_infos VALUES ('DOMAIN\\user1', 'user1')")
c.execute("INSERT INTO hash_infos VALUES ('user2', 'user2')")
conn.commit()
