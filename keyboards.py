from aiogram.types import *
from datetime import datetime


text = {
    "start1": ["🍴 Меню", "🍴 Menyu"],
    "start2": ["🛍 Мои заказы", "🛍 Mening buyurtmalarim"],
    "start3": ["✍️ Оставить отзыв", "✍️ Fikr bildirish"],
    "start4": ["⚙️ Настройки", "⚙️ Sozlamalar"],
    "back": ["⬅️ Назад", "⬅️ Ortga"],
    "next": ["⏩ Следующий", "⏩ Keyingi"],
    "prev": ["⏪ Предыдущий", "⏪ Oldingi"],
    "update": ["🔄 Обновить", "🔄 Yangilash"],
    "settingsLangChange": ["Изменить язык", "Tilni o'zgartirish"],
    "addres1": ["🗺 Мои адреса", "🗺 Mening manzillarim"],
    "addres2": ["📍 Отправить геолокацию", "📍 Geolokatsiyani yuboring"],
    "yes": ["✅ Да", "✅ Ha"],
    "no": ["❌ Нет", "❌ Yo'q"],
    "basket": ["📥 Корзина", "📥 Savat"],
    "mini": ["Мини", "Mini"],
    "big": ["Биг", "Big"],
    "som": ["сум", "so'm"],
    "basket2": ["📥 Добавить в корзину", "📥 Savatga qo'shish"],
    "makeOrder": ["🚖 Оформить заказ", "🚖 Buyurtma berish"],
    "clearBasket": ["🗑 Очистить корзину", "🗑 Savatni tozalash"],
    "selectTime": ["⏳ Время доставки", "⏳ Yetkazib berish vaqti"],
    "myPhoneNumber": ["📞 Мой номер", "📞 Mening raqamim"],
    "payType": ["Наличные", "Naqd pul"],
    "done": ["Наличные", "Naqd pul"],
    "confirm": ["✅ Подтвердить", "✅ Tasdiqlash"],
    "cancel": ["❌ Отменить", "❌ Bekor qilish"],
    "adminOrders": ["Заказы", "Buyurtmalar"],
    "adminCategory": ["Категории", "Kategoriyalar"],
    "adminCategory2": ["Добавить категорию", "Kategoriya qoshish"],
    "adminCategory3": ["Удалить категорию", "Kategoriya ochirish"],
    "adminProduct1": ["Добавить продукт", "Mahsulot qoshish"],
    "adminProduct2": ["Удалить продукт", "Mahsulot ochirish"],
    "adminProduct": ["Продукты", "Mahsulotlar"],
    "adminList": ["Админы", "Adminlar"],
    "adminReviews": ["Отзывы", "Fikrlar"],
    "adminOrder": ["Заказ № ", "Buyurtma № "],
    "delivered": ["✅ Доставлено", "✅ Yetkazib berildi"],
    "delete": ["🗑 Удалить", "🗑 O'chirish"],
    "adminAdd": ["Добавить админа", "Admin qoshish"],
    "adminDelete": ["Удалить админа", "Admin ochirish"]
}

async def adminReview_inline(lang, review):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton(text["back"][lang], callback_data="review_back"),
        InlineKeyboardButton(text["delete"][lang], callback_data=f"review_del:{review[0]}")
    )
    return btn

async def adminReviews_inline(lang, reviews, page):
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(
        InlineKeyboardButton(text["back"][lang], callback_data="back_admin")
    )
    btn.add(
        InlineKeyboardButton(text["prev"][lang], callback_data="review_prev"),
        InlineKeyboardButton(text["next"][lang], callback_data="review_next")
    )
    index = page * 8
    btn_len = 0
    for i in range(index - 8, index):
        try:
            btn.add(
                InlineKeyboardButton(f"{reviews[i][2]}", callback_data=f"review:{reviews[i][0]}")
            )
            btn_len += 1
        except IndexError:
            pass
    if btn_len != 0:
        return btn
    else:
        return None

