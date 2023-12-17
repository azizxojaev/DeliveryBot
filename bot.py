import logging

from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from database import *   
from keyboards import *
from states import *
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import requests
import datetime

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode="html")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Приниматель адресса
def get_address(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}"
    response = requests.get(url).json()
    address = response['display_name']
    return address

text = {
    "start": ["Выберите одно из следующих", "Quyidagilardan birini tanlang"],
    "action": ["<b>Выберите действие:</b>", "<b>Harakat tanlang:</b>"],
    "selectOrders": ["<b>Выберите заказ:</b>", "<b>Buyurtma tanlang:</b>"],
    "lang": ["<b>Выберите язык:</b>", "<b>Tilni tanlang:</b>"],
    "done": ["<b>✅ Готово</b>", "<b>✅ Tayyor</b>"],
    "review": ["Отправьте ваши отзывы", "Fikringizni yuboring"],
    "thanksForReview": ["Спасибо за ваш отзыв", "Fikr-mulohazangiz uchun rahmat"],
    "myOrders": ["Вы совсем ничего не заказали.", "Siz hech narsa buyurtma bermagansiz"],
    "location": ["Отправьте 📍 геолокацию или выберите адрес доставки", "📍 Geolokatsiyani yuboring yoki yetkazib berish manzilini tanlang"],
    "locationYesNo": ["Адрес, по которому вы хотите заказать:", "Buyurtma bermoqchi bo'lgan manzil:"],
    "locationYesNo2": ["Вы подтверждаете этот адрес?", "Ushbu manzilni tasdiqlaysizmi?"],
    "myAdressesNone": ["У вас нет сохраненных адресов", "Bo'sh"],
    "chooseCategory": ["Выберите категорию.", "Bo'limni tanlang."],
    "myAdressesChoose": ["Выберите адрес.", "Yetkazib berish manzilni tanlang"],
    "addressNotFound": ["По Вашему адресу отсутствует служба доставки!", "Sizning manzilingiz bo'yicha etkazib berish xizmati mavjud emas!"],
    "price": ["Цена:", "Narxi:"],
    "price2": ["сум", "so'm"],
    "emptyBasket": ["Ваша корзина пустая", "Savatingiz boʻsh"],
    "basket": ["В корзине:", "Savatda:"],
    "basketPrice1": ["Товары:", "Mahsulotlar:"],
    "basketPrice2": ["Доставка:", "Yetkazib berish:"],
    "basketPrice3": ["Итого:", "Jami:"],
    "phone": ["Отправьте или введите ваш номер телефона в формате: +998 ** *** ** **\nПримечание: Если вы планируете оплатить заказ онлайн с помощью Click, либо Payme, пожалуйста, укажите номер телефона, на который зарегистрирован аккаунт в соответствующем сервисе", "Telefon raqamingizni quyidagi formatda yuboring yoki kiriting: +998 ** *** ** **\nEslatma: Agar siz onlayn buyurtma uchun Click yoki Payme orqali toʻlashni rejalashtirmoqchi boʻlsangiz, tegishli xizmatda hisob qaydnomasi roʻyxatdan oʻtgan telefon raqamini koʻrsating."],
    "payingType": ["Пожалуйста, выберите тип оплаты", "Toʻlov turini tanlang"],
    "phoneErr": ["Вы ввели номер телефона в неправильном формате.\nПожалуйста, отправьте или введите заново", "Telefon reqmingiz noto'gri, raqamingizni boshqatdan jonating"],
    "order1": ["<b>Ваш заказ:</b>\nАдрес: ", "<b>Sizning buyurtmangiz:</b>\nManzil: "],
    "order2": ["Тип оплаты: ", "To'lov turi: "],
    "new": ["<b>Новый</b>", "<b>Yangi</b>"],
    "delivered": ["<b>✅ Доставлено</b>", "<b>✅ Yetkazib berildi</b>"],
    "status2": ["Статус: ", "Holat: "],
    "order_id": ["Номер заказа: ", "Zakaz raqami: "],
    "addres": ["Адрес: ", "Manzil: "],
    "time": ["Время доставки: ", "Buyurtma vaqti: "],
    "fast": ["Как можно быстрее", "Iloji boricha tezroq"],
    "incorrect": ["Неправильный ввод", "Yaroqsiz kiritish"],
    "addCategory1": ["Введите название категории на русском языке", "Kategoriya ni nomini rus tilida kiriting"],
    "addCategory2": ["Введите название категории на узбекском языке", "Kategoriya ni nomini ozbek tilida kiriting"],
    "addCategory3": ["Отправьте фотографию для категории на русском языке", "Kategoriya ni rus tili uchun rasm yuboring"],
    "addCategory4": ["Отправьте фотографию для категории на узбекском языке", "Kategoriya ni ozbek tili uchun rasm yuboring"],
    "addProduct1": ["Введите название продукта на русском языке", "Mahsulot ni nomini rus tilida kiriting"],
    "addProduct2": ["Введите название продукта на узбекском языке", "Mahsulot ni nomini ozbek tilida kiriting"],
    "addProduct3": ["Введите цену за мини размер (если у товара только 1 размер введите 'none')", "Mini o'lcham uchun narxni kiriting (agar mahsulot faqat 1 o'lchamga ega bo'lsa, 'none' ni kiriting)"],
    "addProduct4": ["Введите цену за биг размер (если у товара только 1 размер введите его цену тут)", "Big o'lcham uchun narxni kiriting (agar mahsulot faqat 1 o'lchamga ega bo'lsa, uning narxini shu yerga kiriting)"],
    "addProduct5": ["Введите описание товара на русском (если его нету введите 'none')", "Mahsulot tavsifini rus tilida kiriting (agar u yo'q bo'lsa, 'none' ni kiriting)"],
    "addProduct6": ["Введите описание товара на узбекском (если его нету введите 'none')", "Mahsulot tavsifini ozbek kiriting (agar u yo'q bo'lsa, 'none' ni kiriting)"],
    "addProduct7": ["Выберите категорию", "Kategoriyani tanlang"],
    "addProduct8": ["Отправьте фотографию для продукта", "Mahsulot uchun rasm yuboring"],
    "addAdmin": ["Введите id админа", "Admin ning ID sini kiriting"],
    "username": ["Пользователь: ", "Foydalanuvchi: "]
}


@dp.message_handler(commands=["start"], state="*")
async def start_handler(message: types.Message, state: FSMContext):
    await state.finish()
    lang = await get_lang(message.from_user.id)
    btn = await start_reply(lang)
    await message.answer(text["start"][lang], reply_markup=btn)
    if message.from_user.username == None:
        username = "None"
    else:
        username = message.from_user.username
    await insert_start(message.from_user.id, username)

# Кнопка Настройки
if True:
    @dp.message_handler(text="⚙️ Настройки")
    @dp.message_handler(text="⚙️ Sozlamalar")
    async def settings_handler(message: types.Message):
        lang = await get_lang(message.from_user.id)
        btn = await settings_reply(lang)
        await message.answer(text["action"][lang], reply_markup=btn)
        await SettingsStates.settings_action.set()
    @dp.message_handler(text="Изменить язык", state=SettingsStates.settings_action)
    @dp.message_handler(text="Tilni o'zgartirish", state=SettingsStates.settings_action)
    async def settingsLang_handler(message: types.Message, state: FSMContext):
        lang = await get_lang(message.from_user.id)
        btn = await lang_reply(lang)
        await message.answer(text["lang"][lang], reply_markup=btn)
        await SettingsStates.lang.set()
    @dp.message_handler(text="⬅️ Назад", state=SettingsStates.settings_action)
    @dp.message_handler(text="⬅️ Ortga", state=SettingsStates.settings_action)
    async def settingsLangBack_handler(message: types.Message, state: FSMContext):
        lang = await get_lang(message.from_user.id)
        btn = await start_reply(lang)
        await message.answer(text["start"][lang], reply_markup=btn)
        await state.finish()
    @dp.message_handler(text="🇷🇺 Русский", state=SettingsStates.lang)
    async def settingsLangRu_handler(message: types.Message, state: FSMContext):
        await change_lang(message.from_user.id, 0)
        lang = await get_lang(message.from_user.id)
        btn = await settings_reply(lang)
        await message.answer(text["done"][lang], reply_markup=btn)
        await SettingsStates.settings_action.set()
    @dp.message_handler(text="🇺🇿 O'zbekcha", state=SettingsStates.lang)
    async def settingsLangUz_handler(message: types.Message, state: FSMContext):
        await change_lang(message.from_user.id, 1)
        lang = await get_lang(message.from_user.id)
        btn = await settings_reply(lang)
        await message.answer(text["done"][lang], reply_markup=btn)
        await SettingsStates.settings_action.set()
    @dp.message_handler(text="⬅️ Назад", state=SettingsStates.lang)
    @dp.message_handler(text="⬅️ Ortga", state=SettingsStates.lang)
    async def settingsLangRuUzBack_handler(message: types.Message, state: FSMContext):
        lang = await get_lang(message.from_user.id)
        btn = await settings_reply(lang)
        await message.answer(text["action"][lang], reply_markup=btn)
        await SettingsStates.settings_action.set()

