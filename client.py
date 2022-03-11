import socket
import sys

HOST, PORT = "localhost", 9999
data = "i am martin, hi" #Create string we want to capitalize

# Create a socket (SOCK_STREAM means a TCP socket)
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: #creating the socket
        solutions = []  # Connect to server and send data
        sock.connect((HOST, PORT)) #we tell socket to connect to server
        sock.sendall(bytes(data + "\n", "utf-8")) #send string that I created. Need to convert string to bytes before sending to server

        # Receive data from the server and shut down
        received = str(sock.recv(1024), "utf-8") #here we expect response from server

        #if we receive a word from the server here we can feed it into our model and send back a word guess to the server
        print("Sent:     {}".format(data))
        print("Received: {}".format(received))
        sock.close()
        time.sleep(5)
