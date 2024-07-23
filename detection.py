import time
import ev3dev.ev3 as ev3
import serial

# Инициализация моторов и датчика
motor_left = ev3.LargeMotor('outA')
motor_right = ev3.LargeMotor('outB')
kicker = ev3.LargeMotor('outC')
us_sensor = ev3.UltrasonicSensor('in1')
us_sensor.mode = 'US-DIST-CM'

# Параметры ПИ регулятора
Kp, Ki = 7.5, 0.02
integral, last_error, dt = 0, 0, 0.1
target_distance = 20  # Целевая дистанция до стены в см

ser = serial.Serial('...', 9600)  # TODO: найти порт для подключения


def set_motor_speeds(speed_left, speed_right):
    """Функция для установки скорости моторов"""
    motor_left.run_forever(speed_sp=speed_left)
    motor_right.run_forever(speed_sp=speed_right)


def kick_off():
    """Функция для продвижения к продукту и удара"""
    set_motor_speeds(300, 300)
    time.sleep(0.5)
    motor_left.stop(stop_action='hold')
    motor_right.stop(stop_action='hold')
    kicker.run_forever(speed_sp=500)
    time.sleep(0.1)
    kicker.run_forever(speed_sp=-500)
    time.sleep(0.1)
    kicker.stop(stop_action='hold')


def send_message(message):
    """Получает сообщение по serial на rpi"""
    ser.write(message.encode('utf-8'))


def get_message():
    """Получает сообщение по serial из rpi"""
    return ser.readline().decode('utf-8').rstrip()


try:
    # Основной цикл управления
    while True:
        # Чтение текущей дистанции до стены
        current_distance = us_sensor.value() / 10  # Переводим мм в см

        if 15 <= current_distance <= 25:
            motor_left.stop(stop_action='hold')
            motor_right.stop(stop_action='hold')

            send_message('detected')  # Включение камеры, детект типа продукта
            result = get_message()
            if result == 'kick_off':
                kick_off()

            current_distance = us_sensor.value() / 10  # Продукт сбит, повторное чтение дистанции

        # Вычисление ошибки
        error = target_distance - current_distance

        # Интегральная часть
        integral += error * dt

        # ПИ регулятор
        correction = Kp * error + Ki * integral

        # Задание скорости моторов с учетом коррекции
        base_speed = 300  # Базовая скорость
        left_speed = base_speed - correction
        right_speed = base_speed + correction

        # Установка скоростей моторов
        set_motor_speeds(left_speed, right_speed)

        # Задержка для соблюдения dt
        time.sleep(dt)

except KeyboardInterrupt:
    # Остановка моторов при завершении программы
    motor_left.stop(stop_action='hold')
    motor_right.stop(stop_action='hold')
