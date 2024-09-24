from aiogram.fsm.state import State, StatesGroup

class CategoryState(StatesGroup):
    id = State()
    name = State()

class Users(StatesGroup):
    tanlash = State()
    taomlar = State()
    soni = State()

class Karzinka(StatesGroup):
    confirm = State()
    finish = State()