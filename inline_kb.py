import os
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from yoomoney_test import pay_base_url
from dotenv import find_dotenv, load_dotenv
# сбор переменных .env
load_dotenv(find_dotenv())
# url kb
inline_kb_builder_urls = InlineKeyboardBuilder()
inline_kb_builder_urls.row(InlineKeyboardButton(text='Pay', url=pay_base_url.base_url))
inline_kb_builder_urls.row(InlineKeyboardButton(text='Lenin_street', url=os.getenv('LENIN_STREET')))
inline_kb_builder_urls.row(InlineKeyboardButton(text='hedgehog.png', url=os.getenv('HEDGEHOG_URI')))
# Callback kb
inline_kb_builder_a_2 = InlineKeyboardBuilder()
inline_kb_builder_a_2.row(InlineKeyboardButton(text='Значение таблицы А2', callback_data='a_2'))
