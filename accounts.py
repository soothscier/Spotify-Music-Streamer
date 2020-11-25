from selenium import webdriver

from time import sleep
import csv
import random
import string

def getRandomString(length): #Letters and numbers
    pool=string.ascii_lowercase+string.digits
    return "".join(random.choice(pool) for i in range(length))

def getRandomText(length): #Chars only
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))

def createAccount(driver):
    # creating new spotify account
    driver.get('https://spotify-upgrade.net/upgrade')

    sleep(0.7)


    password = getRandomString(8)
    email = getRandomText(10)+"@"+getRandomText(8)+".com"
    
    driver.find_element_by_xpath('//*[@id="mainLogin"]/div/div[2]/div/div[2]/label[2]').click()
    sleep(1)

    driver.find_element_by_xpath('//*[@id="mainLogin"]/div/div[2]/div/div[1]/form[2]/div[2]/input').send_keys(email)
    driver.find_element_by_xpath('//*[@id="mainLogin"]/div/div[2]/div/div[1]/form[2]/div[3]/input').send_keys(password)
    driver.find_element_by_xpath('//*[@id="mainLogin"]/div/div[2]/div/div[1]/form[2]/div[4]/input').click()

    sleep(1.5)

    return {
        'email': email,
        'password': password
    }









