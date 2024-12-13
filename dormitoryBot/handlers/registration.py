from aiogram import Router, F, Bot, html
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from settings import CHANNEL_ID
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.callbacks import RegistrationCallback

from filters.exists_filter import ExistsFilter
from filters.registration_status_filter import Registration


router = Router()


@router.message(~ExistsFilter(), ~Registration())
async def user_not_exists(message: Message, bot: Bot, state: FSMContext):

    buttons = [
        [
            InlineKeyboardButton(text="✅", callback_data=RegistrationCallback(user_id=message.from_user.id).pack()),
            InlineKeyboardButton(text="⛔️", callback_data="reject"),
            InlineKeyboardButton(text="💬", url=f'tg://user?id={message.from_user.id}')
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await bot.send_message(CHANNEL_ID, f"(test) Пользователь {html.code(html.quote(message.from_user.first_name))} подал заявку на регистрацию", reply_markup=keyboard)
    await message.answer("⏳ Ожидается одобрение регистрации")

    data = await state.get_data()
    data["registration"] = True
    await state.set_data(data)


@router.message(~ExistsFilter(), Registration())
async def user_not_registered(message: Message):
    await message.answer("⏳ Ожидается одобрение регистрации")