# Кнопка Отзывы
if True:
    @dp.message_handler(text="✍️ Оставить отзыв")
    @dp.message_handler(text="✍️ Fikr bildirish")
    async def review_handler(message: types.Message):
        lang = await get_lang(message.from_user.id)
        btn = await review_reply(lang)
        await message.answer(text["review"][lang], reply_markup=btn)
        await ReviewStates.review.set()
    @dp.message_handler(text="⬅️ Назад", state=ReviewStates.review)
    @dp.message_handler(text="⬅️ Ortga", state=ReviewStates.review)
    async def reviewBack_handler(message: types.Message, state: FSMContext):
        lang = await get_lang(message.from_user.id)
        btn = await start_reply(lang)
        await message.answer(text["start"][lang], reply_markup=btn)
        await state.finish()
    @dp.message_handler(state=ReviewStates.review)
    async def reviewText_handler(message: types.Message, state: FSMContext):
        lang = await get_lang(message.from_user.id)
        btn = await start_reply(lang)
        await message.answer(text["thanksForReview"][lang], reply_markup=btn)
        await add_review(message.from_user.username, message.text)
        await state.finish()

# Кнопка Мои заказы
if True:
    @dp.message_handler(text="🛍 Мои заказы")
    @dp.message_handler(text="🛍 Mening buyurtmalarim")
    async def myOrders_handler(message: types.Message, state: FSMContext):
        orders = await select_orders(message.from_user.id)
        lang = await get_lang(message.from_user.id)
        if len(orders) == 0:
            await message.answer(text["myOrders"][lang])
        else:
            for i in range(len(orders)):
                products = orders[i][3]
                products = products.split("; ")
                unique_products = []
                for j in products:
                    if j not in unique_products:
                        unique_products.append(j)
                products_text = ""
                quantity_text = 0
                for g in unique_products:
                    if g != "":
                        quantity_text = products.count(g)
                        count_str = str(quantity_text)
                        emoji_str = ""
                        for digit in count_str:
                            emoji_str += emoji[int(digit)]
                        products_text += f"{emoji_str} ✖️ {g}\n"
                current_price = orders[i][5]
                current_price = current_price.replace(" ", "")
                current_price = int(current_price)
                current_price = current_price + 10000
                str_num = str(current_price)
                formatted_price = ' '.join([str_num[:-3], str_num[-3:]])
                await message.answer(f"{text['order_id'][lang]}{orders[i][0]}\n{text['status2'][lang]}{text[orders[i][1]][lang]}\n{text['addres'][lang]}{orders[i][2]}\n\n{products_text}\n{text['order2'][lang]}{orders[i][4]}\n\n<b>{text['basketPrice1'][lang]}</b> {orders[i][5]} {text['price2'][lang]}\n<b>{text['basketPrice2'][lang]}</b> 10 000 {text['price2'][lang]}\n<b>{text['basketPrice3'][lang]}</b> {formatted_price} {text['price2'][lang]}")

