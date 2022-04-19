from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup


class UserState(StatesGroup):
    selectig_product = State()
    adding_cart = State()
    cart = State()
    