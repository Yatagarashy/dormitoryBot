from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext


class Registration(BaseFilter):
    async def __call__(self, event, state: FSMContext) -> bool:
        data = await state.get_data()

        try:
            if data["registration"] == True:
                return True
            else:
                return False
        except KeyError:
            return False