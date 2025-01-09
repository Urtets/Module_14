import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
id INT,
username TEXT,
first_name TEXT,
block INT
);
''')


def add_user(user_id, username, first_name):
    check_user = cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))

    if check_user.fetchone() is None:
        cursor.execute(f'''
    INSERT INTO Users VALUES('{user_id}', '{username}', '{first_name}', 0)
''')
    connection.commit()


connection.commit()
connection.close()