async def adminsDelete_inline(lang, admins, page):
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(
        InlineKeyboardButton(text["back"][lang], callback_data="admin_back")
    )
    btn.add(
        InlineKeyboardButton(text["prev"][lang], callback_data="admin_prev"),
        InlineKeyboardButton(text["next"][lang], callback_data="admin_next")
    )
    index = page * 8
    btn_len = 0
    for i in range(index - 8, index):
        try:
            btn.add(
                InlineKeyboardButton(f"🗑 {admins[i][0]}", callback_data=f"del_admin:{admins[i][0]}")
            )
            btn_len += 1
        except IndexError:
            pass
    if btn_len != 0:
        return btn
    else:
        return None

async def adminBack_inline2(lang):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton(text["back"][lang], callback_data="admin_back")
    )
    return btn

async def admins_inline(lang):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton(text["back"][lang], callback_data="back_admin")
    )
    btn.add(
        InlineKeyboardButton(text["adminAdd"][lang], callback_data="admins_add"),
        InlineKeyboardButton(text["adminDelete"][lang], callback_data="admins_delete")
    )
    return btn

async def adminDelete_inline(lang, products, page):
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(
        InlineKeyboardButton(text["back"][lang], callback_data="product_back")
    )
    btn.add(
        InlineKeyboardButton(text["prev"][lang], callback_data="product_prev"),
        InlineKeyboardButton(text["next"][lang], callback_data="product_next")
    )
    index = page * 8
    btn_len = 0
    for i in range(index - 8, index):
        try:
            btn.add(
                InlineKeyboardButton(f"🗑 {products[i][lang + 1]}", callback_data=f"del_product:{products[i][0]}")
            )
            btn_len += 1
        except IndexError:
            pass
    if btn_len != 0:
        return btn
    else:
        return None

async def adminOrder_inline(lang, id):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton(text["delivered"][lang], callback_data=f"delivered_{id}"),
        InlineKeyboardButton(text["delete"][lang], callback_data=f"delete_{id}"),
        InlineKeyboardButton(text["back"][lang], callback_data=f"back_orders")
    )
    return btn

async def admin_inline(lang):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton(text["adminOrders"][lang], callback_data="see_orders"),
        InlineKeyboardButton(text["adminCategory"][lang], callback_data="category"),
        InlineKeyboardButton(text["adminProduct"][lang], callback_data="product"),
        InlineKeyboardButton(text["adminList"][lang], callback_data="admins"),
        InlineKeyboardButton(text["adminReviews"][lang], callback_data="reviews")
    )
    return btn

async def adminCategory_inline(lang):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton(text["back"][lang], callback_data="back_admin"),
        InlineKeyboardButton(text["adminCategory2"][lang], callback_data="add_category"),
        InlineKeyboardButton(text["adminCategory3"][lang], callback_data="delete_category")
    )
    return btn

async def adminProduct_inline(lang):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton(text["back"][lang], callback_data="back_admin"),
        InlineKeyboardButton(text["adminProduct1"][lang], callback_data="add_product"),
        InlineKeyboardButton(text["adminProduct2"][lang], callback_data="del_product")
    )
    return btn

async def adminBack_inline(lang):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton(text["back"][lang], callback_data="category_back")
    )
    return btn

async def adminProductBack_inline(lang):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton(text["back"][lang], callback_data="product_back")
    )
    return btn

async def deleteCategory_inline(lang, categories, page):
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(
        InlineKeyboardButton(text["back"][lang], callback_data="product_back")
    )
    btn.add(
        InlineKeyboardButton(text["prev"][lang], callback_data="category_prev"),
        InlineKeyboardButton(text["next"][lang], callback_data="category_next")
    )
    index = page * 5
    btn_len = 0
    for i in range(index - 5, index):
        try:
            btn.add(
                InlineKeyboardButton(f"🗑 {categories[i][lang + 1]}", callback_data=f"delete_category:{categories[i][0]}")
            )
            btn_len += 1
        except IndexError:
            pass
    if btn_len != 0:
        return btn
    else:
        return None
    
async def categories_inline(lang, categories, page):
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(
        InlineKeyboardButton(text["back"][lang], callback_data="product_back")
    )
    btn.add(
        InlineKeyboardButton(text["prev"][lang], callback_data="add_category_prev"),
        InlineKeyboardButton(text["next"][lang], callback_data="add_category_next")
    )
    index = page * 5
    btn_len = 0
    for i in range(index - 5, index):
        try:
            btn.add(
                InlineKeyboardButton(f"{categories[i][lang + 1]}", callback_data=f"select_category:{categories[i][0]}")
            )
            btn_len += 1
        except IndexError:
            pass
    if btn_len != 0:
        return btn
    else:
        return None

