from selenium import webdriver
import os


def login(username, pw):
    browser = webdriver.Chrome()
    browser.get('https://www.google.com/')
    search = browser.find_element_by_name("q")
    search.send_keys(username)
    butn = browser.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[3]/center/input[1]')
    butn.click()
    browser.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/a/h3').click()
    browser.find_element_by_xpath('/html/body/div[1]/header/div/div[2]/div[2]/a[1]').click()
    userinput = browser.find_element_by_id('login_field')
    userinput.send_keys(username)
    userpass = browser.find_element_by_id('password')
    userpass.send_keys(pw)
    browser.find_element_by_xpath('//*[@id="login"]/form/div[4]/input[9]').click()
    g = input("Enter your 2FA Code : ")
    auth = browser.find_element_by_id('otp')
    auth.send_keys(g)
    browser.find_element_by_xpath('//*[@id="login"]/div[5]/form/button').click()


if __name__ == "__main__":
    username = 'vipink1203'
    pw = os.environ['gitpass']
    login(username, pw)
