import sqlite3
from dpat import Config, DatabaseManager, NTDSProcessor

config = Config(ntds_file="sample_data/customer.ntds", cracked_file="sample_data/oclHashcat.pot", min_password_length=8)
db = DatabaseManager(config)
db.create_schema([])

ntds = NTDSProcessor(config, db)
ntds.process_ntds_file()

# Let's see what is in hash_infos
db.cursor.execute("SELECT username_full, username FROM hash_infos LIMIT 5")
print(db.cursor.fetchall())
