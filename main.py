import os
import asyncio
from datetime import datetime

import aiogram.utils.markdown as fmt
from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, Command, StateFilter
from dotenv import find_dotenv, load_dotenv
from inline_kb import inline_kb_builder_urls, inline_kb_builder_a_2
from gspread_test import a_2, wks_append

# сбор переменных .env
load_dotenv(find_dotenv())
# инициализация бота
bot = Bot(os.getenv('TOKEN'))
# инициализация диспетчера
dp = Dispatcher()


# класс состояния
class Date(StatesGroup):
    date = State()


# /start
@dp.message(CommandStart())
async def start(massage: types.Message) -> None:
    '''
    список команд
    '''

    commands = fmt.text(
        fmt.text(fmt.hbold('Полный список команд: ')),
        fmt.text(fmt.hbold('/urls'), fmt.hitalic(' - Ссылки')),
        fmt.text(fmt.hbold('/res_table'), fmt.hitalic(' - данные из таблицы')),
        fmt.text(fmt.hbold('/wr_table'), fmt.hitalic(' - Запись в таблицу')),
        sep='\n'
    )

    await massage.answer(text=commands, parse_mode='HTML')


# /urls
@dp.message(Command('urls'))
async def urls(message: types.Message) -> None:
    '''
    возврат пользователю клавиатуру  с ссылками:
    Pay
    Lenin_street
    hedgehog.png
    '''
    await message.answer('Выберите необходимую ссылку:', reply_markup=inline_kb_builder_urls.as_markup())


# res_table
@dp.message(Command('res_table'))
async def urls_table(message: types.Message) -> None:
    '''
    возврат пользователю клавиатуры с результатом поиска
    '''
    await message.answer('Для получения результата просто нажмите:', reply_markup=inline_kb_builder_a_2.as_markup())


# обработка нажатия на кнопку
@dp.callback_query(F.data == 'a_2')
async def process_callback_button(callback_query: types.CallbackQuery) -> None:
    '''
    возврат результата
    '''
    await callback_query.answer(f'Результат: {a_2}')


# /wr_table
@dp.message(Command('wr_table'))
async def write_table(message: types.Message, state: FSMContext) -> None:
    '''
    Просим пользователя ввести дату формата ГГ-ММ-ДД
    '''
    await message.answer('Введите дату (в формате ГГ-ММ-ДД):')
    await state.set_state(Date.date)


# /break
@dp.message(Command('break'), StateFilter("*"))
async def date_cancel(message: types.Message, state: FSMContext) -> None:
    '''
    выход из fsm
    '''
    await state.clear()
    await message.answer(text=fmt.hitalic('Действие отменено.'), parse_mode='HTML')


# fsm
@dp.message()
async def get_date(message: types.Message, state: FSMContext) -> None:
    try:
        # проверка шаблона
        datetime.strptime(message.text, '%y-%m-%d')
        # добавление message.text в google table при успешной проверке
        wks_append(user_input_date=message.text)
        # сохраняем состояние
        await state.update_data(date=message.text)
        # получаем состояние
        data = await state.get_data()
        # сообщаем пользователю об успешном добавлении
        await message.answer(fmt.hitalic(f'Дата верна.\nВаша дата {data.get("date")}'), parse_mode='HTML')
        # чистим состояние
        await state.clear()
    except ValueError:
        # при неудачной попытке просил пользователя повторить
        text = fmt.text(
            fmt.text(fmt.hitalic(f'Дата неверна\nВведите дату (в формате ГГ-ММ-ДД):')),
            fmt.text(fmt.hbold('/break'), fmt.hitalic('Отмена')),
            sep="\n\n",
        )
        await message.answer(text=text, parse_mode='HTML')


async def main() -> None:
    # дроп ожидающих обновлений
    await bot.delete_webhook(drop_pending_updates=True)
    # запускает бота в режиме опроса
    await dp.start_polling(bot)


# запуск бота
if __name__ == '__main__':
    print('Bot started!')
    asyncio.run(main())
