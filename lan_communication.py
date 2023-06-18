import socket

def __init__(self) -> None:
    #Server erstellen
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Client erstellen
    self.client_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_ip="255.255.255.255"
    
def setup_connection_as_server(self):
    self.server_socket.bind((self.server_ip, 12345))  # Binden an die lokale Adresse und den Port 12345
    self.server_socket.listen(1)  # Anzahl der maximalen Verbindungen
    #Warte auf Verbindung
    self.client_socket, self.address = self.server_socket.accept()  # Auf eine eingehende Verbindung warten
    #Verbunden mit: address(client_socket)

def setup_connection_as_client(self):
      # Verbindung zum Server herstellen über den Port
    self.client_socket.connect((self.server_ip, 12345))
    
def get_data_as_server(self):
    data = self.client_socket.recv(1024)  # Daten empfangen (maximal 1024 Bytes)
    return data.decode()

def send_data_as_server(self, data):
    self.server_socket.sendall(data.encode())

def get_data_as_client(self):
    data = self.client_socket.recv(1024)  # Daten empfangen (maximal 1024 Bytes)
    return data.decode()

def send_data_as_client(self, data):
    self.client_socket.sendall(data.encode())

def close_connection(self):
    self.client_socket.close()  # Verbindung schließen
    self.server_socket.close()  # Server-Socket schließen






