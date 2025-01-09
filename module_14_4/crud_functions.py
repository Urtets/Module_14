import sqlite3

from product_text import Reducer
from product_text import reducer_list


def initiate_db():
    connection = sqlite3.connect('bot_db.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    );
    ''')
    for reducer in reducer_list:
        cursor.execute('INSERT INTO Products (id, title, description, price) VALUES (?, ?, ?, ?)', (reducer.id,
                                                                                                    reducer.title,
                                                                                                    reducer.description,
                                                                                                    reducer.price))
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    );
    ''')
    connection.commit()
    connection.close()


# initiate_db()

def get_all_products():
    connection = sqlite3.connect('bot_db.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    product_list = []
    for product in products:
        id, title, description, price = product
        # print(f'id: {id} | Название: {title} | Описание: {description} | Стоимость: {price}')
        product_list.append(Reducer(id, title, description, price))
    connection.commit()
    connection.close()
    return product_list


def add_user(username, email, age):
    connection = sqlite3.connect('bot_db.db')
    cursor = connection.cursor()
    if is_included(username):
        return
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (username, email, age, str(1000)))
    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect('bot_db.db')
    cursor = connection.cursor()
    name_check = cursor.execute('SELECT COUNT(*) FROM Users WHERE username = ?', (username,)).fetchone()[0]
    print(name_check)
    decision = False
    if name_check > 0:
        decision = True

    connection.commit()
    connection.close()
    return decision


if __name__ == '__main__':
    prod_list = get_all_products()
    print(prod_list)
