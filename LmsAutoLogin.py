#import numpy.core.multiarray
from io import BytesIO
import sys
# from sys import argv
from time import sleep
import requests
# import shutil
from PIL import Image
import numpy as np
from selenium import webdriver
import pytesseract
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import random
import configparser
# import io

uname = None
passwd = None

config = configparser.ConfigParser()
config.read('config.ini')

if len(sys.argv) > 1:
    uname = sys.argv[1]
    passwd = sys.argv[2]
else:
    uname = config.get("UserData","UserName")
    passwd = config.get("UserData","Password")

# options = ChromeOptions()
# options.add_argument("--start-maximized")
browser = webdriver.Chrome()
browser.maximize_window()
browser.implicitly_wait(5)


browser.get("https://lms"+str(random.randint(1, 10))+ ".uk.ac.ir")
WebDriverWait(browser, 20).until(EC.url_contains("mainpage.aspx"))
browser.find_element_by_id(
    "ctl00_PortalMasterPageStandardHeader_LoginStatusMainL").click()
img = None
try:
    while EC.url_contains('loginPage.aspx'):
        arr = None
        captcha = browser.find_element_by_id("ctl00_mainContent_myRadCaptcha_CaptchaImageUP")

        src = captcha.get_attribute('src')

        r = requests.get(src, stream=True)


        if r.status_code == 200:
            r.raw.decode_content = True
            try:
                image = Image.open(BytesIO(r.content))
                grayscale = image.convert("L")
                arr = np.array(grayscale)
            except Exception as e:
                print(e)

        for i in range(0,len(arr)):
            for j in range(0,len(arr[i])):
                if arr[i][j] >= 165:
                    arr[i][j] = 255
                else:
                    arr[i][j] = 0

        for i in range(0, len(arr)):
            for j in range(0, len(arr[i])):
                if (i < 7 or j < 7) or (i > len(arr) - 7 or j > len(arr[i]) - 7):
                    arr[i][j] = 255

        for count in range(0,10):
            arr2 = arr
            for margin in range(1,6):
                for i in range(margin, len(arr)-margin):
                    for j in range(margin, len(arr[i])-margin):
                        if arr2[i-margin][j] == 255 and arr2[i+margin][j] == 255 and arr2[i][j-margin] == 255 and arr2[i][j+margin] == 255 and arr2[i-margin][j-margin] == 255 and arr2[i-margin][j+margin] == 255 and arr2[i+margin][j+margin] == 255 and arr2[i+margin][j-margin] == 255:
                            arr[i][j] = 255

        for count in range(0,10):
            arr2 = arr
            margin = 3
            for i in range(margin, len(arr)-margin):
                for j in range(margin, len(arr[i])-margin):
                    if arr2[i-margin][j] == 255 and arr2[i+margin][j] == 255 and arr2[i][j-margin] == 255 and arr2[i][j+margin] == 255:
                        arr[i][j] = 255

        for count in range(0, 15):
            arr2 = arr
            for margin in range(1, 6):
                for i in range(margin, len(arr)-margin):
                    for j in range(margin, len(arr[i])-margin):
                        if arr2[i-margin][j] == 255 and arr2[i+margin][j] == 255 and arr2[i][j-margin] == 255 and arr2[i][j+margin] == 255 and arr2[i-margin][j-margin] == 255 and arr2[i-margin][j+margin] == 255 and arr2[i+margin][j+margin] == 255 and arr2[i+margin][j-margin] == 255:
                            arr[i][j] = 255

        for count in range(0, 10):
            arr2 = arr
            margin = 3
            for i in range(margin, len(arr)-margin):
                for j in range(margin, len(arr[i])-margin):
                    if arr2[i-margin][j] == 255 and arr2[i+margin][j] == 255 and arr2[i][j-margin] == 255 and arr2[i][j+margin] == 255:
                        arr[i][j] = 255
                            
        for count in range(0, 10):
            arr2 = arr
            margin = 1
            for i in range(margin, len(arr)-margin):
                for j in range(margin, len(arr[i])-margin):
                    if (arr2[i-margin][j] == 255 and arr2[i+margin][j] == 255) or (arr2[i][j-margin] == 255 and arr2[i][j+margin] == 255):
                        arr[i][j] = 255

        img = Image.fromarray(arr)
        
        captchaText = pytesseract.image_to_string(
            img, config='--psm 8 outputbase digits')
        print(captchaText)
        if len(captchaText) == 7:
            print('login')
            if EC.presence_of_element_located((By.ID,"LoginButton")):
                try:
                    username = browser.find_element_by_id('UserName')
                    password = browser.find_element_by_id('Password')
                    captchaBox = browser.find_element_by_id(
                        'ctl00_mainContent_myRadCaptcha_CaptchaTextBox')
                    submit = browser.find_element_by_id("LoginButton")

                    username.clear()
                    username.send_keys(uname)

                    password.clear()
                    password.send_keys(passwd)

                    captchaBox.clear()
                    captchaBox.send_keys(captchaText)

                    submit.click()
                except Exception as e:
                    browser.refresh()

        else:
            browser.find_element_by_id(
                'ctl00_mainContent_myRadCaptcha_CaptchaLinkButton').click()
            sleep(2)
except:
    pass
quit()
