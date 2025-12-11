from aiogram import types, Router, F

router = Router()

@router.message(F.text)
async def pay_for_delivery_with_card(message: types.Message):
    await message.reply(f'Вы ввели команду:\n{message.text}\nданная команда мне не известна⁉️ 🤔\n\n'
                        f'Список доступных команд:\n/help\n\n'
                        f'попробуйте ещё раз ✍️, у вас обязательно получится 👇')