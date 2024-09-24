from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from base import CategoryRead


menyu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Menyu 🛍", callback_data="menyu")],
        [InlineKeyboardButton(text="Karzinka 🛒", callback_data="karzinka"), InlineKeyboardButton(text="Bog'lanish", url='t.me//rajabov_shohruhbek')]
    ]
)



category = InlineKeyboardBuilder()
for cat in CategoryRead():
    category.button(text=f"{cat[1]}", callback_data=f"{cat[1]}")
category.button(text="⬅️ ortga", callback_data="ortga")
category.adjust(2)

tasdiqlash = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Zakaz Berish", callback_data="ha"), InlineKeyboardButton(text="bekor qilish",callback_data='bekor')]
    ]
)


locations = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Joylashuv yuboring", request_location=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

tasdiqlash_uchun = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Tasdiqlash ✅", callback_data="true"), InlineKeyboardButton(text="Bekor qilish ❌",callback_data="false")]
    ]
)
