
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
import time

#  Custom word solution dictionary
with open("possible_solutions_freq.txt") as f:
  word_dictionary = f.read().splitlines()[1:]

# Run the Selenium Process for the Official Wordle site
url = 'https://www.nytimes.com/games/wordle/index.html'
#driver = webdriver.Safari(executable_path="/usr/bin/safaridriver")
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

#Identify controls for the game
host = driver.find_element(By.TAG_NAME,"game-app")
game = driver.execute_script("return arguments[0].shadowRoot.getElementById('game')", host)
keyboard = game.find_element(By.TAG_NAME,"game-keyboard")
keys = driver.execute_script("return arguments[0].shadowRoot.getElementById('keyboard')", keyboard)

#Check the letters we've entered
driver.execute_script("return arguments[0].innerHTML;",keys)
#Trying to get rid of the pop up screen with instructions on Safari
#Works on Chrome though
#driver.find_element_by_tag_name("body").click()
#driver.find_element_by_class_name("nightmode").click()

#Click on screen to get rid of pop up screen
page = driver.find_element(By.TAG_NAME,'html')
page.click()

#Send words
# obj.send_keys('raced')
# obj.send_keys(Keys.ENTER)

# after first guess
def input(word):
  # function to enter the wordle guess
  page.send_keys(word)
  page.send_keys(Keys.RETURN)
  time.sleep(2)


def output():
  # return the feedback data from the guessed word
  # local data contains json with site interaction info including guess results
  local_data = driver.execute_script("return window.localStorage;")
  game_info = local_data["nyt-wordle-state"]
  # guessed word results - in json form
  game_response = json.loads(game_info)["evaluations"]
  return game_response

# word freq list tends to get hung up on rarely used words, refinements to the dictionary
# limit the search space
possible_words = word_dictionary
# input your first guess word here - research points to roate and adieu as being very good
word = "roate"
# run functions
input(word)
evals = output()
# track what letters we've found
found_list = []

for q in range(5):
  stats = evals[q]
  correct_tally = 0
  for i in range(5):
    if (stats[i] != "absent") and (not word[i] in found_list):
      found_list.append(word[i])
    if stats[i] == "correct":
      correct_tally += 1
  if correct_tally == 5:
    time.sleep(2.5)
    page.click()
    quit()
  for i in range(5):
    print(evals)
    letter = word[i]
    # eliminate all words with the absent letters
    # eliminate all words without present letters
    # eliminate all words without correct positioned letters
    if stats[i] == "absent":
      if letter in found_list:
        possible_words = [x for x in possible_words if (x.count(letter) == 1) and (x[i] != letter)]
      else:
        possible_words = [x for x in possible_words if not letter in x]
    elif stats[i] == "present":
      possible_words = [x for x in possible_words if (letter in x) and (x[i] != letter)]
    elif stats[i] == "correct":
      possible_words = [x for x in possible_words if letter == x[i]]
  word = possible_words[0]
  input(word)
  evals = output()
  # handle if word is not accepted by
  while type(evals[q+1]) is not list:
    for i in range(5):
      page.send_keys(Keys.BACKSPACE)
    possible_words.remove(word)
    word = possible_words[0]
    input(word)
    evals = output()


time.sleep(2.5)
driver.close()
