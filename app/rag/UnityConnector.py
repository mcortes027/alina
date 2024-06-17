import socket
import threading
from Rag import Rag  # Ensure Rag has a queryllm method

class UnityConnector:
    def __init__(self, host, port, connections):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (host, port)
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(connections)
        self.rag = Rag()  # Instance of Rag to use for LLM queries

    def handle_client(self, connection):
        with connection:
            print('Client connected:', connection)
            while True:
                print("Listening for data")
                try:
                    data = connection.recv(1024)
                    if data:
                        message = data.decode()
                        print(f'Received: {message}')
                        #connection.sendall("HOLA!, SOY ALINA".encode())
                        #print("Sending intermediate response and processing message")
                        # connection.sendall("got it, making reply, wait".encode())
                        # Simulate or perform actual processing
                        response = self.rag.queryllm(message)
                        self.rag.to_audio(response, "/audio/response_audio")
                        print(f"Response from LLM: {response}")
                        connection.sendall(f"{response}\n".encode())

                        #connection.sendall("all green, output\n".encode())
                    else:
                        print('No more data from client.')
                        break
                except Exception as e:
                    print(f'Error handling data from client: {e}')
                    break

    def run(self):
        while True:
            try:
                print('Waiting for a connection')
                connection, client_address = self.server_socket.accept()
                print(f'Connection from {client_address}')
                client_thread = threading.Thread(target=self.handle_client, args=(connection,))
                client_thread.start()
            except Exception as e:
                print(f'Error accepting connection: {e}')

def run_unity_connector():
    uc = UnityConnector("0.0.0.0", 8501, 5)
    uc.run()

if __name__ == '__main__':
    run_unity_connector()