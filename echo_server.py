import socket

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('127.0.0.1', 23))  # 127.0.0.1 is this computer,  23 is the port
        server_socket.listen(1)
        print(f"Server started")

        while True:
            client_socket, client_address = server_socket.accept()  # start listening, waiting for client connections
            with client_socket:  # a client has connected
                print(f"Connection from {client_address}")
                client_socket.sendall(b"Welcome to the Telnet-like server!\r\n")  # send a welcome message, terminated by a newline
                incoming_buffer = b""
                while True:
                    data = client_socket.recv(1024)  # wait for data from the client, max 1024 bytes
                    incoming_buffer += data  # add the received data to the buffer
                    pos = incoming_buffer.find(b"\r\n")  # check if the buffer contains a newline
                    if pos != -1:
                        message = incoming_buffer[:pos]  # extract the message
                        print(message)
                        if len(message) == 0:
                            break  # exit the loop if the message is empty
                        client_socket.sendall(b"You said: " + message + b"\r\n")  # respond to the client
                        incoming_buffer = incoming_buffer[pos + 2:]  # remove the message from the buffer



