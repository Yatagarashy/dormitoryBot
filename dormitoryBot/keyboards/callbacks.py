from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from typing import Literal 



class RegistrationCallback(CallbackData, prefix='reg'):
    user_id: int
    # action: Literal['r', 'a'] # Reject / Accept

