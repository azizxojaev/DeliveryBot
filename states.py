from aiogram.dispatcher.filters.state import StatesGroup, State


class SettingsStates(StatesGroup):
    settings_action = State()
    lang = State()

class ReviewStates(StatesGroup):
    review = State()

class MenuStates(StatesGroup):
    size = State()
    quantity = State()
    location = State()
    locationText = State()
    yesNo = State()
    category = State()
    product = State()
    price = State()
    phone = State()
    payType = State()
    order = State()
    last_time = State()
    time = State()

class AdminStates(StatesGroup):
    category_ru = State()
    category_uz = State()
    category_photo = State()
    category_photo_uz = State()
    page = State()
    category_page = State()
    product_name_ru = State()
    product_name_uz = State()
    price_mini = State()
    price_big = State()
    about_ru = State()
    about_uz = State()
    category = State()
    photo = State()
    add_product_page = State()
    delete_product_page = State()
    admin_id = State()
    admin_page = State()
    review_page = State()