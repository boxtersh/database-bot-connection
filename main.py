import asyncio
from aiogram import Bot, Dispatcher
from config import token
from handlers import special, crud, unknown_team
from repo import DB


async def main():
    bot = Bot(token=token())
    dp = Dispatcher()
    dp.include_routers(
        special.router,
        crud.router,
        unknown_team.router
    )

    await DB.creating_tables()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())