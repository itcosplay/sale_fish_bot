from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup


class UserState(StatesGroup):
    handle_menu = State()
    handle_description = State()
    handle_cart = State()
    handle_email = State()

    selected_product_id = State()
