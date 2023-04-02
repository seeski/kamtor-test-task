import csv

# чтобы не дублировать код я создал функцию, который вернет массив с значениями изменений цены
def exec_changes(filepath: str) -> list[int]:
    changes = []
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            # чтобы не возиться с регулярками, я закинул все в try|except конструкцию
            # будут отлавливаться IndexError и ValueError
            try:
                lst = list(row[6])
                # попаем знак %, чтобы преобразовать к float
                lst.pop()
                changes.append(
                    float(''.join(lst))
                )
            except:
                continue

    return changes

# данные взяты с https://www.barchart.com/
ethusdt_changes = exec_changes(r'^ethusdt_price-history-04-01-2023.csv')
btcusdt_changes = exec_changes('^btcusdt_price-history-04-01-2023.csv')

# чтобы найти среднее значение бета-коэффициента, нужно вычислить значение за взятый промежуток времени
# я взял последние 2 года
coefficients = []

# списки одинаковой длины, можно взять длину массива ethusdt, можно btcusdt
for i in range(len(ethusdt_changes)):
    # приводим бету к изменениям на 1%
    # т.е. считаем, насколько % изменилась цена эфира после того, как биток вырос/упал на 1%
    beta = (1 / btcusdt_changes[i]) * ethusdt_changes[i]
    coefficients.append(beta)

beta_coefficient = sum(coefficients) / len(coefficients) # 2.3205286654936277
