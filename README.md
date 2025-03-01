# Тепличная среда: автоматизация сбора урожая в теплицах
[![en](https://img.shields.io/badge/lang-EN-red?style=flat-square)](https://github.com/snowlue/cif-robotics-2024/blob/main/README.en.md)
### Состав команды
- Павел Овчинников: [VK](https://vk.com/snowlue), [Telegram](https://t.me/snowlue), [GitHub](https://github.com/snowlue)
- Михаил Журавлёв: [VK](https://vk.com/gentlemanofgoodluck), [Telegram](https://t.me/zhurik_ne_zhulik), [GitHub](https://github.com/crazycrendel)
## Постановка задачи
В рамках Кавказского инвестиционного форума в лаборатории «Робототехника» ЦНИИ РТК предложил нам в формате хакатона собрать за 2 дня работающий прототип робота, который будет решать один из трёх кейсов:
- Тепличная среда — необходимо автоматизировать сбор урожая в теплице так, чтобы робот собирал урожай только определённого типа (например, только томаты или всё, кроме томатов)
- Городская среда — необходимо организовать движение робота по площадке так, чтобы он следовал знакам дорожного движения и сигналам светофора
- Медицинская среда — необходимо по заданному роботу ArUco-маркеру выбрать лекарство из медицинского блока с лекарствами, изъять его из ячейки и доставить до точки назначения

## Решение задачи
Кейсы назначаются каждой команде путём жеребьёвки, и нашей команде достался кейс «Тепличная среда». Поскольку нас было двое, мы решили разделить задачи: Михаил Журавлёв отвечал за конструирование, а я взял на себя программирование. Моя основная цель — создать модель, способную отличать друг от друга зелёное яблоко, красное яблоко, баклажан, красный перец, жёлтый перец, томат и лимон. В репозитории содержится только программная часть.

Чтобы достичь нашей главной цели, мы снимали продукты с разных ракурсов на камеру смартфона. Затем мы вручную разметили и аннотировали несколько сотен отдельных кадров из полученных видео. На основе этого набора данных мы [обучили модель YOLOv10](https://blog.roboflow.com/yolov10-how-to-train). После этого модель самостоятельно разметила оставшиеся кадры — нам оставалось только проверить и подкорректировать разметку. На полученном наборе данных мы ещё раз обучили новую модель YOLOv10. В результате у нас есть сохранённая модель в формате .pt, которая может в режиме реального времени распознавать урожай, получая изображение с камеры.

![Video Capture_screenshot_17 07 2024](https://github.com/user-attachments/assets/a9140197-06e7-4379-a7b5-1731597cc30d)


### Комплектующие робота:
- Детали конструктора Lego Mindstorms
- Микрокомпьютер Lego Mindstorms EV3 для управления роботом
- Raspberry Pi 4 для управления камерой и работы модели нейронной сети
- Камера для захвата изображения урожая
- Сервомоторы Lego Mindstorms EV3 — ×2 для движения робота, ×1 для сборщика урожая
- Ультразвуковой датчик измерения расстояния Lego Mindstorms EV3 (дальномер)

### Алгоритм работы робота:
1. На Raspberry Pi 4 запускается `recognition.py`, который подключается к микрокомпьютеру Lego Mindstorms EV3 по SSH и запускает на нём `detection.py`.
2. Робот с подключённым к нему микрокомпьютером EV3 начинает движение, используя ультразвуковой датчик, чтобы искать резкие скачки в изменении расстояния. Когда скачок обнаружен, EV3 передаёт сигнал на Pi 4 по USB-соединению.
3. Pi 4 получает сигнал от EV3, включает камеру и распознаёт тип урожая. Если тип урожая соответствует заданному, то Pi 4 передаёт сигнал на EV3 о необходимости сбора урожая, в противном случае — о необходимости продолжить движение. Затем камера выключается.
4. EV3 получает сигнал от Pi 4 и, в зависимости от результата, либо собирает урожай, либо продолжает движение.

По итогу хакатона мы смогли запустить отдельно `recognition.py` на Pi 4 и `detection.py` на EV3 — камера распознавала тип урожая, в том числе если продуктов в кадре несколько, а инфракрасный датчик останавливал движение робота и EV3 был готов передавать сигнал на Pi 4, но установить соединение по USB, к сожалению, не вышло. В случае коммерческого успеха мы готовы доработать прототип до рабочего состояния — свяжитесь с нами!
