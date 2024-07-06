import os
from uuid import uuid4
from yoomoney import Quickpay, Client
from dotenv import find_dotenv, load_dotenv

# сбор переменных .env
load_dotenv(find_dotenv())
# инициализация клиента
client = Client(token=os.getenv('TOKEN_YOOMONEY'))
# получаем уникальный label
label = str(uuid4())

# получение ссылки
pay_base_url = Quickpay(
    receiver=os.getenv('WALLET_NUMBER_YOOMONEY'),
    quickpay_form='shop',
    targets='test',
    paymentType='VV',
    sum=2,
    label=label
)