async def adminOrders_inline(lang, orders, page):
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(
        InlineKeyboardButton(text["back"][lang], callback_data="back_admin")
    )
    btn.add(
        InlineKeyboardButton(text["prev"][lang], callback_data="prev"),
        InlineKeyboardButton(text["next"][lang], callback_data="next"),
        InlineKeyboardButton(text["update"][lang], callback_data="update")
    )
    index = page * 5
    btn_len = 0
    for i in range(index - 5, index):
        try:
            btn.add(
                InlineKeyboardButton(f"{text['adminOrder'][lang] + str(orders[i][0])}", callback_data=f"order_{orders[i][0]}")
            )
            btn_len += 1
        except IndexError:
            pass
    if btn_len != 0:
        return btn
    else:
        return None

async def start_reply(lang):
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn.add(
        KeyboardButton(text["start1"][lang])
    )
    btn.add(
        KeyboardButton(text["start2"][lang])
    )
    btn.add(
        KeyboardButton(text["start3"][lang]),
        KeyboardButton(text["start4"][lang])
    )
    return btn

async def settings_reply(lang):
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn.add(
        KeyboardButton(text["settingsLangChange"][lang]),
        KeyboardButton(text["back"][lang])
    )
    return btn

async def lang_reply(lang):
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn.add(
        KeyboardButton("🇷🇺 Русский"),
        KeyboardButton("🇺🇿 O'zbekcha"),
        KeyboardButton(text["back"][lang])
    )
    return btn

async def review_reply(lang):
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn.add(
        KeyboardButton(text["back"][lang])
    )
    return btn

async def location_reply(lang):
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn.add(
        KeyboardButton(text["addres1"][lang])
    )
    btn.add(
        KeyboardButton(text["addres2"][lang], request_location=True),
        KeyboardButton(text["back"][lang])
    )
    return btn

async def locationYesNo_reply(lang):
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn.add(
        KeyboardButton(text["no"][lang]),
        KeyboardButton(text["yes"][lang]),
        KeyboardButton(text["back"][lang])
    )
    return btn

async def adresses_reply(adress_list, lang):
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for i in adress_list:
        btn.add(
            KeyboardButton(f"{i[0]}")
        )
    btn.add(
        KeyboardButton(text["back"][lang])
    )
    return btn

async def categories_reply(categories, lang):
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    try:
        for i in range(0, len(categories), 2):
            btn.add(
                KeyboardButton(f"{categories[i][0]}"),
                KeyboardButton(f"{categories[i+1][0]}")
            )
    except IndexError:
        pass
    if len(categories) % 2 == 1:
        btn.add(
            KeyboardButton(f"{categories[-1][0]}")
        )
    btn.add(
        KeyboardButton(text["basket"][lang]),
        KeyboardButton(text["back"][lang])
    )
    return btn

async def products_reply(products, lang):
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    try:
        for i in range(0, len(products), 2):
            btn.add(
                KeyboardButton(f"{products[i][0]}"),
                KeyboardButton(f"{products[i+1][0]}")
            )
    except IndexError:
        pass
    if len(products) % 2 == 1:
        btn.add(
            KeyboardButton(f"{products[-1][0]}")
        )
    btn.add(
        KeyboardButton(text["back"][lang])
    )
    return btn

async def products_reply2(products, lang):
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn.add(
        KeyboardButton(text["basket"][lang])
    )
    try:
        for i in range(0, len(products), 2):
            btn.add(
                KeyboardButton(f"{products[i][0]}"),
                KeyboardButton(f"{products[i+1][0]}")
            )
    except IndexError:
        pass
    if len(products) % 2 == 1:
        btn.add(
            KeyboardButton(f"{products[-1][0]}")
        )
    btn.add(
        KeyboardButton(text["back"][lang])
    )
    return btn

async def size_inline(min_price, max_price, id, lang):
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(
        InlineKeyboardButton(f"{text['mini'][lang]} {min_price} {text['som'][lang]}", callback_data=f"min_price:{id}"),
        InlineKeyboardButton(f"{text['big'][lang]} {max_price} {text['som'][lang]}", callback_data=f"max_price:{id}")
    )
    return btn

