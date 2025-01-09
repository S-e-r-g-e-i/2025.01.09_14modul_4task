""" Домашнее задание по теме "План написания админ панели" Часть 2"""

import sqlite3


def initiate_db():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')

    # for i in range(1, 11):      # создание 4 срок записей в таблице
    #     cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
    #                    (f"Продукт {i}", f"Описание {i}", i * 500))

    connection.commit()    # совершить
    connection.close()     # закрыть


def get_all_products():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Products")
    prod_data = cursor.fetchall()

    connection.commit()  # совершить
    connection.close()  # закрыть
    return prod_data    # возвращаем всю таблицу в виде списка кортежей


# initiate_db()
# get_all_products()
