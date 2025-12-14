from aiogram import filters, types, Router
from dictionary_queries_and_inform import get_dict_info_for_user

router = Router()


@router.message(filters.Command('start'))
async def start(message: types.Message):
    username = message.from_user.username
    await message.reply(get_dict_info_for_user()['Приветствие'].format(username = username))


@router.message(filters.Command('help'))
async def start(message: types.Message):
    await message.reply(get_dict_info_for_user()['Команды'])