async def size_reply(lang):
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn.add(
        KeyboardButton(text["basket"][lang]),
        KeyboardButton(text["back"][lang])
    )
    return btn

async def quantity_inline(quantity, id, lang):
    btn = InlineKeyboardMarkup(row_width=3)
    btn.add(
        InlineKeyboardButton("-", callback_data=f"quantity:minus:{id}"),
        InlineKeyboardButton(f"{quantity}", callback_data=f"quantity:{id}"),
        InlineKeyboardButton("+", callback_data=f"quantity:plus:{id}"),
        InlineKeyboardButton(text["basket2"][lang], callback_data=f"add_to_cart:{id}")
    )
    return btn

async def basket_inline(lang, products):
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(
        InlineKeyboardButton(text["back"][lang], callback_data="basket_back"),
        InlineKeyboardButton(text["makeOrder"][lang], callback_data="make_order"),
        InlineKeyboardButton(text["clearBasket"][lang], callback_data="clear_basket"),
        InlineKeyboardButton(text["selectTime"][lang], callback_data="select_time")
    )
    for i in products:
        if i != "":
            btn.add(
                InlineKeyboardButton(f"❌ {i}", callback_data=f"delete:{i}")
            )
    return btn

async def phone_inline(lang):
    btn = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn.add(
        KeyboardButton(text["myPhoneNumber"][lang], request_contact=True),
        KeyboardButton(text["back"][lang])
    )
    return btn

async def payType_inline(lang):
    btn = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn.add(
        KeyboardButton(text["payType"][lang]),
        KeyboardButton("Click"),
        KeyboardButton("Payme"),
        KeyboardButton(text["back"][lang])
    )
    return btn

async def order_reply(lang):
    btn = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn.add(
        KeyboardButton(text["confirm"][lang]),
        KeyboardButton(text["cancel"][lang])
    )
    return btn

time_list = ["9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00", "23:30", "0:00", "0:30", "1:00", "1:30", "2:00"]

async def time_inline(lang):
    btn = InlineKeyboardMarkup(row_width=2)
    time = datetime.now()
    index = 0
    for i in range(len(time_list)):
        if int(time.hour) < int(time_list[i].split(":")[0]):
            index = i
            break
    new_time = time_list[index:len(time_list)]
    btn.add(
        InlineKeyboardButton(text["back"][lang], callback_data=f"time_back"),
        InlineKeyboardButton(text["next"][lang], callback_data=f"time_next")
    )
    for i in range(0, 5, 2):
        try:
            last_time = new_time[i+1]
            btn.add(
                InlineKeyboardButton(f"{new_time[i]}", callback_data=f"time_{new_time[i]}"),
                InlineKeyboardButton(f"{new_time[i+1]}", callback_data=f"time_{new_time[i+1]}")
            )
        except IndexError:
            last_time = new_time[i]
            btn.add(
                InlineKeyboardButton(f"{new_time[i]}", callback_data=f"time_{new_time[i]}")
            )
        finally:
            pass
    return btn, last_time

async def time_inline_next(lang, last_time):
    index = time_list.index(last_time) + 1
    new_time = time_list[index:len(time_list)]
    if len(new_time) != 0:
        btn = InlineKeyboardMarkup(row_width=2)
        btn.add(
            InlineKeyboardButton(text["back"][lang], callback_data=f"time_back"),
            InlineKeyboardButton(text["next"][lang], callback_data=f"time_next")
        )
        times_len = 0
        last = new_time[-1]
        times = []
        for i in range(0, 5, 2):
            try:
                btn.add(
                    InlineKeyboardButton(f"{new_time[i]}", callback_data=f"time_{new_time[i]}"),
                    InlineKeyboardButton(f"{new_time[i+1]}", callback_data=f"time_{new_time[i+1]}")
                )
                last = new_time[i+1]
                times_len += 1
                times.append(new_time[i])
                times.append(new_time[i+1])
            except:
                pass
        if len(new_time) % 2 != 0 and times_len != 3:
            last = new_time[-1]
            btn.add(
                InlineKeyboardButton(f"{new_time[-1]}", callback_data=f"time_{new_time[-1]}")
            )
        return btn, last
    else:
        return "none", last_time
