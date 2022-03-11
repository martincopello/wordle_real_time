import socketserver
import random
import time

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

def split_word(word):
    return ({letter: index for index, letter in enumerate(word)})

def set_timer():
    t = random.randrange(5, 30, 1)
    time.sleep(t)
    reset_wordle()

def reset_wordle():
    global curr_word
    global curr_solution
    global curr_puzzle_solved
    global wordle_ended
    global number_of_guesses
    global solve_count
    global curr_guess
    curr_word = pick_word(list_of_words)
    curr_solution = split_word(curr_word)
    curr_puzzle_solved = False
    wordle_ended = False
    number_of_guesses = 0
    curr_guess = {}

curr_word = pick_word(list_of_words)
curr_solution = split_word(curr_word)
curr_puzzle_solved = False
wordle_ended = False
number_of_guesses = 0
solve_count = 0
curr_guess = {}


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        global curr_word
        global curr_solution
        global curr_puzzle_solved
        global wordle_ended
        global number_of_guesses
        global solve_count
        global curr_guess

        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip() #receive string

        #If the client requests a new wordle and they have not already solved it, start it up
        if self.data.decode("utf-8") == "get_puzzle":
            message = "Wordle started. Go ahead and send me a guess.".encode("utf-8")
            self.request.sendall(message)
        #If the client has already solved the current puzzle, deny them
        elif curr_puzzle_solved == True:
            message = "You've already solved the current Wordle!".encode("utf-8")
            self.request.sendall(message)
        #If the client already used up all five of its guesses, deny them
        elif wordle_ended == True:
            message = "You've already failed to solve the current Wordle!".encode("utf-8")
            self.request.sendall(message)
        #If the client's guess is invalid, deny them
        elif len(self.data.decode("utf-8")) != 5 or not isinstance(self.data.decode("utf-8"), str):
            message = "Your guess is not a 5-letter word, therefore invalid.".encode("utf-8")
            self.request.sendall(message)
        #If they guess the word, send a congratulations message!
        elif self.data.decode("utf-8") == curr_word:
            message = "Congratulations! You've solved the Wordle".encode("utf-8")
            self.request.sendall(message)
            solve_count +=1
            reset_wordle()
        #If the client reaches 5 guesses and they have not solved it then reset the wordle
    elif number_of_guesses == 5:
            message = "it's OVER!".encode("utf-8")
            self.request.sendall(message)
            wordle_ended == True
            time.sleep(15)
            reset_wordle()
        #Otherwise increase the number of guesses and provide feedback to the client
        else:
            number_of_guesses += 1
            curr_guess = split_word(self.data.decode("utf-8"))
            message = {}
            for letter in curr_guess.keys():
                if letter in curr_solution.keys() and curr_guess[letter] == curr_solution[letter]:
                    print(letter)
                    message[letter]= "correct"
                elif letter in curr_solution.keys():
                    print(letter)
                    message[letter]= "present"
                else:
                    print(letter)
                    message[letter]= "absent"
            message = str(str(message) + str(curr_word)).encode("utf-8")
            self.request.sendall(message)
        print("{} wrote:".format(self.client_address[0]))

if __name__ == "__main__":
    #HOST, PORT = "localhost", 9999
    HOST, PORT = "127.0.0.1", 9999


    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
    #server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
