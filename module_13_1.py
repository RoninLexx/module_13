import asyncio


async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')

    for i in range(1, 6):  # Подъем 5 шаров
        await asyncio.sleep(1 / power)  # Задержка обратно пропорциональна силе
        print(f'Силач {name} поднял {i} шар{"а" if i == 1 else "ов"}')

    print(f'Силач {name} закончил соревнования.')


async def start_tournament():
    # Создаем задачи для соревнований
    tasks = [start_strongman('Pasha', 3), start_strongman('Denis', 4),
             start_strongman('Apollon', 5)]

    # Ожидаем выполнения всех задач
    await asyncio.gather(*tasks)


# Запуск асинхронной функции
asyncio.run(start_tournament())
