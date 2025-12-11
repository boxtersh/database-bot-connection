from aiogram import filters, types, Router
from dictionary_queries_and_inform import get_dict_query

router = Router()


@router.message(filters.Command('start'))
async def start(message: types.Message):
    user_id = message.from_user.username
    await message.reply(get_dict_query()['Приветствие'].format(user_id = user_id))


@router.message(filters.Command('help'))
async def start(message: types.Message):
    await message.reply(get_dict_query()['Команды'])