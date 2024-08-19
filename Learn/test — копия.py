import socket
import threading
from colorama import Fore, Style, init

# Инициализация цветового вывода
init(autoreset=True)

# Цвета для сообщений
COLORS = {
    "1": Fore.RED,
    "2": Fore.GREEN,
    "3": Fore.YELLOW,
    "4": Fore.BLUE,
    "5": Fore.MAGENTA,
    "6": Fore.CYAN
}

# Функция для приема сообщений
def receive_messages(connection_socket):
    while True:
        try:
            message = connection_socket.recv(1024).decode("utf-8")
            if message:
                print(message)
        except:
            break

# Функция для отправки сообщений
def send_messages(connection_socket, username, color):
    while True:
        message = input(f"{color}{username}: ")
        if message:
            # Форматируем сообщение с цветом и именем пользователя
            colored_message = f"{color}{username}: {message}{Style.RESET_ALL}"
            try:
                connection_socket.send(colored_message.encode("utf-8"))
            except:
                print("Соединение закрыто.")
                break

            
# Функция для установки соединения с другим пользователем
def connect_to_peer():
    #peer_ip = input("Введите IP другого пользователя: ")
    peer_ip = "192.168.254.128"
    #peer_port = int(input("Введите порт другого пользователя: "))
    peer_port = 333
    
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_socket.connect((peer_ip, peer_port))
    
    return peer_socket

# Функция для прослушивания входящих соединений (серверная часть)
def listen_for_peers(local_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', local_port))
    server_socket.listen(5)
    
    print(f"Слушаю входящие соединения на порту {local_port}...")
    
    connection_socket, addr = server_socket.accept()
    print(f"Подключен новый пользователь: {addr}")
    
    return connection_socket

if __name__ == "__main__":
    # Регистрация пользователя
    #username = input("Введите ваше имя: ")
    username = "Vania"

    print("Выберите цвет:")
    for num, color in COLORS.items():
        print(f"{num}: {color}Пример текста")
    
    #color_choice = input("Введите номер выбранного цвета: ")
    color_choice = "2"
    color = COLORS.get(color_choice, Fore.WHITE)  # Если неверный выбор, ставим белый цвет по умолчанию
    
    # Определяем роль
    #role = input("Вы хотите подключиться к другому пользователю или ждать подключения? (connect/listen): ")
    role = "connect"

    if role == 'listen':
        # Ввод порта для прослушивания
        local_port = int(input("Введите порт для прослушивания: "))
        # Ждем подключения другого пользователя
        connection_socket = listen_for_peers(local_port)
    else:
        # Подключаемся к другому пользователю
        connection_socket = connect_to_peer()
    
    # Запуск потоков для отправки и получения сообщений
    receive_thread = threading.Thread(target=receive_messages, args=(connection_socket,))
    send_thread = threading.Thread(target=send_messages, args=(connection_socket, username, color))
    
    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()
