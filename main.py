import asyncio
import logging
import sys
from config import token as TOKEN, admins
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states import CategoryState, Users, Karzinka
from base import InsertCategory, CategoryRead, ProductRead, TaomRead, InsertSavat, SavatRead, SavatDelete
from buttons import menyu, category, tasdiqlash, locations, tasdiqlash_uchun
from aiogram.utils.keyboard import InlineKeyboardBuilder
import time


bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
dp = Dispatcher()



@dp.message(Command('start'))
async def command_start_handler(message: Message, state: FSMContext):
    await message.answer(f"Bizning Restranga xush kelibsiz {message.from_user.full_name}", reply_markup=menyu)
    await message.delete()

@dp.callback_query(F.data == 'karzinka')
async def karzinkaBot(call: CallbackQuery, state:FSMContext):
    user_id = call.from_user.id
    savat = ""
    umumiy = 0
    savatlar = SavatRead(user_id=user_id)
    if len(savatlar) != 0:
        for i in savatlar:
            savat += f"{i[2]} ->  {i[3]} -> {i[4]} so'm\n"
            umumiy += int(i[4]) * int(i[3])
        await call.message.answer(f"sizdan {savat}\nUmumiy hisob {umumiy} so'm", reply_markup=tasdiqlash)
        await state.set_state(Karzinka.confirm)
        await call.message.delete()
    else:
        await call.answer("buyurtma bering")


