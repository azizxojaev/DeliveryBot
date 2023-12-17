import sqlite3 as sql

con = sql.connect("database.db")
cur = con.cursor()


def create_tables():
    global con, cur
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER NOT NULL,
                username VARCHAR(25) NOT NULL,
                lang INTEGER NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(25) NOT NULL,
                review TEXT NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS locations (
                id INTEGER NOT NULL,
                address TEXT NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name VARCHAR(20) NOT NULL,
                category_name_uz VARCHAR(20) NOT NULL,
                photo_url TEXT NOT NULL,
                photo_url_uz TEXT NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name VARCHAR(30) NOT NULL,
                product_name_uz VARCHAR(30) NOT NULL,
                price_mini TEXT NOT NULL,
                price_big TEXT NOT NULL,
                about TEXT,
                about_uz TEXT,
                category INTEGER NOT NULL,
                photo_url TEXT NOT NULL,
                photo_url_uz TEXT NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS basket (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                products TEXT NOT NULL,
                price TEXT NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                status VARCHAR(50) NOT NULL,
                addres TEXT NOT NULL,
                products TEXT NOT NULL,
                pay_type VARCHAR(20) NOT NULL,
                price TEXT NOT NULL,
                date TEXT NOT NULL,
                phone_number VARCHAR(20) NOT NULL,
                user_id INTEGER NOT NULL,
                time VARCHAR(5)
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS admins (
                id INTEGER NOT NULL
    )""")

async def delete_review(id):
    cur.execute(f"DELETE FROM reviews WHERE id = {id}")
    con.commit()

async def select_review(id):
    return cur.execute(f"SELECT * FROM reviews WHERE id = {id}").fetchone()

async def select_all_reviews():
    return cur.execute("SELECT * FROM reviews").fetchall()

async def delete_admin(id):
    cur.execute(f"DELETE FROM admins WHERE id = {id}")
    con.commit()

async def insert_admin(id):
    cur.execute("INSERT INTO admins VALUES (?)", (id,))
    con.commit()

async def select_all_admins():
    return cur.execute("SELECT id FROM admins").fetchall()

async def select_admins(id):
    return cur.execute(f"SELECT id FROM admins WHERE id = {id}").fetchone()

async def delete_from_basket(id, product_name, lang):
    global con, cur
    current_products = cur.execute(f"SELECT products FROM basket WHERE user_id = {id}").fetchone()[0].split("; ")
    products_text = ""
    for i in current_products:
        if i != "":
            if i != product_name:
                products_text += i + "; "
    if products_text == "":
        cur.execute(f"DELETE FROM basket WHERE user_id = {id}")
    else:
        quantity = current_products.count(product_name)
        if lang == 0:
            product = product_name.replace(" биг", "")
            product = product.replace(" мини", "")
            if product_name.endswith("мини"):
                price = cur.execute(f"SELECT price_mini FROM products WHERE product_name = '{product}'").fetchone()[0]
            else:
                price = cur.execute(f"SELECT price_big FROM products WHERE product_name = '{product}'").fetchone()[0]
        else:
            product = product_name.replace(" big", "")
            product = product.replace(" mini", "")
            if product_name.endswith("mini"):
                price = cur.execute(f"SELECT price_mini FROM products WHERE product_name_uz = '{product}'").fetchone()[0]
            else:
                price = cur.execute(f"SELECT price_big FROM products WHERE product_name_uz = '{product}'").fetchone()[0]
        price = int(price.replace(" ", "")) * quantity
        basket_price = int(cur.execute(f"SELECT price FROM basket WHERE user_id = {id}").fetchone()[0].replace(" ", ""))
        sum = basket_price - price
        sum = '{:,.0f}'.format(sum).replace(',', ' ')
        cur.execute(f"UPDATE basket SET products = '{products_text}', price = '{sum}' WHERE user_id = {id}")
    con.commit()

async def insert_start(id, username):
    global con, cur
    if cur.execute(f"SELECT * FROM users WHERE id = {id}").fetchone() == None:
        cur.execute("INSERT INTO users VALUES(?, ?, ?)", (id, username, 0))
        con.commit()

async def get_lang(id):
    global con, cur
    if cur.execute(f"SELECT lang FROM users WHERE id = {id}").fetchone() != None:
        return cur.execute(f"SELECT lang FROM users WHERE id = {id}").fetchone()[0]
    else:
        return 0

async def change_lang(id, lang):
    global con, cur
    cur.execute(f"UPDATE users SET lang = {lang} WHERE id = {id}")
    try:
        products_list = cur.execute(f"SELECT products FROM basket WHERE user_id = {id}").fetchone()[0].split('; ')
        products_text = ""
        if lang == 0:
            for i in products_list:
                if i != "":
                    if i.endswith(" big"):
                        product = i.replace(" big", "")
                        products_text += cur.execute(f"SELECT product_name FROM products WHERE product_name_uz = '{product}'").fetchone()[0] + " биг" + "; "
                    elif i.endswith(" mini"):
                        product = i.replace(" mini", "")
                        products_text += cur.execute(f"SELECT product_name FROM products WHERE product_name_uz = '{product}'").fetchone()[0] + " мини" + "; "
                    else:
                        products_text += cur.execute(f"SELECT product_name FROM products WHERE product_name_uz = '{product}'").fetchone()[0] + "; "
        elif lang == 1:
            for i in products_list:
                if i != "":
                    if i.endswith(" биг"):
                        product = i.replace(" биг", "")
                        products_text += cur.execute(f"SELECT product_name_uz FROM products WHERE product_name = '{product}'").fetchone()[0] + " big" + "; "
                    elif i.endswith(" мини"):
                        product = i.replace(" мини", "")
                        products_text += cur.execute(f"SELECT product_name_uz FROM products WHERE product_name = '{product}'").fetchone()[0] + " mini" + "; "
                    else:
                        products_text += cur.execute(f"SELECT product_name_uz FROM products WHERE product_name = '{product}'").fetchone()[0] + "; "
        cur.execute(f"UPDATE basket SET products = '{products_text}' WHERE user_id = '{id}'")
    except:
        pass
    con.commit()

async def add_review(username, review):
    global con, cur
    if username == None:
        username = "None"
    cur.execute("INSERT INTO reviews (username, review) VALUES (?, ?)", (username, review))
    con.commit()

async def insert_location(id, address):
    global con, cur
    if cur.execute(f"SELECT * FROM locations WHERE id = {id} AND address = '{address}'").fetchone() == None:
        cur.execute("INSERT INTO locations VALUES(?, ?)", (id, address))
        con.commit()

async def select_locations(id):
    global con, cur
    return cur.execute(f"SELECT address FROM locations WHERE id = {id}").fetchall()

async def select_categories(lang):
    global con, cur
    if lang == 0:
        return cur.execute(f"SELECT category_name FROM categories").fetchall()
    else:
        return cur.execute(f"SELECT category_name_uz FROM categories").fetchall()

async def select_all_categories():
    return cur.execute("SELECT * FROM categories").fetchall()

async def delete_category(id):
    cur.execute(f"DELETE FROM categories WHERE id = '{id}'")
    con.commit()

async def get_category(category_name, lang):
    global con, cur
    if lang == 0:
        return cur.execute(f"SELECT * FROM categories WHERE category_name = '{category_name}'").fetchone()
    else:
        return cur.execute(f"SELECT * FROM categories WHERE category_name_uz = '{category_name}'").fetchone()
    
async def get_product(category, lang):
    global con, cur
    if lang == 0:
        return cur.execute(f"SELECT product_name FROM products WHERE category = '{category}'").fetchall()
    else:
        return cur.execute(f"SELECT product_name_uz FROM products WHERE category = '{category}'").fetchall()

async def get_product_info(name, lang):
    global con, cur
    if lang == 0:
        return cur.execute(f"SELECT * FROM products WHERE product_name = '{name}'").fetchone()
    else:
        return cur.execute(f"SELECT * FROM products WHERE product_name_uz = '{name}'").fetchone()
    
async def get_product_by_id(size, id):
    global con, cur
    if size == "max":
        return cur.execute(f"SELECT price_big FROM products WHERE id = '{id}'").fetchone()
    elif size == "min":
        return cur.execute(f"SELECT price_mini FROM products WHERE id = '{id}'").fetchone()
    
async def insert_basket(user_id, products, price):
    global con, cur
    if cur.execute(f"SELECT * FROM basket WHERE user_id = '{user_id}'").fetchone() == None:
        cur.execute("INSERT INTO basket (user_id, products, price) VALUES (?, ?, ?)", (user_id, products, price))
        con.commit()
    else:
        current_products = cur.execute(f"SELECT products FROM basket WHERE user_id = '{user_id}'").fetchone()[0]
        result_products = current_products + products
        current_price = cur.execute(f"SELECT price FROM basket WHERE user_id = '{user_id}'").fetchone()[0]
        current_price = current_price.replace(" ", "")
        current_price = int(current_price)
        new_price = str(price)
        new_price = new_price.replace(" ", "")
        new_price = int(new_price)
        result_price = current_price + new_price
        str_num = str(result_price)
        formatted_price = ' '.join([str_num[:-3], str_num[-3:]])
        cur.execute(f"UPDATE basket SET products = '{result_products}', price = '{formatted_price}' WHERE user_id = '{user_id}'")
        con.commit()

async def select_by_id(id):
    global con, cur
    return cur.execute(f"SELECT * FROM products WHERE id = '{id}'").fetchone()

async def select_basket(id):
    global con, cur
    if cur.execute(f"SELECT * FROM basket WHERE user_id = '{id}'").fetchone() != None:
        if cur.execute(f"SELECT products FROM basket WHERE user_id = '{id}'").fetchone()[0] == "":
            cur.execute(f"DELETE FROM basket WHERE user_id = '{id}'")
            con.commit()
            return "none"
        else:
            return cur.execute(f"SELECT * FROM basket WHERE user_id = '{id}'").fetchone()
    else:
        return "none"
    
async def clear_basket(id):
    global con, cur
    cur.execute(f"DELETE FROM basket WHERE user_id = '{id}'")
    con.commit()

async def insert_order(status, addres, products, pay_type, price, date, phone_number, user_id, time):
    global con, cur
    cur.execute(f"INSERT INTO orders (status, addres, products, pay_type, price, date, phone_number, user_id, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (status, addres, products, pay_type, price, date, phone_number, user_id, time))
    con.commit()
    return cur.execute(f"SELECT * FROM orders WHERE user_id = {user_id}").fetchall()[-1]

async def select_orders(id):
    global con, cur
    return cur.execute(f"SELECT * FROM orders WHERE user_id = {id}").fetchall()

async def select_order_by_id(id):
    return cur.execute(f"SELECT * FROM orders WHERE id = {id}").fetchone()

async def update_status_order(id):
    cur.execute(f"UPDATE orders SET status = 'delivered' WHERE id = {id}")
    con.commit()

async def delete_order(id):
    cur.execute(f"DELETE FROM orders WHERE id = {id}")
    con.commit()

async def select_all_orders():
    global con, cur
    return cur.execute(f"SELECT * FROM orders WHERE status = 'new'").fetchall()

async def delete_product(id):
    cur.execute(f"DELETE FROM products WHERE id = {id}")
    con.commit()

async def select_all_products():
    return cur.execute("SELECT * FROM products").fetchall()

async def insert_product(product_name, product_name_uz, price_mini, price_big, about, about_uz, category, photo):
    cur.execute(f"INSERT INTO products (product_name, product_name_uz, price_mini, price_big, about, about_uz, category, photo_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (product_name, product_name_uz, price_mini, price_big, about, about_uz, category, photo))
    con.commit()

async def insert_category(ru, uz, photo_ru, photo_uz):
    cur.execute("INSERT INTO categories (category_name, category_name_uz, photo_url, photo_url_uz) VALUES (?, ?, ?, ?)", (ru, uz, photo_ru, photo_uz))
    con.commit()