import socket
import sys
import time
import random
from Project.wordle_solver import *


HOST, PORT = "localhost", 9999
#Create string we want to capitalize
# Create a socket (SOCK_STREAM means a TCP socket)
message = str()
PingServerAgain = True

def set_timer():
    global PingServerAgain
    t = random.randrange(2, 3, 1)
    time.sleep(t)
    PingServerAgain = True
    message = str()

ws = Wordle()
#Can implement the timed run with a while variable is False do nothing. but then have a timer to set it to true. set the variable to false at the end of a wordle
while PingServerAgain == True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: #creating the socket
        #solutions = []  # Connect to server and send data
        sock.connect((HOST, PORT)) #we tell socket to connect to server

        #If you just created the socket, ask for a new Wordle
        if message == "":
            message = "get_puzzle"
            sock.sendall(message.encode("utf-8")) #send string that I created. Need to convert string to bytes before sending to server
            print("Sent: {}".format(message))
            received = str(sock.recv(1024), "utf-8")
            print("Received: {}".format(received))

        #If the server responds saying that the Wordle started, enter a first word. In this case, adieu
        elif received == "Wordle started. Go ahead and send me a guess.":
            message = "orate"
            sock.sendall(message.encode("utf-8"))
            print("Sent: {}".format(message))
            received = str(sock.recv(1024), "utf-8")
            print("Received: {}".format(received))

        #If the server responds saying that we already failed to solve the current Wordle, set timer and try again later when the Wordle may have reset
        elif received == "You've already failed to solve the current Wordle!":
            message = ""
            PingServerAgain == False
            ws.read_words()
            set_timer()

        #If the server responds saying that we lost, set timer and try again later when the Wordle may have reset
        elif received == "You've reached five guesses. Wait until the next Wordle starts!":
            message = ""
            PingServerAgain == False
            ws.read_words()
            set_timer()

        elif received == "You've already solved the current Wordle!":
            message = ""
            PingServerAgain == False
            ws.read_words()
            set_timer()

        elif received == "Congratulations! You've solved the Wordle":
            print("\n \n")
            message = ""
            PingServerAgain == False
            ws.read_words()
            set_timer()
        #Otherwise, send another guess word
        #We can program how to work with the feedback we're receiving from the server
        else:
            #This is currently sending "crony" over and over. this is where we would incorporate our solver and its guesses
            #message="crony"
            #print(received, message)
            rules, matched_counts = ws.parse_rule_codes(received,message)
            ws.apply_rules(rules, matched_counts)
            message = ws.get_test_word()[0]
            sock.sendall(message.encode("utf-8"))
            print("Client wrote: {}".format(message))
            received = str(sock.recv(1024), "utf-8")
            print("Server wrote {}".format(received))

        sock.close()