# Кнопка Меню
if True:
    @dp.message_handler(text="🍴 Меню")
    @dp.message_handler(text="🍴 Menyu")
    async def menu_handler(message: types.Message):
        lang = await get_lang(message.from_user.id)
        btn = await location_reply(lang)
        await message.answer(text["location"][lang], reply_markup=btn)
        await MenuStates.location.set()
    @dp.message_handler(text="⬅️ Назад", state=MenuStates.location)
    @dp.message_handler(text="⬅️ Ortga", state=MenuStates.location)
    async def menuBack_handler(message: types.Message, state: FSMContext):
        lang = await get_lang(message.from_user.id)
        btn = await start_reply(lang)
        await message.answer(text["start"][lang], reply_markup=btn)
        await state.finish()
    @dp.message_handler(text="🗺 Мои адреса", state=MenuStates.location)
    @dp.message_handler(text="🗺 Mening manzillarim", state=MenuStates.location)
    async def menuMyAdresses_handler(message: types.Message, state: FSMContext):
        locations = await select_locations(message.from_user.id)
        lang = await get_lang(message.from_user.id)
        if not locations:
            await message.answer(text["myAdressesNone"][lang])
        else:
            btn = await adresses_reply(locations, lang)
            await message.answer(text["myAdressesChoose"][lang], reply_markup=btn)
            await MenuStates.locationText.set()
    @dp.message_handler(text="⬅️ Назад", state=MenuStates.locationText)
    @dp.message_handler(text="⬅️ Ortga", state=MenuStates.locationText)
    async def menuMyAdressesBack_handler(message: types.Message, state: FSMContext):
        lang = await get_lang(message.from_user.id)
        btn = await location_reply(lang)
        await message.answer(text["location"][lang], reply_markup=btn)
        await MenuStates.location.set()
    @dp.message_handler(state=MenuStates.locationText)
    async def menuMyAdress_handler(message: types.Message, state: FSMContext):
        addresses = await select_locations(message.from_user.id)
        lang = await get_lang(message.from_user.id)
        for i in range(len(addresses)):
            addresses[i] = addresses[i][0]
        if message.text in addresses:
            btn = await categories_reply(await select_categories(lang), lang)
            await message.answer(text["chooseCategory"][lang], reply_markup=btn)
            await state.update_data(location=message.text)
            await MenuStates.category.set()
        else:
            await message.answer(text["addressNotFound"][lang])
    @dp.message_handler(content_types=["location"], state=MenuStates.location)
    async def menuLocation_handler(message: types.Message, state: FSMContext):
        lang = await get_lang(message.from_user.id)
        latitude = message.location.latitude
        longitude = message.location.longitude
        address = get_address(latitude, longitude)
        address = address.replace("`", "")
        address = address.replace("'", "")
        address = address.split(", Toshkent, ")[0]
        btn = await locationYesNo_reply(lang)
        await message.answer(f"{text['locationYesNo'][lang]} {address} {text['locationYesNo2'][lang]}", reply_markup=btn)
        await state.update_data(location=address)
        await MenuStates.yesNo.set()
    @dp.message_handler(text="⬅️ Назад", state=MenuStates.yesNo)
    @dp.message_handler(text="⬅️ Ortga", state=MenuStates.yesNo)
    async def menuLocationBack_handler(message: types.Message, state: FSMContext):
        lang = await get_lang(message.from_user.id)
        btn = await location_reply(lang)
        await message.answer(text["location"][lang], reply_markup=btn)
        await MenuStates.location.set()
    @dp.message_handler(text="❌ Нет", state=MenuStates.yesNo)
    @dp.message_handler(text="❌ Yo'q", state=MenuStates.yesNo)
    async def menuLocationNo_handler(message: types.Message, state: FSMContext):
        lang = await get_lang(message.from_user.id)
        btn = await location_reply(lang)
        await message.answer(text["location"][lang], reply_markup=btn)
        await MenuStates.location.set()
    @dp.message_handler(text="✅ Да", state=MenuStates.yesNo)
    @dp.message_handler(text="✅ Ha", state=MenuStates.yesNo)
    async def menuLocationYes_handler(message: types.Message, state: FSMContext):
        lang = await get_lang(message.from_user.id)
        btn = await categories_reply(await select_categories(lang), lang)
        await message.answer(text["chooseCategory"][lang], reply_markup=btn)
        data = await state.get_data()
        await insert_location(message.from_user.id, data['location'])
        await MenuStates.category.set()
    @dp.message_handler(text="⬅️ Назад", state=MenuStates.category)
    @dp.message_handler(text="⬅️ Ortga", state=MenuStates.category)
    async def productsMenuBack_handler(message: types.Message, state: FSMContext):
        lang = await get_lang(message.from_user.id)
        btn = await location_reply(lang)
        await message.answer(text["location"][lang], reply_markup=btn)
        await MenuStates.location.set()
    emoji = {
        1: "1️⃣",
        2: "2️⃣",
        3: "3️⃣",
        4: "4️⃣",
        5: "5️⃣",
        6: "6️⃣",
        7: "7️⃣",
        8: "8️⃣",
        9: "9️⃣",
        0: "0️⃣",
    }
    @dp.message_handler(text="📥 Корзина", state=MenuStates.category)
    @dp.message_handler(text="📥 Savat", state=MenuStates.category)
    async def productsBasket_handler(message: types.Message, state: FSMContext):
        basket = await select_basket(message.from_user.id)
        lang = await get_lang(message.from_user.id)
        btn = await categories_reply(await select_categories(lang), lang)
        await message.answer(text["chooseCategory"][lang], reply_markup=btn)
        if basket == "none":
            await message.answer(text["emptyBasket"][lang])
        else:
            products = basket[2]
            products = products.split("; ")
            unique_products = []
            for i in products:
                if i not in unique_products:
                    unique_products.append(i)
            products_text = ""
            quantity_text = 0
            for i in unique_products:
                if i != "":
                    quantity_text = products.count(i)
                    count_str = str(quantity_text)
                    emoji_str = ""
                    for digit in count_str:
                        emoji_str += emoji[int(digit)]
                    products_text += f"{emoji_str} ✖️ {i}\n"
            current_price = basket[3]
            current_price = current_price.replace(" ", "")
            current_price = int(current_price)
            current_price = current_price + 10000
            str_num = str(current_price)
            formatted_price = ' '.join([str_num[:-3], str_num[-3:]])
            btn = await basket_inline(lang, unique_products)
            await message.answer(f"{text['basket'][lang]}\n{products_text}{text['basketPrice1'][lang]} {basket[3]} {text['price2'][lang]}\n{text['basketPrice2'][lang]} 10 000 {text['price2'][lang]}\n{text['basketPrice3'][lang]} {formatted_price} {text['price2'][lang]}", reply_markup=btn)
    @dp.callback_query_handler(text_contains="delete:", state=MenuStates.category)
    @dp.callback_query_handler(text_contains="delete:", state=MenuStates.product)
    @dp.callback_query_handler(text_contains="delete:", state=MenuStates.price)
    async def productsDelete_query(call: types.CallbackQuery, state: FSMContext):
        lang = await get_lang(call.from_user.id)
        product_name = call.data.split(":")[1]
        await delete_from_basket(call.from_user.id, product_name, lang)
        basket = await select_basket(call.from_user.id)
        if basket == "none":
            await call.message.edit_text(text["emptyBasket"][lang])
        else:
            products = basket[2]
            products = products.split("; ")
            unique_products = []
            for i in products:
                if i not in unique_products:
                    unique_products.append(i)
            products_text = ""
            quantity_text = 0
            for i in unique_products:
                if i != "":
                    quantity_text = products.count(i)
                    count_str = str(quantity_text)
                    emoji_str = ""
                    for digit in count_str:
                        emoji_str += emoji[int(digit)]
                    products_text += f"{emoji_str} ✖️ {i}\n"
            current_price = basket[3]
            current_price = current_price.replace(" ", "")
            current_price = int(current_price)
            current_price = current_price + 10000
            str_num = str(current_price)
            formatted_price = ' '.join([str_num[:-3], str_num[-3:]])
            btn = await basket_inline(lang, unique_products)
            await call.message.edit_text(f"{text['basket'][lang]}\n{products_text}{text['basketPrice1'][lang]} {basket[3]} {text['price2'][lang]}\n{text['basketPrice2'][lang]} 10 000 {text['price2'][lang]}\n{text['basketPrice3'][lang]} {formatted_price} {text['price2'][lang]}", reply_markup=btn)
    @dp.message_handler(state=MenuStates.category)
    async def products_handler(message: types.Message, state: FSMContext):
        try:
            lang = await get_lang(message.from_user.id)
            await state.update_data(category=message.text)
            category = await get_category(message.text, lang)
            btn = await products_reply(await get_product(category[0], lang), lang)
            if lang == 0:
                photo = category[3]
            else:
                photo = category[4]
            await message.answer_photo(photo, reply_markup=btn)
            await MenuStates.product.set()
        except TypeError:
            pass
    @dp.message_handler(text="⬅️ Назад", state=MenuStates.product)
    @dp.message_handler(text="⬅️ Ortga", state=MenuStates.product)
    async def productsBack_handler(message: types.Message, state: FSMContext):
        lang = await get_lang(message.from_user.id)
        btn = await categories_reply(await select_categories(lang), lang)
        await message.answer(text["chooseCategory"][lang], reply_markup=btn)
        await MenuStates.category.set()
    @dp.message_handler(text="📥 Корзина", state=MenuStates.product)
    @dp.message_handler(text="📥 Savat", state=MenuStates.product)
    async def productsBasket2_handler(message: types.Message, state: FSMContext):
        basket = await select_basket(message.from_user.id)
        lang = await get_lang(message.from_user.id)
        btn = await categories_reply(await select_categories(lang), lang)
        await message.answer(text["chooseCategory"][lang], reply_markup=btn)
        if basket == "none":
            await message.answer(text["emptyBasket"][lang])
        else:
            products = basket[2]
            products = products.split("; ")
            unique_products = []
            for i in products:
                if i not in unique_products:
                    unique_products.append(i)
            products_text = ""
            quantity_text = 0
            for i in unique_products:
                if i != "":
                    quantity_text = products.count(i)
                    count_str = str(quantity_text)
                    emoji_str = ""
                    for digit in count_str:
                        emoji_str += emoji[int(digit)]
                    products_text += f"{emoji_str} ✖️ {i}\n"
            current_price = basket[3]
            current_price = current_price.replace(" ", "")
            current_price = int(current_price)
            current_price = current_price + 10000
            str_num = str(current_price)
            formatted_price = ' '.join([str_num[:-3], str_num[-3:]])
            btn = await basket_inline(lang, unique_products)
            await message.answer(f"{text['basket'][lang]}\n{products_text}{text['basketPrice1'][lang]} {basket[3]} {text['price2'][lang]}\n{text['basketPrice2'][lang]} 10 000 {text['price2'][lang]}\n{text['basketPrice3'][lang]} {formatted_price} {text['price2'][lang]}", reply_markup=btn)
        await MenuStates.category.set()
    @dp.message_handler(state=MenuStates.product)
    async def productsProduct_handler(message: types.Message, state: FSMContext):
        try:
            lang = await get_lang(message.from_user.id)
            product = await get_product_info(message.text, lang) 
            if product[3] != "none":
                btn = await size_reply(lang)
                await message.answer(text["start"][lang], reply_markup=btn)
                btn = await size_inline(product[3], product[4], product[0], lang)
                if lang == 0:
                    about = product[5]
                else:
                    about = product[6]
                if about == "none":
                    about = ""
                await message.answer_photo(product[8], caption=about, reply_markup=btn)
            else:
                await state.update_data(size="none")
                btn = await size_reply(lang)
                await message.answer(text["start"][lang], reply_markup=btn)
                await state.update_data(quantity=1)
                await state.update_data(price=product[4])
                if lang == 0:
                    about = product[5]
                else:
                    about = product[6]
                if about == "none":
                    about = ""
                btn = await quantity_inline(1, product[0], lang)
                await message.answer_photo(product[8], caption=f"{about}\n{text['price'][lang]} {product[4]} {text['price2'][lang]}", reply_markup=btn)
            await MenuStates.price.set()
        except TypeError:
            pass
    @dp.message_handler(text="⬅️ Назад", state=MenuStates.price)
    @dp.message_handler(text="⬅️ Ortga", state=MenuStates.price)
    async def productsProductBack_handler(message: types.Message, state: FSMContext):
        try:
            lang = await get_lang(message.from_user.id)
            data = await state.get_data()
            category = await get_category(data["category"], lang)
            btn = await products_reply(await get_product(category[0], lang), lang)
            if lang == 0:
                photo = category[3]
            else:
                photo = category[4]
            await message.answer_photo(photo, reply_markup=btn)
            await MenuStates.product.set()
        except Exception as e:
            print(e)
    @dp.message_handler(text="📥 Корзина", state=MenuStates.price)
    @dp.message_handler(text="📥 Savat", state=MenuStates.price)
    async def productsBasket2_handler(message: types.Message, state: FSMContext):
        basket = await select_basket(message.from_user.id)
        lang = await get_lang(message.from_user.id)
        btn = await categories_reply(await select_categories(lang), lang)
        await message.answer(text["chooseCategory"][lang], reply_markup=btn)
        if basket == "none":
            await message.answer(text["emptyBasket"][lang])
        else:
            products = basket[2]
            products = products.split("; ")
            unique_products = []
            for i in products:
                if i not in unique_products:
                    unique_products.append(i)
            products_text = ""
            quantity_text = 0
            for i in unique_products:
                if i != "":
                    quantity_text = products.count(i)
                    count_str = str(quantity_text)
                    emoji_str = ""
                    for digit in count_str:
                        emoji_str += emoji[int(digit)]
                    products_text += f"{emoji_str} ✖️ {i}\n"
            current_price = basket[3]
            current_price = current_price.replace(" ", "")
            current_price = int(current_price)
            current_price = current_price + 10000
            str_num = str(current_price)
            formatted_price = ' '.join([str_num[:-3], str_num[-3:]])
            btn = await basket_inline(lang, unique_products)
            await message.answer(f"{text['basket'][lang]}\n{products_text}{text['basketPrice1'][lang]} {basket[3]} {text['price2'][lang]}\n{text['basketPrice2'][lang]} 10 000 {text['price2'][lang]}\n{text['basketPrice3'][lang]} {formatted_price} {text['price2'][lang]}", reply_markup=btn)
        await MenuStates.category.set()
    @dp.callback_query_handler(text_contains="max_price:", state=MenuStates.price)
    async def produtsProductQuantityMax(call: types.CallbackQuery, state: FSMContext):
        lang = await get_lang(call.from_user.id)
        id = call.data.split(":")[1]
        price = await get_product_by_id("max", id)
        await state.update_data(price=price[0])
        await state.update_data(quantity=1)
        btn = await quantity_inline(1, id, lang)
        await call.message.edit_reply_markup(btn)
        await state.update_data(size="max")
    @dp.callback_query_handler(text_contains="min_price:", state=MenuStates.price)
    async def produtsProductQuantityMin(call: types.CallbackQuery, state: FSMContext):
        lang = await get_lang(call.from_user.id)
        id = call.data.split(":")[1]
        price = await get_product_by_id("min", id)
        await state.update_data(price=price[0])
        await state.update_data(quantity=1)
        btn = await quantity_inline(1, id, lang)
        await call.message.edit_reply_markup(btn)
        await state.update_data(size="min")
    @dp.callback_query_handler(text_contains="quantity:", state=MenuStates.price)
    async def produtsProductQuantityMin(call: types.CallbackQuery, state: FSMContext):
        lang = await get_lang(call.from_user.id)
        action = call.data.split(":")
        if action[1] == "minus":
            data = await state.get_data()
            await call.answer()
            if data["quantity"] > 1:
                await state.update_data(quantity=data["quantity"]-1)
                data = await state.get_data()
                btn = await quantity_inline(data["quantity"], action[2], lang)
                await call.message.edit_reply_markup(btn)
        elif action[1] == "plus":
            data = await state.get_data()
            await state.update_data(quantity=data["quantity"]+1)
            data = await state.get_data()
            btn = await quantity_inline(data["quantity"], action[2], lang)
            await call.message.edit_reply_markup(btn)
    @dp.callback_query_handler(text_contains="add_to_cart:", state=MenuStates.price)
    async def addToCart_inline(call: types.CallbackQuery, state: FSMContext):
        id = call.data.split(':')[1]
        user_id = call.from_user.id
        lang = await get_lang(user_id)
        await call.answer("Товар добавлен")
        data = await state.get_data()
        category = await get_category(data["category"], lang)
        btn = await products_reply2(await get_product(category[0], lang), lang)
        await call.message.delete()
        if lang == 0:
            photo = category[3]
        else:
            photo = category[4]
        await call.message.answer_photo(photo, reply_markup=btn)
        await MenuStates.product.set()
        product = await select_by_id(id)
        if lang == 0:
            if data["size"] == "max":
                product_name = product[1] + " биг"
            elif data["size"] == "min":
                product_name = product[1] + " мини"
            else:
                product_name = product[1]
        elif lang == 1:
            if data["size"] == "max":
                product_name = product[2] + " big"
            elif data["size"] == "min":
                product_name = product[2] + " mini"
            else:
                product_name = product[2]
        result_produtcs = ""
        if data["quantity"] > 1:
            for i in range(data["quantity"]):
                result_produtcs += product_name + "; "
            current_price = data["price"].replace(" ", "")
            current_price = int(current_price)
            price = current_price * data["quantity"]
        else:
            result_produtcs = product_name + "; "
            price = data["price"]
        await insert_basket(user_id, result_produtcs, price)
    @dp.callback_query_handler(text="clear_basket", state=MenuStates.category)
    async def cartClear_inline(call: types.CallbackQuery, state: FSMContext):
        await call.message.edit_text(text["emptyBasket"][await get_lang(call.from_user.id)])
        await clear_basket(call.from_user.id)
    @dp.callback_query_handler(text="basket_back", state=MenuStates.category)
    async def cartBack_inline(call: types.CallbackQuery, state: FSMContext):
        await call.message.delete()
        await call.message.answer(text["chooseCategory"][await get_lang(call.from_user.id)])
    @dp.callback_query_handler(text="select_time", state=MenuStates.category)
    async def cartTime_inline(call: types.CallbackQuery, state: FSMContext):
        lang = await get_lang(call.from_user.id)
        btn, last_time = await time_inline(lang)
        await state.update_data(last_time=last_time)
        await call.message.edit_reply_markup(btn)
    @dp.callback_query_handler(text="time_next", state=MenuStates.category)
    async def cartTimeNext_inline(call: types.CallbackQuery, state: FSMContext):
        lang = await get_lang(call.from_user.id)
        data = await state.get_data()
        last_time = data["last_time"]
        btn, last_time = await time_inline_next(lang, last_time)
        await state.update_data(last_time=last_time)
        if btn != "none":
            await call.message.edit_reply_markup(btn)
        else:
            await call.answer()
    @dp.callback_query_handler(text_contains="time_", state=MenuStates.category)
    async def cartTimeSelected_inline(call: types.CallbackQuery, state: FSMContext):
        await state.update_data(time=call.data.split("_")[1])
        await cartTimeBack_inline(call, state)
    @dp.callback_query_handler(text="time_back", state=MenuStates.category)
    async def cartTimeBack_inline(call: types.CallbackQuery, state: FSMContext):
        basket = await select_basket(call.from_user.id)
        lang = await get_lang(call.from_user.id)
        if basket == "none":
            await call.message.edit_text(text["emptyBasket"][lang])
        else:
            products = basket[2]
            products = products.split("; ")
            unique_products = []
            for i in products:
                if i not in unique_products:
                    unique_products.append(i)
            products_text = ""
            quantity_text = 0
            for i in unique_products:
                if i != "":
                    quantity_text = products.count(i)
                    count_str = str(quantity_text)
                    emoji_str = ""
                    for digit in count_str:
                        emoji_str += emoji[int(digit)]
                    products_text += f"{emoji_str} ✖️ {i}\n"
            current_price = basket[3]
            current_price = current_price.replace(" ", "")
            current_price = int(current_price)
            current_price = current_price + 10000
            str_num = str(current_price)
            formatted_price = ' '.join([str_num[:-3], str_num[-3:]])
            btn = await basket_inline(lang, unique_products)
            await call.message.edit_text(f"{text['basket'][lang]}\n{products_text}{text['basketPrice1'][lang]} {basket[3]} {text['price2'][lang]}\n{text['basketPrice2'][lang]} 10 000 {text['price2'][lang]}\n{text['basketPrice3'][lang]} {formatted_price} {text['price2'][lang]}", reply_markup=btn)
    @dp.callback_query_handler(text="make_order", state=MenuStates.category)
    async def cartOrder_inline(call: types.CallbackQuery, state: FSMContext):
        lang = await get_lang(call.from_user.id)
        await call.answer()
        btn = await phone_inline(lang)
        await call.message.answer(text["phone"][lang], reply_markup=btn)
        await MenuStates.phone.set()
    @dp.message_handler(text="⬅️ Назад", state=MenuStates.phone)
    @dp.message_handler(text="⬅️ Ortga", state=MenuStates.phone)
    async def cartOrderBack_inline(message: types.Message, state: FSMContext):
        basket = await select_basket(message.from_user.id)
        lang = await get_lang(message.from_user.id)
        btn = await categories_reply(await select_categories(lang), lang)
        await message.answer(text["chooseCategory"][lang], reply_markup=btn)
        if basket == "none":
            await message.answer(text["emptyBasket"][lang])
        else:
            products = basket[2]
            products = products.split("; ")
            unique_products = []
            for i in products:
                if i not in unique_products:
                    unique_products.append(i)
            products_text = ""
            quantity_text = 0
            for i in unique_products:
                if i != "":
                    quantity_text = products.count(i)
                    count_str = str(quantity_text)
                    emoji_str = ""
                    for digit in count_str:
                        emoji_str += emoji[int(digit)]
                    products_text += f"{emoji_str} ✖️ {i}\n"
            current_price = basket[3]
            current_price = current_price.replace(" ", "")
            current_price = int(current_price)
            current_price = current_price + 10000
            str_num = str(current_price)
            formatted_price = ' '.join([str_num[:-3], str_num[-3:]])
            btn = await basket_inline(lang, unique_products)
            await message.answer(f"{text['basket'][lang]}\n{products_text}{text['basketPrice1'][lang]} {basket[3]} {text['price2'][lang]}\n{text['basketPrice2'][lang]} 10 000 {text['price2'][lang]}\n{text['basketPrice3'][lang]} {formatted_price} {text['price2'][lang]}", reply_markup=btn)
        await MenuStates.category.set()
    @dp.message_handler(content_types=["contact"], state=MenuStates.phone)
    async def cartOrderPhone_inline(message: types.Message, state: FSMContext):
        lang = await get_lang(message.from_user.id)
        await state.update_data(phone=message.contact.phone_number)
        btn = await payType_inline(lang)
        await message.answer(text["payingType"][lang], reply_markup=btn)
        await MenuStates.payType.set()
    @dp.message_handler(state=MenuStates.phone)
    async def cartOrderPhone2_inline(message: types.Message, state: FSMContext):
        lang = await get_lang(message.from_user.id)
        if len(message.text) == 17 and message.text[0] == "+" and message.text[1] == "9" and message.text[2] == "9" and message.text[3] == "8" and message.text[4] == " " and message.text[7] == " " and message.text[11] == " " and message.text[14] == " ":
            await state.update_data(phone=message.text)
            btn = await payType_inline(lang)
            await message.answer(text["payingType"][lang], reply_markup=btn)
            await MenuStates.payType.set()
        else:
            await message.answer(text["phoneErr"][lang])
    @dp.message_handler(text="⬅️ Назад", state=MenuStates.payType)
    @dp.message_handler(text="⬅️ Ortga", state=MenuStates.payType)
    async def cartOrderPhoneBack_inline(message: types.Message, state: FSMContext):
        lang = await get_lang(message.from_user.id)
        btn = await phone_inline(lang)
        await message.answer(text["phone"][lang], reply_markup=btn)
        await MenuStates.phone.set()
    @dp.message_handler(state=MenuStates.payType)
    async def cartOrderPayType_inline(message: types.Message, state: FSMContext):
        if message.text == "Наличные" or message.text == "Naqd pul":
            await state.update_data(payType=message.text)
            data = await state.get_data()
            basket = await select_basket(message.from_user.id)
            lang = await get_lang(message.from_user.id)
            if basket == "none":
                await message.answer(text["emptyBasket"][lang])
            else:
                products = basket[2]
                products = products.split("; ")
                unique_products = []
                for i in products:
                    if i not in unique_products:
                        unique_products.append(i)
                products_text = ""
                quantity_text = 0
                for i in unique_products:
                    if i != "":
                        quantity_text = products.count(i)
                        count_str = str(quantity_text)
                        emoji_str = ""
                        for digit in count_str:
                            emoji_str += emoji[int(digit)]
                        products_text += f"{emoji_str} ✖️ {i}\n"
                current_price = basket[3]
                current_price = current_price.replace(" ", "")
                current_price = int(current_price)
                current_price = current_price + 10000
                str_num = str(current_price)
                formatted_price = ' '.join([str_num[:-3], str_num[-3:]])
                btn = await order_reply(lang)
                await message.answer(f"{text['order1'][lang]}{data['location']}\n\n{products_text}\n{text['order2'][lang]}{message.text}\n\n<b>{text['basketPrice1'][lang]}</b> {basket[3]} {text['price2'][lang]}\n<b>{text['basketPrice2'][lang]}</b> 10 000 {text['price2'][lang]}\n<b>{text['basketPrice3'][lang]}</b> {formatted_price} {text['price2'][lang]}", reply_markup=btn)
                await MenuStates.order.set()
        elif message.text == "Click":
            await state.update_data(payType=message.text)
            data = await state.get_data()
            basket = await select_basket(message.from_user.id)
            lang = await get_lang(message.from_user.id)
            if basket == "none":
                await message.answer(text["emptyBasket"][lang])
            else:
                products = basket[2]
                products = products.split("; ")
                unique_products = []
                for i in products:
                    if i not in unique_products:
                        unique_products.append(i)
                products_text = ""
                quantity_text = 0
                for i in unique_products:
                    if i != "":
                        quantity_text = products.count(i)
                        count_str = str(quantity_text)
                        emoji_str = ""
                        for digit in count_str:
                            emoji_str += emoji[int(digit)]
                        products_text += f"{emoji_str} ✖️ {i}\n"
                current_price = basket[3]
                current_price = current_price.replace(" ", "")
                current_price = int(current_price)
                current_price = current_price + 10000
                str_num = str(current_price)
                formatted_price = ' '.join([str_num[:-3], str_num[-3:]])
                btn = await order_reply(lang)
                await message.answer(f"{text['order1'][lang]}{data['location']}\n\n{products_text}\n{text['order2'][lang]}{message.text}\n\n<b>{text['basketPrice1'][lang]}</b> {basket[3]} {text['price2'][lang]}\n<b>{text['basketPrice2'][lang]}</b> 10 000 {text['price2'][lang]}\n<b>{text['basketPrice3'][lang]}</b> {formatted_price} {text['price2'][lang]}", reply_markup=btn)
                await MenuStates.order.set()
        elif message.text == "Payme":
            await state.update_data(payType=message.text)
            data = await state.get_data()
            basket = await select_basket(message.from_user.id)
            lang = await get_lang(message.from_user.id)
            if basket == "none":
                await message.answer(text["emptyBasket"][lang])
            else:
                products = basket[2]
                products = products.split("; ")
                unique_products = []
                for i in products:
                    if i not in unique_products:
                        unique_products.append(i)
                products_text = ""
                quantity_text = 0
                for i in unique_products:
                    if i != "":
                        quantity_text = products.count(i)
                        count_str = str(quantity_text)
                        emoji_str = ""
                        for digit in count_str:
                            emoji_str += emoji[int(digit)]
                        products_text += f"{emoji_str} ✖️ {i}\n"
                current_price = basket[3]
                current_price = current_price.replace(" ", "")
                current_price = int(current_price)
                current_price = current_price + 10000
                str_num = str(current_price)
                formatted_price = ' '.join([str_num[:-3], str_num[-3:]])
                btn = await order_reply(lang)
                await message.answer(f"{text['order1'][lang]}{data['location']}\n\n{products_text}\n{text['order2'][lang]}{message.text}\n\n<b>{text['basketPrice1'][lang]}</b> {basket[3]} {text['price2'][lang]}\n<b>{text['basketPrice2'][lang]}</b> 10 000 {text['price2'][lang]}\n<b>{text['basketPrice3'][lang]}</b> {formatted_price} {text['price2'][lang]}", reply_markup=btn)
                await MenuStates.order.set()
    @dp.message_handler(text="❌ Отменить", state=MenuStates.order)
    @dp.message_handler(text="❌ Bekor qilish", state=MenuStates.order)
    async def cartOrderPayTypeOrder1_inline(message: types.Message, state: FSMContext):
        lang = await get_lang(message.from_user.id)
        await clear_basket(message.from_user.id)
        btn = await start_reply(lang)
        await message.answer(text["chooseCategory"][lang], reply_markup=btn)
        await state.finish()
    @dp.message_handler(text="✅ Подтвердить", state=MenuStates.order)
    @dp.message_handler(text="✅ Tasdiqlash", state=MenuStates.order)
    async def cartOrderPayTypeOrder2_inline(message: types.Message, state: FSMContext):
        lang = await get_lang(message.from_user.id)
        data = await state.get_data()
        basket = await select_basket(message.from_user.id)
        try:
            time = data["time"]
        except KeyError:
            time = ""
        order = await insert_order("new", data['location'], basket[2], data['payType'], basket[3], datetime.datetime.now(), data['phone'], message.from_user.id, time)
        await clear_basket(message.from_user.id)
        products = basket[2]
        products = products.split("; ")
        unique_products = []
        for i in products:
            if i not in unique_products:
                unique_products.append(i)
        products_text = ""
        quantity_text = 0
        for i in unique_products:
            if i != "":
                quantity_text = products.count(i)
                count_str = str(quantity_text)
                emoji_str = ""
                for digit in count_str:
                    emoji_str += emoji[int(digit)]
                products_text += f"{emoji_str} ✖️ {i}\n"
        current_price = basket[3]
        current_price = current_price.replace(" ", "")
        current_price = int(current_price)
        current_price = current_price + 10000
        str_num = str(current_price)
        formatted_price = ' '.join([str_num[:-3], str_num[-3:]])
        btn = await start_reply(lang)
        await message.answer(f"{text['order_id'][lang]}{order[0]}\n{text['status2'][lang]}{order[1]}\n{text['addres'][lang]}{order[2]}\n\n{products_text}\n{text['order2'][lang]}{order[4]}\n\n<b>{text['basketPrice1'][lang]}</b> {order[5]} {text['price2'][lang]}\n<b>{text['basketPrice2'][lang]}</b> 10 000 {text['price2'][lang]}\n<b>{text['basketPrice3'][lang]}</b> {formatted_price} {text['price2'][lang]}", reply_markup=btn)
        await state.finish()

