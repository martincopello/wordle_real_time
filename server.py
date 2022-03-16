import socketserver
import random
import time
from Project.wordle_solver import *

def create_list_of_words(path):
    words = []
    with open(path, 'r') as file:
        for line in file:
            words.append(line.rstrip())
    file.close()
    return(words)

list_of_words = create_list_of_words('Project/FiveLetterWords.txt')

def pick_word(words_list):
    return(random.choice(words_list))

def set_timer():
    t = random.randrange(3, 4, 1)
    time.sleep(t)
    reset_wordle()

def reset_wordle():
    global curr_puzzle_solved
    global wordle_ended
    global number_of_guesses
    global solve_count
    global curr_guess
    curr_puzzle_solved = False
    wordle_ended = False
    number_of_guesses = 0
    curr_guess = {}
    ws = Wordle()


curr_puzzle_solved = False
wordle_ended = False
number_of_guesses = 0
solve_count = 0
curr_guess = {}
prior_solutions = []
ws = Wordle()

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        #global curr_word
        #global curr_solution
        global curr_puzzle_solved
        global wordle_ended
        global number_of_guesses
        global solve_count
        global curr_guess

        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip() #receive string
        print("Client wrote:", self.data.decode("utf-8"))
        if number_of_guesses < 0:
            pass

        #If the client requests a new wordle and they have not already solved it, start it up
        elif self.data.decode("utf-8") == "get_puzzle" and curr_puzzle_solved == False and wordle_ended == False:
            time.sleep(3)
            message = "Wordle started. Go ahead and send me a guess.".encode("utf-8")
            ws.target_word = pick_word(list_of_words)

            print("\nTarget word is:", ws.target_word, "\n")
            self.request.sendall(message)
            print("{} (Server) wrote:".format(self.client_address[0]), message.decode("utf-8"))

        #If the client has already solved the current puzzle, deny them
        elif curr_puzzle_solved == True:
            message = "You've already solved the current Wordle!".encode("utf-8")
            self.request.sendall(message)
            print("{} (Server) wrote:".format(self.client_address[0]), message.decode("utf-8"))
            print(f"You've solved {solve_count} of {len(prior_solutions)} Wordles \n \n")

        #If the client already used up all five of its guesses, deny them
        elif wordle_ended == True:
            message = "You've already failed to solve the current Wordle!".encode("utf-8")
            self.request.sendall(message)
            print("{} (Server) wrote:".format(self.client_address[0]), message.decode("utf-8"))
            print(f"You've solved {solve_count} of {len(prior_solutions)} Wordles \n \n")

        #If the client's guess is invalid, deny them
        elif len(self.data.decode("utf-8")) != 5 or not isinstance(self.data.decode("utf-8"), str):
            message = str("Your guess is not a 5-letter word, therefore invalid." + self.data.decode("utf-8")).encode("utf-8")
            self.request.sendall(message)
            print("{} (Server) wrote:".format(self.client_address[0]), message.decode("utf-8"))

        #If they guess the word, send a congratulations message!
        elif self.data.decode("utf-8") == ws.target_word:
            message = "Congratulations! You've solved the Wordle".encode("utf-8")
            self.request.sendall(message)
            print("{} (Server) wrote:".format(self.client_address[0]), message.decode("utf-8"))
            solve_count +=1
            curr_puzzle_solved = True
            prior_solutions.append(ws.target_word)
            print(f"You've solved {solve_count} of {len(prior_solutions)} Wordles \n \n")
            set_timer()

        #If the client reaches 5 guesses and they have not solved it then reset the wordle
        elif number_of_guesses == 5:
            message = "You've reached five guesses. Wait until the next Wordle starts!".encode("utf-8")
            self.request.sendall(message)
            print("{} (Server) wrote:".format(self.client_address[0]), message.decode("utf-8"))
            wordle_ended == True
            number_of_guesses = -1
            prior_solutions.append(ws.target_word)
            print(f"You've solved {solve_count} of {len(prior_solutions)} Wordles \n \n")
            set_timer()

        #Otherwise increase the number of guesses and provide feedback to the client
        else:
            number_of_guesses += 1
            curr_guess_feedback = ws.assess_word(self.data.decode("utf-8"))[2]
            message = str(curr_guess_feedback).encode("utf-8")
            self.request.sendall(message)
            print("{} (Server) wrote: ".format(self.client_address[0]), message.decode("utf-8"))

if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 9999

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
