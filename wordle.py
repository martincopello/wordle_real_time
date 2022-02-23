from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

url = 'https://www.nytimes.com/games/wordle/index.html'
#driver = webdriver.Safari(executable_path="/usr/bin/safaridriver")
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

#Identify controls for the game
host = driver.find_element_by_tag_name("game-app")
game = driver.execute_script("return arguments[0].shadowRoot.getElementById('game')", host)
keyboard = game.find_element_by_tag_name("game-keyboard")
keys = driver.execute_script("return arguments[0].shadowRoot.getElementById('keyboard')", keyboard)

#Check the letters we've entered
driver.execute_script("return arguments[0].innerHTML;",keys)
#Trying to get rid of the pop up screen with instructions on Safari
#Works on Chrome though
#driver.find_element_by_tag_name("body").click()
#driver.find_element_by_class_name("nightmode").click()

#Click on screen to get rid of pop up screen
obj = driver.find_element_by_tag_name('html')
obj.click()

#Send words
obj.send_keys('thorn')
obj.send_keys(Keys.ENTER)

#Once puzzle is solved, refresh forever until game resets
driver.refresh()
