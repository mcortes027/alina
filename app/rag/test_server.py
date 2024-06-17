import socket

def test_server(host, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print(f"Sending to server: {message}")
        client_socket.sendall(message.encode('utf-8'))

        response = client_socket.recv(1024)
        print(f"Received from server: {response.decode('utf-8')}")

if __name__ == '__main__':
    HOST, PORT = 'localhost', 8501
    MESSAGE = "mandado desde python"
    test_server(HOST, PORT, MESSAGE)