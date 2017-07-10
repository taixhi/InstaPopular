from datetime import datetime
from os import environ
from time_util import sleep
from random import randint
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

class InstaPopular:
  def __init__(self, username=None, password=None, nogui=False):
    if nogui:
      self.display = Display(visible=0, size=(800, 600))
      self.display.start()

    self.username = username or environ.get('INSTA_USER')
    self.password = password or environ.get('INSTA_PW')
    self.nogui = nogui
    chrome_options = Options()
    chrome_options.add_argument('--dns-prefetch-disable')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--lang=en-US')
    chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en-US'})
    self.browser = webdriver.Chrome('./assets/chromedriver', chrome_options=chrome_options)
    self.browser.implicitly_wait(25)
    self.completeUserData = {'':[]}

  def login(self):
    """Used to login the user either with the username and password"""
    if not login_user(self.browser, self.username, self.password):
      print('Wrong login data!')
      print('Wrong login data!\n')

      self.aborting = True
    else:
      print('Logged in successfully!')
      print('Logged in successfully!\n')
    return self

  def logFollowers(self, usernames):
    for username in usernames:
      self.completeUserData.update(getUser(self.browser, username))
    print(self.completeUserData)
    return self.completeUserData

def getUser(browser, target_username):
  browser.get('https://www.instagram.com/' + target_username)
  try:
    followers = browser.find_elements_by_class_name('_bkw5z')[1].text
    followings = browser.find_elements_by_class_name('_bkw5z')[2].text
    shared_data = browser.execute_script('return window._sharedData')
    data = shared_data["entry_data"]["ProfilePage"][0]["user"]
    total_comment_count = 0
    total_like_count = 0
    for photo in data["media"]["nodes"]:
      total_comment_count += photo["comments"]["count"]
      total_like_count += photo["likes"]["count"]
    avg_comment_count = total_comment_count / len(data["media"]["nodes"])
    avg_like_count = total_like_count / len(data["media"]["nodes"])
  except IndexError:
    followers = 'null'
    followings = 'null'
    avg_like_count = 0
    avg_comment_count = 0
  except ZeroDivisionError:
    avg_like_count = 0
    avg_comment_count = 0
  userData = {target_username: [followers, followings, avg_like_count, avg_comment_count]}
  print('DATA:')
  print(userData)
  return userData

def login_user(browser, username, password):
  """Logins the user with the given username and password"""
  browser.get('https://www.instagram.com')

  #Check if the first div is 'Create an Account' or 'Log In'
  login_elem = browser.find_element_by_xpath("//article/div/div/p/a[text()='Log in']")
  if login_elem is not None:
    action = ActionChains(browser).move_to_element(login_elem).click().perform()

  #Enter username and password and logs the user in
  #Sometimes the element name isn't 'Username' and 'Password' (valid for placeholder too)
  inputs = browser.find_elements_by_xpath("//form/div/input")
  action = ActionChains(browser).move_to_element(inputs[0]).click().send_keys(username) \
          .move_to_element(inputs[1]).click().send_keys(password).perform()

  login_button = browser.find_element_by_xpath("//form/span/button[text()='Log in']")
  action = ActionChains(browser).move_to_element(login_button).click().perform()

  sleep(2)
  
  #Check if user is logged-in (If there's two 'nav' elements)
  nav = browser.find_elements_by_xpath('//nav')
  if len(nav) == 2:
    return True
  else:
    return False

session = InstaPopular(username='', password='')
session.login()
usernames = []
session.logFollowers(usernames)





