from aiogram import filters, types, Router
from dictionary_queries_and_inform import get_dict_info_for_user

router = Router()
dict_info = get_dict_info_for_user()

@router.message(filters.Command('start'))
async def start(message: types.Message):
    username = message.from_user.username
    await message.reply(dict_info['Приветствие'].format(username = username))


@router.message(filters.Command('help'))
async def start(message: types.Message):
    await message.reply(dict_info['Команды'])