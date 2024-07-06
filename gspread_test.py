import os
import gspread
from dotenv import load_dotenv, find_dotenv

# сбор переменных .env
load_dotenv(find_dotenv())
# функция аутентификации
gc = gspread.service_account(filename='test.json')

# открываем google table
wks = gc.open(os.getenv('TABLE_NAME')).sheet1

# переменная с результатом A2
a_2 = wks.acell('A2').value


# функция добавления данных в google table
def wks_append(user_input_date: str) -> None:
    wks.append_row([user_input_date, 'Дата верна'])
