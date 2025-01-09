import sqlite3
from product_text import reducer_list
from product_text import Reducer




def create_db():
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
                                                                                                reducer.title, reducer.description,
                                                                                                reducer.price))
    connection.commit()
    connection.close()

# create_db()

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

if __name__ == '__main__':
    prod_list = get_all_products()
    print(prod_list)