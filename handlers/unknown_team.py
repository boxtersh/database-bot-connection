from aiogram import types, Router, F

from dictionary_queries_and_inform import get_dict_info_for_user

router = Router()

@router.message(F.text)
async def pay_for_delivery_with_card(message: types.Message):
    text = message.text
    await message.reply(get_dict_info_for_user()['Неверная команда'].format(text = text))