import socket
import sys
import time
HOST, PORT = "localhost", 9999
#Create string we want to capitalize

# Create a socket (SOCK_STREAM means a TCP socket)
message = str()

#Can implement the timed run with a while variable is False do nothing. but then have a timer to set it to true. set the variable to false at the end of a wordle
while True:
    global message
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: #creating the socket
        #solutions = []  # Connect to server and send data
        sock.connect((HOST, PORT)) #we tell socket to connect to server
        if message == "":
            message = "get_puzzle"
            sock.sendall(message.encode("utf-8")) #send string that I created. Need to convert string to bytes before sending to server
            print("Sent: {}".format(message))
            received = str(sock.recv(1024), "utf-8")
            print("Received: {}".format(received))
        elif received == "Wordle started. Go ahead and send me a guess.":
            message = "adieu"
            sock.sendall(message.encode("utf-8"))
            print("Sent: {}".format(message))
            received = str(sock.recv(1024), "utf-8")
            print("Received: {}".format(received))
        elif received == "You've already faield to solve the current Wordle!":
            message = str()
        elif received == "it's OVER!":
            message = str()
        else:
            #this is currently sending "crony" over and over. this is where we would incorporate our solver and its guesses
            message="crony"
            sock.sendall(message.encode("utf-8"))
            print("Sent: {}".format(message))
            received = str(sock.recv(1024), "utf-8")
            print("Received: {}".format(received))
        #if we receive a word from the server here we can feed it into our model and send back a word guess to the server
        sock.close()
        time.sleep(1)
