from aiogram import Router, F, Bot, html
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from settings import CHANNEL_ID
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.callbacks import RegistrationCallback

from filters.exists_filter import ExistsFilter
from filters.registration_status_filter import Registration
from filters.registration_input import RegistrationInput

from sqlite3 import Cursor


router = Router()



@router.callback_query(RegistrationCallback.filter())
async def accept_registration(callback: CallbackQuery, bot: Bot, state: FSMContext, cursor: Cursor, callback_data: RegistrationCallback):
    # await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (callback.from_user.id,))
    user = cursor.fetchone()
    first_name = user[1]
    last_name = user[2]
    surname = user[3]
    floor = user[4]
    room = user[5]
    role = user[6]
    await bot.send_message(CHANNEL_ID, f"📝 {html.bold(role)} | {first_name} {last_name} | Начал(а) регистрацию пользователя")
    await bot.send_message(callback.from_user.id, "✏️ Введите <b>Имя</b> пользователя")

    data = await state.get_data()
    data["registration_user_id"] = callback_data.user_id
    data["registration_input_state"] = "first_name"
    await state.set_data(data)


# Ввели Имя пользователя
@router.message(RegistrationInput("first_name"))
async def enter_first_name(message: Message, state: FSMContext):


    await message.answer("✏️ Введите <b>Фамилию</b> пользователя")


    data = await state.get_data()
    data["registration_user_first_name"] = message.text
    data["registration_input_state"] = "last_name"
    await state.set_data(data)


# Ввели фамилию пользователя
@router.message(RegistrationInput("last_name"))
async def enter_last_name(message: Message, state: FSMContext):


    await message.answer("✏️ Введите <b>Отчество</b> пользователя")


    data = await state.get_data()
    data["registration_user_last_name"] = message.text
    data["registration_input_state"] = "surname"
    await state.set_data(data)


# Ввели Отчество пользователя
@router.message(RegistrationInput("surname"))
async def enter_surname(message: Message, state: FSMContext):


    await message.answer("✏️ Введите <b>Этаж</b> пользователя")


    data = await state.get_data()
    data["registration_user_surname"] = message.text
    data["registration_input_state"] = "floor"
    await state.set_data(data)


# Ввели Этаж пользователя
@router.message(RegistrationInput("floor"))
async def enter_floor(message: Message, state: FSMContext):


    await message.answer("✏️ Введите <b>Комнату</b> пользователя")


    data = await state.get_data()
    data["registration_user_floor"] = message.text
    data["registration_input_state"] = "room"
    await state.set_data(data)


# Ввели Комнату пользователя
@router.message(RegistrationInput("room"))
async def enter_room(message: Message, state: FSMContext):

    buttons = [
        [
            InlineKeyboardButton(text="🧽 Дежурный", callback_data='Дежурный'),
            InlineKeyboardButton(text="🛡 Опер", callback_data='Опер'),
            InlineKeyboardButton(text="🗝 Староста", callback_data='Староста'),
        ],
        [
            InlineKeyboardButton(text="🔒 Админ", callback_data='Админ'),
            InlineKeyboardButton(text="🔐 Гл. Админ", callback_data='Гл. Админ')
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    data = await state.get_data()
    data["registration_user_room"] = message.text
    data["registration_input_state"] = "role"
    # data.pop("registration_input_state")
    await state.set_data(data)


@router.callback_query()
async def enter_role(callback: CallbackQuery, state: FSMContext, cursor: Cursor):
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (callback.from_user.id,))
    user = cursor.fetchone()
    role = user[6]

    data = await state.get_data()

    first_name = data["registration_user_first_name"]
    last_name = data["registration_user_last_name"]
    surname = data["registration_user_surname"]
    floor = data["registration_user_floor"]
    room = data["registration_user_room"]
    role = callback.data




    if callback.data == "Дежурный" and role in ["Староста", "Гл. Админ"]:
        data["registration_user_role"] = callback.data
        data["registration_input_state"] = "correct"

        await callback.message.edit_reply_markup(reply_markup=None)

        await callback.message.answer(f'📍 Проверьте верность данных:\n<pre>ФИО: {first_name} {last_name} {surname}\nЭтаж: {floor}\nКомната: {room}\nРоль: {role}</pre>')

    elif callback.data == "Дежурный" and role not in ["Староста", "Гл. Админ"]:
        await callback.answer(show_alert=True, text="🔐 Недостаточно прав")


    elif callback.data == "Опер" and role == "Гл. Админ":
        data["registration_user_role"] = callback.data
        data["registration_input_state"] = "correct"

        await callback.message.edit_reply_markup(reply_markup=None)

        await callback.message.answer(f'📍 Проверьте верность данных:\n<pre>ФИО: {first_name} {last_name} {surname}\nЭтаж: {floor}\nКомната: {room}\nРоль: {role}</pre>')

    elif callback.data == "Опер" and role != "Гл. Админ":
        await callback.answer(show_alert=True, text="🔐 Недостаточно прав")


    elif callback.data == "Староста" and role == "Гл. Админ":
        data["registration_user_role"] = callback.data
        data["registration_input_state"] = "correct"

        await callback.message.edit_reply_markup(reply_markup=None)

        await callback.message.answer(f'📍 Проверьте верность данных:\n<pre>ФИО: {first_name} {last_name} {surname}\nЭтаж: {floor}\nКомната: {room}\nРоль: {role}</pre>')

    elif callback.data == "Староста" and role != "Гл. Админ":
        await callback.answer(show_alert=True, text="🔐 Недостаточно прав")


    elif callback.data == "Админ" and role == "Гл. Админ":
        data["registration_user_role"] = callback.data
        data["registration_input_state"] = "correct"

        await callback.message.edit_reply_markup(reply_markup=None)

        await callback.message.answer(f'📍 Проверьте верность данных:\n<pre>ФИО: {first_name} {last_name} {surname}\nЭтаж: {floor}\nКомната: {room}\nРоль: {role}</pre>')

    elif callback.data == "Админ" and role != "Гл. Админ":
        await callback.answer(show_alert=True, text="🔐 Недостаточно прав")


    elif callback.data == "Гл. Админ" and role == "Гл. Админ":
        data["registration_user_role"] = callback.data
        data["registration_input_state"] = "correct"

        await callback.message.edit_reply_markup(reply_markup=None)

        await callback.message.answer(f'📍 Проверьте верность данных:\n<pre>ФИО: {first_name} {last_name} {surname}\nЭтаж: {floor}\nКомната: {room}\nРоль: {role}</pre>')

    elif callback.data == "Гл. Админ" and role != "Гл. Админ":
        await callback.answer(show_alert=True, text="🔐 Недостаточно прав")

    await state.set_data(data)