import sqlite3

db_path = '/home/feri/Templates/Program/Task/Bg/instance/data.db'

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

table_name = 'data'

query = f"SELECT * FROM {table_name}"
cursor.execute(query)

columns = [description[0] for description in cursor.description]
rows = cursor.fetchall()

print(f"Columns: {columns}")
print(f"Rows: {rows}")

connection.close()
