from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup


class UserState(StatesGroup):
    select_product = State()
    