# Админ панель
@dp.message_handler(commands=["admin"], state="*")
async def admin_command(message: types.Message, state: FSMContext):
    if await select_admins(message.from_user.id) != None:
        await state.finish()
        lang = await get_lang(message.from_user.id)
        btn = await admin_inline(lang)
        await message.answer(text["action"][lang], reply_markup=btn)
@dp.callback_query_handler(text="back_admin")
async def adminSeeOrdersBack(call: types.CallbackQuery):
    lang = await get_lang(call.from_user.id)
    btn = await admin_inline(lang)
    await call.message.edit_text(text["action"][lang], reply_markup=btn)
@dp.callback_query_handler(text="see_orders")
async def adminSeeOrders(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(call.from_user.id)
    await state.update_data(page=1)
    data = await state.get_data()
    orders = await select_all_orders()
    btn = await adminOrders_inline(lang, orders, 1)
    await call.message.edit_text(text["selectOrders"][lang], reply_markup=btn)
@dp.callback_query_handler(text="next")
async def adminSeeOrdersNext(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    updated_page = data["page"]+1
    await state.update_data(page=updated_page)
    lang = await get_lang(call.from_user.id)
    orders = await select_all_orders()
    btn = await adminOrders_inline(lang, orders, updated_page)
    if btn != None:
        await call.message.edit_reply_markup(btn)
    else:
        await state.update_data(page=data["page"])
        await call.answer()
@dp.callback_query_handler(text="update")
async def adminSeeOrdersUpdate(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(call.from_user.id)
    data = await state.get_data()
    orders = await select_all_orders()
    btn = await adminOrders_inline(lang, orders, data["page"])
    try:
        btn.inline_keyboard[2][0]["text"] += " "
    except AttributeError:
        await state.update_data(page=data["page"]-1)
        btn = await adminOrders_inline(lang, orders, data["page"]-1)
        btn.inline_keyboard[2][0]["text"] += " "
    await call.message.edit_reply_markup(btn)
    btn.inline_keyboard[2][0]["text"] = btn.inline_keyboard[2][0]["text"][:-1]
    await call.message.edit_reply_markup(btn)
@dp.callback_query_handler(text="prev")
async def adminSeeOrdersPrev(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data["page"] > 1:
        updated_page = data["page"]-1
        await state.update_data(page=updated_page)
        lang = await get_lang(call.from_user.id)
        orders = await select_all_orders()
        btn = await adminOrders_inline(lang, orders, updated_page)
        await call.message.edit_reply_markup(btn)
    else:
        await call.answer()
@dp.callback_query_handler(text="category")
async def adminSeeAddCategory2(call: types.CallbackQuery):
    lang = await get_lang(call.from_user.id)
    btn = await adminCategory_inline(lang)
    await call.message.edit_text(text["action"][lang], reply_markup=btn)
@dp.callback_query_handler(text="category_back")
@dp.callback_query_handler(text="category_back", state=AdminStates.category_ru)
@dp.callback_query_handler(text="category_back", state=AdminStates.category_uz)
async def adminSeeAddCategory2Back(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    lang = await get_lang(call.from_user.id)
    btn = await adminCategory_inline(lang)
    await call.message.edit_text(text["action"][lang], reply_markup=btn)
@dp.callback_query_handler(text="add_category")
async def adminSeeAddCategory(call: types.CallbackQuery):
    lang = await get_lang(call.from_user.id)
    btn = await adminBack_inline(lang)
    await call.message.edit_text(text["addCategory1"][lang], reply_markup=btn)
    await AdminStates.category_ru.set()
@dp.callback_query_handler(text="delete_category")
async def adminSeeDeleteCategory(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(call.from_user.id)
    categories = await select_all_categories()
    await state.update_data(category_page=1)
    btn = await deleteCategory_inline(lang, categories, 1)
    await call.message.edit_text(text["action"][lang], reply_markup=btn)
@dp.callback_query_handler(text="category_next")
async def adminSeeCategoriesNext(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    updated_page = data["category_page"]+1
    await state.update_data(category_page=updated_page)
    lang = await get_lang(call.from_user.id)
    categories = await select_all_categories()
    btn = await deleteCategory_inline(lang, categories, updated_page)
    if btn != None:
        await call.message.edit_reply_markup(btn)
    else:
        await state.update_data(category_page=data["category_page"])
        await call.answer()
@dp.callback_query_handler(text="category_prev")
async def adminSeeCategoriesPrev(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data["category_page"] > 1:
        updated_page = data["category_page"]-1
        await state.update_data(category_page=updated_page)
        lang = await get_lang(call.from_user.id)
        categories = await select_all_categories()
        btn = await deleteCategory_inline(lang, categories, updated_page)
        await call.message.edit_reply_markup(btn)
    else:
        await call.answer()
@dp.callback_query_handler(text_contains="delete_category:")
async def adminSeeCategoriesDelete(call: types.CallbackQuery, state: FSMContext):
    id = call.data.split(":")[1]
    await delete_category(id)
    lang = await get_lang(call.from_user.id)
    categories = await select_all_categories()
    data = await state.get_data()
    btn = await deleteCategory_inline(lang, categories, data["category_page"])
    if btn != None:
        await call.message.edit_reply_markup(btn)
    else:
        while True:
            data = await state.get_data()
            btn = await deleteCategory_inline(lang, categories, data["category_page"])
            if btn == None:
                await state.update_data(category_page=data["category_page"]-1)
                data = await state.get_data()
                btn = await deleteCategory_inline(lang, categories, data["category_page"])
                await call.message.edit_reply_markup(btn)
            else:
                break
@dp.message_handler(state=AdminStates.category_ru)
async def adminSeeAddCategoryRu(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    btn = await adminBack_inline(lang)
    await message.answer(text["addCategory2"][lang], reply_markup=btn)
    await state.update_data(category_ru=message.text)
    await AdminStates.category_uz.set()
@dp.message_handler(state=AdminStates.category_uz)
async def adminSeeAddCategoryUz(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    btn = await adminBack_inline(lang)
    await message.answer(text["addCategory3"][lang], reply_markup=btn)
    await state.update_data(category_uz=message.text)
    await AdminStates.category_photo.set()
@dp.message_handler(state=AdminStates.category_photo, content_types=["photo"])
async def adminSeeAddCategoryPhoto(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    btn = await adminBack_inline(lang)
    await message.answer(text["addCategory4"][lang], reply_markup=btn)
    await state.update_data(category_photo=message.photo[0]["file_id"])
    await AdminStates.category_photo_uz.set()
@dp.message_handler(state=AdminStates.category_photo_uz, content_types=["photo"])
async def adminSeeAddCategoryPhotoUz(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    await state.update_data(category_photo_uz=message.photo[0]["file_id"])
    data = await state.get_data()
    await insert_category(data["category_ru"], data["category_uz"], data["category_photo"], data["category_photo_uz"])
    await message.answer(text["done"][lang])
    btn = await adminCategory_inline(lang)
    await message.answer(text["action"][lang], reply_markup=btn)
    await state.finish()
@dp.callback_query_handler(text="back_orders")
async def adminSeeOrderBack(call: types.CallbackQuery, state: FSMContext):
    await adminSeeOrders(call, state)
@dp.callback_query_handler(text_contains="order_")
async def adminSeeOrder(call: types.CallbackQuery):
    lang = await get_lang(call.from_user.id)
    orders = await select_order_by_id(call.data.split("_")[1])
    products = orders[3]
    products = products.split("; ")
    unique_products = []
    for j in products:
        if j not in unique_products:
            unique_products.append(j)
    products_text = ""
    quantity_text = 0
    for g in unique_products:
        if g != "":
            quantity_text = products.count(g)
            count_str = str(quantity_text)
            emoji_str = ""
            for digit in count_str:
                emoji_str += emoji[int(digit)]
            products_text += f"{emoji_str} ✖️ {g}\n"
    current_price = orders[5]
    current_price = current_price.replace(" ", "")
    current_price = int(current_price)
    current_price = current_price + 10000
    str_num = str(current_price)
    formatted_price = ' '.join([str_num[:-3], str_num[-3:]])
    order_time = orders[9]
    if order_time == "":
        order_time = text["fast"][lang]
    btn = await adminOrder_inline(lang, call.data.split("_")[1])
    await call.message.edit_text(f"{text['order_id'][lang]}{orders[0]}\n{text['status2'][lang]}{text[orders[1]][lang]}\n{text['addres'][lang]}{orders[2]}\n{text['time'][lang]}{order_time}\n\n{products_text}\n{text['order2'][lang]}{orders[4]}\n\n<b>{text['basketPrice1'][lang]}</b> {orders[5]} {text['price2'][lang]}\n<b>{text['basketPrice2'][lang]}</b> 10 000 {text['price2'][lang]}\n<b>{text['basketPrice3'][lang]}</b> {formatted_price} {text['price2'][lang]}", reply_markup=btn)
@dp.callback_query_handler(text_contains="delivered_")
async def adminSeeOrderDelivered(call: types.CallbackQuery, state: FSMContext):
    await update_status_order(call.data.split("_")[1])
    await adminSeeOrders(call, state)
@dp.callback_query_handler(text_contains="delete_")
async def adminSeeOrderDelete(call: types.CallbackQuery, state: FSMContext):
    await delete_order(call.data.split("_")[1])
    await adminSeeOrders(call, state)
@dp.callback_query_handler(text="product")
async def adminProducts(call: types.CallbackQuery):
    lang = await get_lang(call.from_user.id)
    btn = await adminProduct_inline(lang)
    await call.message.edit_reply_markup(btn)
@dp.callback_query_handler(text="product_back", state=AdminStates.product_name_ru)
@dp.callback_query_handler(text="product_back", state=AdminStates.product_name_uz)
@dp.callback_query_handler(text="product_back", state=AdminStates.price_mini)
@dp.callback_query_handler(text="product_back", state=AdminStates.price_big)
@dp.callback_query_handler(text="product_back", state=AdminStates.about_ru)
@dp.callback_query_handler(text="product_back", state=AdminStates.about_uz)
@dp.callback_query_handler(text="product_back", state=AdminStates.category)
@dp.callback_query_handler(text="product_back")
async def adminProductsBack(call: types.CallbackQuery, state: FSMContext):
    await adminProducts(call)
    await state.finish()
@dp.callback_query_handler(text="add_product")
async def adminProductsAdd(call: types.CallbackQuery):
    lang = await get_lang(call.from_user.id)
    btn = await adminProductBack_inline(lang)
    await call.message.edit_text(text["addProduct1"][lang], reply_markup=btn)
    await AdminStates.product_name_ru.set()
@dp.message_handler(state=AdminStates.product_name_ru)
async def adminProductNameRu(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    btn = await adminProductBack_inline(lang)
    await message.answer(text["addProduct2"][lang], reply_markup=btn)
    await state.update_data(product_name_ru=message.text)
    await AdminStates.product_name_uz.set()
@dp.message_handler(state=AdminStates.product_name_uz)
async def adminProductNameUz(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    btn = await adminProductBack_inline(lang)
    await message.answer(text["addProduct3"][lang], reply_markup=btn)
    await state.update_data(product_name_uz=message.text)
    await AdminStates.price_mini.set()
@dp.message_handler(state=AdminStates.price_mini)
async def adminProductPriceMini(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    btn = await adminProductBack_inline(lang)
    try:
        if message.text == "none":
            price = "none"
        else:
            price = int(message.text.replace(" ", ""))
            price = message.text
        await state.update_data(price_mini=price)
        await message.answer(text["addProduct4"][lang], reply_markup=btn)
        await AdminStates.price_big.set()
    except ValueError:
        await message.answer(text["incorrect"][lang], reply_markup=btn)
@dp.message_handler(state=AdminStates.price_big)
async def adminProductPriceBig(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    btn = await adminProductBack_inline(lang)
    try:
        price = int(message.text.replace(" ", ""))
        price = message.text
        await state.update_data(price_big=price)
        await message.answer(text["addProduct5"][lang], reply_markup=btn)
        await AdminStates.about_ru.set()
    except ValueError:
        await message.answer(text["incorrect"][lang], reply_markup=btn)
@dp.message_handler(state=AdminStates.about_ru)
async def adminProductAboutRu(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    btn = await adminProductBack_inline(lang)
    await message.answer(text["addProduct6"][lang], reply_markup=btn)
    await state.update_data(about_ru=message.text)
    await AdminStates.about_uz.set()
@dp.message_handler(state=AdminStates.about_uz)
async def adminProductAboutUz(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    categories = await select_all_categories()
    await state.update_data(add_product_page=1)
    btn = await categories_inline(lang, categories, 1)
    await message.answer(text["addProduct7"][lang], reply_markup=btn)
    await state.update_data(about_uz=message.text)
    await AdminStates.category.set()
@dp.callback_query_handler(text="add_category_prev", state=AdminStates.category)
async def adminProductCategoryPrev(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data["add_product_page"] > 1:
        updated_page = data["add_product_page"]-1
        await state.update_data(add_product_page=updated_page)
        lang = await get_lang(call.from_user.id)
        categories = await select_all_categories()
        btn = await categories_inline(lang, categories, updated_page)
        await call.message.edit_reply_markup(btn)
    else:
        await call.answer()
@dp.callback_query_handler(text="add_category_next", state=AdminStates.category)
async def adminProductCategoryNext(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    updated_page = data["add_product_page"]+1
    await state.update_data(add_product_page=updated_page)
    lang = await get_lang(call.from_user.id)
    categories = await select_all_categories()
    btn = await categories_inline(lang, categories, updated_page)
    if btn != None:
        await call.message.edit_reply_markup(btn)
    else:
        await state.update_data(add_product_page=data["add_product_page"])
        await call.answer()
@dp.callback_query_handler(text_contains="select_category:", state=AdminStates.category)
async def adminProductCategory(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(call.from_user.id)
    await state.update_data(category=call.data.split(":")[1])
    btn = await adminProductBack_inline(lang)
    await call.message.answer(text["addProduct8"][lang], reply_markup=btn)
    await AdminStates.photo.set()
@dp.message_handler(state=AdminStates.photo, content_types=["photo"])
async def adminProductPhoto(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    await state.update_data(photo=message.photo[0]["file_id"])
    data = await state.get_data()
    await message.answer(text["done"][lang])
    await insert_product(data["product_name_ru"], data["product_name_uz"], data["price_mini"], data["price_big"], data["about_ru"], data["about_uz"], data["category"], data["photo"])
    btn = await adminProduct_inline(lang)
    await message.answer(text["action"][lang], reply_markup=btn)
    await state.finish()
@dp.callback_query_handler(text="del_product")
async def adminProductDelete(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(call.from_user.id)
    products = await select_all_products()
    await state.update_data(delete_product_page=1)
    btn = await adminDelete_inline(lang, products, 1)
    await call.message.edit_reply_markup(btn)
@dp.callback_query_handler(text="product_next")
async def adminProductDeleteNext(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    updated_page = data["delete_product_page"]+1
    await state.update_data(delete_product_page=updated_page)
    lang = await get_lang(call.from_user.id)
    products = await select_all_products()
    btn = await adminDelete_inline(lang, products, updated_page)
    if btn != None:
        await call.message.edit_reply_markup(btn)
    else:
        await state.update_data(delete_product_page=data["delete_product_page"])
        await call.answer()
@dp.callback_query_handler(text="product_prev")
async def adminProductDeletePrev(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data["delete_product_page"] > 1:
        updated_page = data["delete_product_page"]-1
        await state.update_data(delete_product_page=updated_page)
        lang = await get_lang(call.from_user.id)
        products = await select_all_products()
        btn = await adminDelete_inline(lang, products, updated_page)
        await call.message.edit_reply_markup(btn)
    else:
        await call.answer()
@dp.callback_query_handler(text_contains="del_product:")
async def adminProductDel(call: types.CallbackQuery, state: FSMContext):
    id = call.data.split(":")[1]
    await delete_product(id)
    lang = await get_lang(call.from_user.id)
    categories = await select_all_products()
    data = await state.get_data()
    btn = await adminDelete_inline(lang, categories, data["delete_product_page"])
    if btn != None:
        await call.message.edit_reply_markup(btn)
    else:
        while True:
            data = await state.get_data()
            btn = await adminDelete_inline(lang, categories, data["delete_product_page"])
            if btn == None:
                await state.update_data(delete_product_page=data["delete_product_page"]-1)
                data = await state.get_data()
                btn = await adminDelete_inline(lang, categories, data["delete_product_page"])
                await call.message.edit_reply_markup(btn)
            else:
                break
@dp.callback_query_handler(text="admins")
async def admins(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(call.from_user.id)
    btn = await admins_inline(lang)
    await call.message.edit_reply_markup(btn)
@dp.callback_query_handler(text="admin_back", state=AdminStates.admin_id)
@dp.callback_query_handler(text="admin_back")
async def adminsBack(call: types.CallbackQuery, state: FSMContext):
    await admins(call, state)
@dp.callback_query_handler(text="admins_add")
async def adminsAdd(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(call.from_user.id)
    btn = await adminBack_inline2(lang)
    await call.message.edit_text(text["addAdmin"][lang], reply_markup=btn)
    await AdminStates.admin_id.set()
@dp.message_handler(state=AdminStates.admin_id)
async def adminsAddId(message: types.Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    await insert_admin(int(message.text))
    await message.answer(text["done"][lang])
    btn = await admins_inline(lang)
    await message.answer(text["action"][lang], reply_markup=btn)
    await state.finish()
@dp.callback_query_handler(text="admins_delete")
async def adminsDelete(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(call.from_user.id)
    products = await select_all_admins()
    await state.update_data(admin_page=1)
    btn = await adminsDelete_inline(lang, products, 1)
    await call.message.edit_reply_markup(btn)
@dp.callback_query_handler(text="admin_next")
async def adminsDeleteNext(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    updated_page = data["admin_page"]+1
    await state.update_data(admin_page=updated_page)
    lang = await get_lang(call.from_user.id)
    admins = await select_all_admins()
    btn = await adminsDelete_inline(lang, admins, updated_page)
    if btn != None:
        await call.message.edit_reply_markup(btn)
    else:
        await state.update_data(admin_page=data["admin_page"])
        await call.answer()
@dp.callback_query_handler(text="admin_prev")
async def adminsDeletePrev(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data["admin_page"] > 1:
        updated_page = data["admin_page"]-1
        await state.update_data(admin_page=updated_page)
        lang = await get_lang(call.from_user.id)
        admins = await select_all_admins()
        btn = await adminsDelete_inline(lang, admins, updated_page)
        await call.message.edit_reply_markup(btn)
    else:
        await call.answer()
@dp.callback_query_handler(text_contains="del_admin:")
async def adminsDeleteAdmin(call: types.CallbackQuery, state: FSMContext):
    id = call.data.split(":")[1]
    await delete_admin(id)
    lang = await get_lang(call.from_user.id)
    admins = await select_all_admins()
    data = await state.get_data()
    btn = await adminsDelete_inline(lang, admins, data["admin_page"])
    if btn != None:
        await call.message.edit_reply_markup(btn)
    else:
        while True:
            data = await state.get_data()
            btn = await adminsDelete_inline(lang, admins, data["admin_page"])
            if btn == None:
                await state.update_data(admin_page=data["admin_page"]-1)
                data = await state.get_data()
                btn = await adminsDelete_inline(lang, admins, data["admin_page"])
                await call.message.edit_reply_markup(btn)
            else:
                break
@dp.callback_query_handler(text="reviews")
async def adminsReviews(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(call.from_user.id)
    reviews = await select_all_reviews()
    await state.update_data(review_page=1)
    btn = await adminReviews_inline(lang, reviews, 1)
    if btn != None:
        await call.message.edit_text(text["action"][lang], reply_markup=btn)
    else:
        while True:
            data = await state.get_data()
            btn = await adminReviews_inline(lang, reviews, data["review_page"])
            if btn == None:
                await state.update_data(review_page=data["review_page"]-1)
                data = await state.get_data()
                btn = await adminReviews_inline(lang, reviews, data["review_page"])
                await call.message.edit_text(text["action"][lang], reply_markup=btn)
            else:
                break
@dp.callback_query_handler(text="review_back")
async def adminsReviewsBack(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(call.from_user.id)
    reviews = await select_all_reviews()
    data = await state.get_data()
    btn = await adminReviews_inline(lang, reviews, data["review_page"])
    if btn != None:
        await call.message.edit_text(text["action"][lang], reply_markup=btn)
    else:
        while True:
            data = await state.get_data()
            btn = await adminReviews_inline(lang, reviews, data["review_page"])
            if btn == None:
                await state.update_data(review_page=data["review_page"]-1)
                data = await state.get_data()
                btn = await adminReviews_inline(lang, reviews, data["review_page"])
                await call.message.edit_text(text["action"][lang], reply_markup=btn)
            else:
                break
@dp.callback_query_handler(text="review_next")
async def adminsReviewsNext(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    updated_page = data["review_page"]+1
    await state.update_data(review_page=updated_page)
    lang = await get_lang(call.from_user.id)
    reviews = await select_all_reviews()
    btn = await adminReviews_inline(lang, reviews, updated_page)
    if btn != None:
        await call.message.edit_reply_markup(btn)
    else:
        await state.update_data(review_page=data["review_page"])
        await call.answer()
@dp.callback_query_handler(text="review_prev")
async def adminsReviewsPrev(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data["review_page"] > 1:
        updated_page = data["review_page"]-1
        await state.update_data(review_page=updated_page)
        lang = await get_lang(call.from_user.id)
        reviews = await select_all_reviews()
        btn = await adminReviews_inline(lang, reviews, updated_page)
        await call.message.edit_reply_markup(btn)
    else:
        await call.answer()
@dp.callback_query_handler(text_contains="review:")
async def adminsReview(call: types.CallbackQuery, state: FSMContext):
    lang = await get_lang(call.from_user.id)
    id = call.data.split(":")[1]
    review = await select_review(id)
    btn = await adminReview_inline(lang, review)
    await call.message.edit_text(f"{text['username'][lang]}@{review[1]}\n\n{review[2]}", reply_markup=btn)
@dp.callback_query_handler(text_contains="review_del:")
async def adminsReviewDelete(call: types.CallbackQuery, state: FSMContext):
    id = call.data.split(":")[1]
    await delete_review(id)
    lang = await get_lang(call.from_user.id)
    reviews = await select_all_reviews()
    data = await state.get_data()
    btn = await adminReviews_inline(lang, reviews, data["review_page"])
    if btn != None:
        await call.message.edit_reply_markup(btn)
    else:
        while True:
            data = await state.get_data()
            btn = await adminReviews_inline(lang, reviews, data["review_page"])
            if btn == None:
                await state.update_data(review_page=data["review_page"]-1)
                data = await state.get_data()
                btn = await adminReviews_inline(lang, reviews, data["review_page"])
                await call.message.edit_reply_markup(btn)
            else:
                break


if __name__ == "__main__":
    create_tables()
    executor.start_polling(dp, skip_updates=True)