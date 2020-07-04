from selenium import webdriver
import time

try:
    browser = webdriver.Firefox()
    browser.get("https://shimo.im/login?from=home")
    browser.find_element_by_xpath('//input[@name="mobileOrEmail"]').send_keys("myemail")
    browser.find_element_by_xpath('//input[@name="password"]').send_keys("password")
    button = browser.find_element_by_class_name("submit")
    button.click()
except Exception as e:
    print(e)
finally:
    browser.close()