@dp.callback_query(F.data=='menyu')
async def MenyuBot(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer_photo(photo="https://www.jotform.com/blog/wp-content/uploads/2020/07/online-ordering-for-restaurants-7cb342.png", caption="Bo'limlardan birini tanlang", reply_markup=category.as_markup())
    await call.message.delete()
    await state.set_state(Users.tanlash)


@dp.callback_query(F.data, Users.tanlash)
async def TanlashBot(call: CallbackQuery, state: FSMContext):
    xabar = call.data
    await state.update_data({"turi":xabar})
    if xabar == "ortga":
        await call.message.answer(f"Bizning restrandan tanlang", reply_markup=menyu)
        await call.message.delete()
    else:
        cat_id = 0
        for cat in CategoryRead():
            if cat[1] == xabar:
                cat_id += cat[0]
        taomlar = InlineKeyboardBuilder()
        for p in ProductRead(cat_id=cat_id):
            taomlar.button(text=f"{p[3]}", callback_data=f"{p[3]}")
        taomlar.button(text="⬅️ ortga", callback_data="orqaga")
        taomlar.adjust(2)
        await call.message.answer_photo(photo="https://sundayapp.com/app/uploads/2021/11/Sunday_restaurant_2294@2x.png", caption="Bulardan birini tanlang", reply_markup=taomlar.as_markup())
        await state.update_data(
            {'cat_id':cat_id}
        )
        await state.set_state(Users.taomlar)
        await call.message.delete()


@dp.callback_query(F.data, Users.taomlar)
async def Maxsulotlar(call: CallbackQuery, state: FSMContext):
    xabarcha = call.data
    if xabarcha == "orqaga":
        await call.message.answer_photo(photo="https://www.jotform.com/blog/wp-content/uploads/2020/07/online-ordering-for-restaurants-7cb342.png", caption="Bo'limlardan birini tanlang", reply_markup=category.as_markup())
        await call.message.delete()
        await state.set_state(Users.tanlash)
    else:
        await state.update_data(
            {"taom":xabarcha}
        )
        sonlar = InlineKeyboardBuilder()
        for i in range(1, 10):
            sonlar.button(text=f"{i}", callback_data=f"{i}")
        sonlar.button(text="⬅️ ortga", callback_data="orqaga")
        sonlar.adjust(3)
        a = TaomRead(xabarcha)
        narxi = a[0][2]
        print(narxi)
        await call.message.answer_photo(photo=f"{a[0][4]}", caption=f"Nomi {a[0][3]}\nNarxi: {a[0][2]}",reply_markup=sonlar.as_markup())
        await state.update_data({'narxi': narxi})
        await state.set_state(Users.soni)        
        await call.message.delete()



@dp.callback_query(F.data, Users.soni)
async def SonlarBot(call: CallbackQuery, state:FSMContext):
    xabar = call.data
    data = await state.get_data()
    cat_id = data.get("cat_id")
    user_id = call.from_user.id
    if xabar == "orqaga":
        for cat in CategoryRead():
            if cat[1] == xabar:
                cat_id += cat[0]
        taomlar = InlineKeyboardBuilder()
        for p in ProductRead(cat_id=cat_id):
            taomlar.button(text=f"{p[3]}", callback_data=f"{p[3]}")
        taomlar.button(text="⬅️ ortga", callback_data="orqaga")
        taomlar.adjust(2)
        await call.message.answer_photo(photo="https://sundayapp.com/app/uploads/2021/11/Sunday_restaurant_2294@2x.png", caption="Bulardan birini tanlang", reply_markup=taomlar.as_markup())
        await state.set_state(Users.taomlar)
        await call.message.delete()
    else:
        await state.update_data({'taom':xabar})
        await call.answer(f"savatga qo'shildi {xabar} ta")
        await state.update_data({"soni":xabar})
        await state.get_data()
        taom = data.get('taom')
        narxi = data.get('narxi')
        InsertSavat(user_id=user_id, taom=taom, soni=xabar, narxi=narxi)
        await call.message.answer(f"Bizning restrandan tanlang", reply_markup=menyu)
        await call.message.delete()
        await state.clear()



@dp.callback_query(F.data == "ha")
async def TasdiqlashBot(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Joylashuvingizni bo'lishing", reply_markup=locations)

@dp.message(F.location)
async def Joylashuv(message: Message):
    joylashuv1 = message.location.latitude
    user_id = message.from_user.id
    joylashuv2 = message.location.longitude
    savat = ""
    umumiy = 0
    savatlar = SavatRead(user_id=user_id)
    for i in savatlar:
        savat += f"{i[2]} ->  {i[3]} -> {i[4]} so'm\n"
        umumiy += int(i[4]) * int(i[3])
    a = f"sizdan {savat}\nUmumiy hisob {umumiy} so'm"
    await message.answer_location(latitude=joylashuv1, longitude=joylashuv2)
    await message.answer(text=f"Zakazlaringiz\n\n\n{a}", reply_markup=tasdiqlash_uchun)



@dp.callback_query(F.data == "true")
async def Tasdiqlash(call: CallbackQuery):
    savat = ""
    user_id = call.from_user.id
    umumiy = 0
    savatlar = SavatRead(user_id=user_id)
    for i in savatlar:
        savat += f"{i[2]} ->  {i[3]} -> {i[4]} so'm\n"
        umumiy += int(i[4]) * int(i[3])
    print("tasdiqlandi")

    
@dp.callback_query(F.data == "bekor")
async def Bekor(call: CallbackQuery):
    user_id = call.from_user.id
    await call.answer("Hamma zakaz o'chirildi", show_alert=True)
    SavatDelete(user_id=user_id)
    time.sleep(2)
    await call.message.answer(f"Bizning Restrandan yena zakaz berishingiz mumkin", reply_markup=menyu)
    await call.message.delete()


@dp.message(Command("category"), F.from_user.id.in_(admins))
async def CategoryAdd(message: Message, state: FSMContext):
    await message.answer("Taomning id yuboring")
    await state.set_state(CategoryState.id)

@dp.message(F.text, CategoryState.id)
async def CateMessage(message: Message, state: FSMContext):
    xabar = message.text
    if xabar.isdigit():
        await state.update_data(
            {"id":xabar}
        )
        await message.answer(f"Siz bergan id saqlandi\n Category name yuboring")
        await state.set_state(CategoryState.name)
    else:
        await message.answer("Siz Raqam yuboring ? ")
        await state.set_state(CategoryState.id)


@dp.message(F.text, CategoryState.name)
async def CateMessage(message: Message, state: FSMContext):
    xabar = message.text
    if xabar.isdigit():
        await message.answer("Siz Raqam yubordingiz ? ")
        await state.set_state(CategoryState.name)
    else:
        data = await state.get_data()
        id = data.get('id')
        InsertCategory(id=int(id),name=xabar)
        await message.answer("Siz yuborgan Category name saqlandi")
        await state.clear()



@dp.message(Command('menyu'), F.from_user.id.in_(admins))
async def Menyu(message: Message, state: FSMContext):
    a = ""
    for i in CategoryRead():
        a += f"{i[0]}" + " -> " + f"{i[1]}"  + '\n' 
    await message.answer(f"Siz Category tanlang\n{a}")



async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print("Tugadi")