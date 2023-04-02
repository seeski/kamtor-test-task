from config import api_key, secret_key
from binance.client import Client
from datetime import datetime, timedelta


# прописываем бета-коэффициент
beta_coefficient = 2.3205286654936277

# создаем клиента
client = Client(api_key=api_key, api_secret=secret_key)

# устанавливаем точку отсчета по времени и цене
last_hour_starts = datetime.now()
last_hour_start_price = float(client.futures_symbol_ticker(symbol="ETHUSDT")['price'])

# создаем массив, куда будем заносить модули значений изменений цены
last_hour_changes = []


while True:
    # парсим цену и считаем разницу в процентах между точкой отсчета
    ethusdt_price = float(client.futures_symbol_ticker(symbol="ETHUSDT")['price'])
    ethusdt_change = (last_hour_start_price - ethusdt_price) / last_hour_start_price * 100

    # собственные движения ethusdt
    prediction = ethusdt_price + (ethusdt_price / 100) * beta_coefficient

    # добавляем изменения цены в массив last_hour_changes
    last_hour_changes.append(abs(ethusdt_change))

    # если прошел час, то мы программа проваливается в условие
    if datetime.now() >= last_hour_starts + timedelta(hours=1):

        # проверка на наличие изменений на 1%
        if max(last_hour_changes) > 1:
            print(f"в период с {last_hour_starts.strftime('%H:%M:%S')} по {datetime.now().strftime('%H:%M:%S')} цена изменилась на 1%")

        # меняем точку отсчета времени и цены, очищаем список
        last_hour_starts = datetime.now()
        last_hour_start_price = ethusdt_price
        last_hour_changes.clear()

# Спасибо!
# t.me/se3ski