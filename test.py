from djitellopy import Tello

tello = Tello()
tello.connect()

# Установка битрейта видео (в Кбит/с)
tello.set_video_bitrate(5)  # Например, 5 Мбит/с

# Запуск видеопотока
tello.streamon()

# Ваш код для обработки видеопотока

# Остановка видеопотока и отключение от дрона
tello.streamoff()
tello.disconnect()
