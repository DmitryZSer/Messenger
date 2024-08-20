import socket
import threading

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                print(message)
                broadcast(message, client_socket)
            else:
                break
        except:
            break

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode("utf-8"))
            except:
                clients.remove(client)

if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Укажите IP-адрес вашего сервера в локальной сети
    server_ip = '192.168.254.128'
    server_port = 5500

    server.bind((server_ip, server_port))
    server.listen(5)

    clients = []

    print(f"Сервер запущен на {server_ip}:{server_port} и ожидает подключения...")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        print(f"Подключен клиент: {addr}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()
