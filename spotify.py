from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import accounts

from multiprocessing import Process, Lock

from time import sleep
import csv


def playPlaylist(driver, playlist, lock, like):
    """
    @desc
    Function to stream spotify playlist or song
    
    @param
    - driver => selenium webdriver instance
    - playlist => list of songs or playlist to play
    - lock => Multiprocessing lock instance for process synchronization
    - like => if true, likes the song or playlist
    """
    
    for play in playlist:
        print(play)
        lock.acquire()
        driver.get(play[0])
        lock.release()
        lock
        try:
            # waiting for play button to load
            myElem = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "_11f5fc88e3dec7bfec55f7f49d581d78-scss")))
        except:
            pass
        
        # clicking play button to play music
        element = driver.find_element_by_class_name('_11f5fc88e3dec7bfec55f7f49d581d78-scss')
        driver.execute_script("arguments[0].click();", element)

        # like music
        if like:
            element = driver.find_element_by_class_name('_11f5fc88e3dec7bfec55f7f49d581d78-scss')
            driver.execute_script("arguments[0].click();", element)
            
        sleep(float(play[1])*60) # wait for song to finish
    
    driver.quit()


def loginToSpotify(driver, playlist, lock, like):
    """
    @desc
    Function to log in to Spotify and play the playlist link send as a parameter.
    
    @param
    - driver => selenium webdriver instance
    - playlist => list of songs or playlist to play
    - lock => Multiprocessing lock instance for process synchronization
    - like => if true, likes the song or playlist
    """
    # ---------------------------------------------------------------------------------------------
    # code to create a new spotify account and then login to it
    
    lock.acquire()
    login = accounts.createAccount(driver) # creates a new spotify account using accounts.py
    
    driver.get('https://accounts.spotify.com/en/login') 

    driver.find_element_by_xpath('//*[@id="login-username"]').send_keys(login['email'])
    driver.find_element_by_xpath('//*[@id="login-password"]').send_keys(login['password'])
    driver.find_element_by_xpath('//*[@id="login-button"]').click()
    
    lock.release()
    
    sleep(2)
    
    # ---------------------------------------------------------------------------------------------
    
    playPlaylist(driver, playlist, lock, like)


def initializeSpotify(driver, playlist, lock, like):
    
    loginToSpotify(driver, playlist, lock, like)
    
    


if __name__ == "__main__":

    with open('playlist.csv', 'r') as rFile:
        reader = csv.reader(rFile)


        playlist = []

        for i in reader[1:]:
            playlist.append(i)

        Processes = []

        for num in range(4): # creating 4 webdriver instances to stream on spotify
            like = False

            if num%2 == 0: # every second song or playlist will be liked
                like = True 
            
            driver = webdriver.Chrome()
            lock = Lock()
            
            p = Process(target=initializeSpotify, args=(driver, playlist, lock, like,))
            p.start()
            Processes.append(p)

        
        for p in Processes:
            p.join() 
