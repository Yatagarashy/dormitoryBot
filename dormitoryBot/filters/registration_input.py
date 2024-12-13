from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext


class RegistrationInput(BaseFilter):
    def __init__(self, input_type: str):
        self.input_type = input_type

    async def __call__(self, event, state: FSMContext) -> bool:
        data = await state.get_data()
        print(data)
        try:
            if data["registration_input_state"] == self.input_type:
                return True
            else:
                return False
        except KeyError:
            return False