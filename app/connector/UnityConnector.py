import socket
from rag import Rag
class UnityConnector:

    def __init__(self,host,port,connections):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (host, port)  # Use your desired port number
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(connections)
        self.rag = Rag()

    def send(self, msg):
        self.sock.send(msg.encode())
    def receive(self):
        return self.sock.recv(1024).decode()
    def close(self):
        self.sock.close()
    def run(self):
        while True:
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = self.server_socket.accept()

            try:
                print(f'connection from {client_address}')

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(16)
                    print(f'received "{data}"')
                    if data:
                        # Here you can call your "rag" logic handler function
                        print('calling rag logic handler')
                        self.handle_rag_logic(data)
                        # Optionally, send data back
                        # connection.sendall(data)
                    else:
                        print('no more data from', client_address)
                        break
                    
            finally:
                # Clean up the connection
                connection.close()
    
    def handle_rag_logic(self,prompt):
        response = self.rag.queryllm(prompt)
        self.send(response)
#Angela ip: 192.168.1.222
