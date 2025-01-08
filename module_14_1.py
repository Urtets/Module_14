import sqlite3

connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')


# cursor.execute(" CREATE INDEX IF NOT EXISTS idx_email ON Users (email")

for i in range(1, 11):
    name = f'User{i}'
    e_mail = f'example{i}@gmail.com'
    age = i * 10
    balance = 1000
    cursor.execute(" INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)", (f'{name}', f'{e_mail}', str(age), str(balance)))

cursor.execute(" UPDATE Users SET balance = ? WHERE id = 1 OR id % 2 = 0", (500,))

for i in range(1, 11):
    if i % 3 == 1:
        cursor.execute(" DELETE FROM Users WHERE id = ?", (i,))

cursor.execute(" SELECT * FROM Users WHERE age != 60")

users = cursor.fetchall()
for user in users:
    id, username, email_, age, balance = user
    print(f"Имя: {username} | Почта: {email_} | Возраст: {age} | Баланс: {balance}")

connection.commit()
connection.close()