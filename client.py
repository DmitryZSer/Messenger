import socket
import threading
from colorama import Fore, Style, init

# Инициализация colorama для работы с цветами в терминале
init(autoreset=True)

username = ""

COLORS = {
    "1": Fore.RED,
    "2": Fore.GREEN,
    "3": Fore.YELLOW,
    "4": Fore.BLUE,
    "5": Fore.MAGENTA,
    "6": Fore.CYAN
}

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                print(message)
        except:
            break

def send_messages(client_socket, username, color):
    while True:
        message = input(f"{color}{username}: ")
        if message:
            colored_message = f"{color}{username}: {message}{Style.RESET_ALL}"
            client_socket.send(colored_message.encode("utf-8"))

if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.254.128', 5500))

    # Ввод имени пользователя
    username = input("Введите ваше имя: ")

    # Выбор цвета
    print("Выберите цвет для сообщений:")
    print("1 - Красный")
    print("2 - Зеленый")
    print("3 - Желтый")
    print("4 - Синий")
    print("5 - Магента")
    print("6 - Циан")

    color_choice = input("Введите номер цвета: ")
    color = COLORS.get(color_choice, Fore.WHITE)  # По умолчанию - белый цвет

    # Уведомление о подключении к чату
    client.send(f"{color}{username} подключился к чату!".encode("utf-8"))

    # Поток для получения сообщений
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    # Поток для отправки сообщений
    send_thread = threading.Thread(target=send_messages, args=(client, username, color))
    send_thread.start()
