'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
user_name='daniel'
password ='12345'
driver = webdriver.Chrome()
driver.get("http://127.0.0.1:8000/")
'''
from selenium import webdriver

driver = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.
driver.get('http://www.google.com/');
time.sleep(5) # Let the user actually see something!
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5) # Let the user actually see something!
driver.quit()