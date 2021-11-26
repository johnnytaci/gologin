import threading
import time
import os
from multiprocessing import Pool
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from gologin import GoLogin
from random import randrange,choice,random
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep,process_time
from selenium.webdriver.common.action_chains import ActionChains
import numpy
from PIL import Image,ImageEnhance
from io import BytesIO
from functions import *
from threading import Thread
import queue

def calc_time(wait_time):
    a = process_time()
    timee = 0
    while timee < wait_time:
        b = process_time()
        timee = b - a
    if timee>wait_time:
        raise TimeoutError

def create_driver(profiles,queue):
    gl = GoLogin({
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2MTg5M2Q1NGFhOGNiMDcwYTI4OWViNGMiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2MTg5M2Q2NjJjNmRjMDFiZWMwYjdiNGEifQ.qDkIhHC_nzv2xVLQT4ZeqzsYDJWhrRGW3TBnzPwsRjw',
        'profile_id': profiles['profile_id'],
        'port': profiles['port'],
        "local": True,
        "credentials_enable_service": False,

    })

    if platform == "linux" or platform == "linux2":
        chrome_driver_path = './chromedriver'
    elif platform == "darwin":
        chrome_driver_path = './mac/chromedriver'
    elif platform == "win32":
        chrome_driver_path = 'chromedriver.exe'

    debugger_address = gl.start()
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", debugger_address)
    chrome_options.headless = True
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
    return queue.put(driver)


def scrap(profiles):
    br_created = 0
    q = queue.Queue()
    while br_created == 0:
        # lock.acquire()
        create_driver(profiles,q)
        # lock.release()
        if q.empty():
            return print('nuk u krijua driveri')
        else:
            driver = q.get()
            br_created+=1
    # phone_number = randrange(700000000, 799999999)
    # driver.get('https://www.tiktok.com/login/phone-or-email')
    # sleep(5)
    # country = 'Azerba'
    # driver.find_element_by_xpath('//div[contains(text(),"+")]').click()
    # sleep(random())
    # country_field = driver.find_element_by_xpath("//input[@placeholder='Search']")
    # for i in range(len(str(country))):
    #     country_field.send_keys(str(country)[i])
    #     sleep((random())/8)
    # sleep(random())
    # driver.find_element_by_xpath(f'//span[contains(text(),"{country}")]').click()
    # phone_field = driver.find_element_by_xpath("//input[@placeholder='Phone number']")
    # for i in range(len(str(phone_number))):
    #     phone_field.send_keys(str(phone_number)[i])
    #     sleep((random())/8)
    # send_code = driver.find_element_by_xpath('//button[contains(text(), "Send code")]')
    # sleep(random())
    # send_code.click()
    # verify_captcha(driver)
    #################################################
    #################################################
    #################################################
    #################################################
    #################################################
    #################################################
    phone_number = randrange(700000000, 799999999)
    country = 'Azerba'
    date_of_birth = [randrange(1, 28), randrange(1, 12), randrange(1980, 2000)]
    driver.get('https://www.tiktok.com/signup/phone-or-email')
    print('Opening Tiktok')
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"When’s your birthday?")]'))
    ).click()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November','December']
    month = choice(months)
    day = str(date_of_birth[0])
    year = str(date_of_birth[2])
    driver.maximize_window()
    sleep(random())
    index = months.index(month)
    driver.find_element_by_xpath('//div[contains(text(),"Month")]').click()
    sleep(random())
    for i in range(index):
        monthi = driver.find_element_by_xpath(f'//span[contains(text(),"{months[i]}")]')
        driver.execute_script("arguments[0].scrollIntoView(true);", monthi)
        sleep((random()) / 5)
    month = driver.find_element_by_xpath(f'//span[contains(text(),"{month}")]')
    driver.execute_script("arguments[0].click();", month)
    sleep(random())
    driver.find_element_by_xpath('//div[contains(text(),"Day")]').click()
    sleep(random())
    for i in range(int(day)):
        day_btn = driver.find_element_by_xpath(f'//span[contains(text(),"{i}")]')
        driver.execute_script("arguments[0].scrollIntoView(true);", day_btn)
        sleep((random()) / 5)
    day_btn = driver.find_element_by_xpath(f'//span[contains(text(),"{day}")]')
    driver.execute_script("arguments[0].click();", day_btn)
    sleep(random())
    driver.find_element_by_xpath('//div[contains(text(),"Year")]').click()
    sleep(random())
    for i in range(2020,int(year),-1):
        year_btn = driver.find_element_by_xpath(f'//span[contains(text(),"{i}")]')
        driver.execute_script("arguments[0].scrollIntoView(true);", year_btn)
        sleep((random()) / 5)
    year_btn = driver.find_element_by_xpath(f'//span[contains(text(),"{year}")]')
    driver.execute_script("arguments[0].click();", year_btn)
    sleep(random())
    driver.find_element_by_xpath('//div[contains(text(),"+")]').click()
    sleep(random())
    country_field = driver.find_element_by_xpath("//input[@placeholder='Search']")
    for i in range(len(str(country))):
        country_field.send_keys(str(country)[i])
        sleep((random())/8)
    sleep(random())
    country_btn = driver.find_element_by_xpath(f'//span[contains(text(),"{country}")]')
    driver.execute_script("arguments[0].click();", country_btn)
    sleep(random())
    phone_field = driver.find_element_by_xpath("//input[@placeholder='Phone number']")
    for i in range(len(str(phone_number))):
        phone_field.send_keys(str(phone_number)[i])
        sleep((random())/8)
    send_code = driver.find_element_by_xpath('//button[contains(text(), "Send code")]')
    sleep(random())
    driver.execute_script("arguments[0].click();", send_code)
    sleep(random())
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Too many attempts. Try again later.")]'))
        )
    except:
        pass
    else:
        send_code.click()
        sleep(random())
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[contains(text(), "Too many attempts. Try again later.")]'))
            )
        except:
            pass
        else:
            driver.quit()
            return print('Too many attempts. IP is Bad')
    print('Opening Tiktok')

    def verify_captcha(driver):
        i = 0
        while True:
            try:
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//span[contains(text(), "Drag the puzzle piece into place")]'))
                )
                captcha_image = WebDriverWait(driver, 2).until(
                    EC.visibility_of_element_located(
                        (By.ID, 'captcha-verify-image'))
                )
                shigjeta = WebDriverWait(driver, 2).until(
                    EC.visibility_of_element_located(
                        (By.CLASS_NAME, 'secsdk-captcha-drag-icon'))
                )
            except:
                if i == 0:
                    return print('Captcha Not Loaded')
                else:
                    return print('Captcha Verified')
            else:
                image_url = captcha_image.get_attribute('src')
                img_data = requests.get(image_url).content
                length = captcha_solver(img_data)
                action = ActionChains(driver)
                steps = [5 for i in range(int((length / 1.68) / 5))]
                action.move_to_element(shigjeta).click_and_hold().perform()
                for step in steps:
                    action.move_by_offset(step, 0).perform()
                action.pause(0.5).release().perform()
            finally:
                i += 1

    sleep(2)
    verify_captcha(driver)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Too many attempts. Try again later.")]'))
        )
    except:
        print('SUCCESFUL ATTEMPT')
        return print('SUCCESFUL ATTEMPT')
    else:
        driver.quit()
        return print('Too many attempts. IP is Bad')

# profiles = ['617c550407844ccd9d671ed1', '617c5fc5e0ac5b7e525063ad', '617c5fc5e0ac5bb28a5063ac',
# 			'617c5fc5e0ac5ba8255063aa', '617c5fc5e0ac5b9e0d5063a8', '617c5fc5e0ac5b9e0d5063a8',
# 			'617c5fbc179c02549fd4f2bb', '617c5f69e0ac5b1b4b50621c']









profiles = [
    {'profile_id': '61893d54aa8cb0d5aa89eb4e', 'port': 3500},
    {'profile_id': '61893dd1179c02b1b8d5b151', 'port': 3501},
    {'profile_id': '61893dd6e0ac5b2c9c5125b0', 'port': 3502},
    {'profile_id': '61893dd6e0ac5bdcd85125ae', 'port': 3503},
    {'profile_id': '61893dd9179c027792d5b155', 'port': 3503},
    {'profile_id': '61893dda179c020a0ed5b157', 'port': 3503},
    {'profile_id': '61893dda179c028100d5b158', 'port': 3503},
    {'profile_id': '61893dda179c028c93d5b15a', 'port': 3503},
    ]


# with Pool(6) as p:
#     p.map(scrap, profiles)
threads = []
lock = threading.Lock()
for i in range(8):
    prof = profiles[i]
    x = threading.Thread(target=scrap,args=(prof, ))
    x.start()
    threads.append(x)

for x in threads:
    x.join()
if platform == "win32":
    os.system('taskkill /im chrome.exe /f')
    os.system('taskkill /im chromedriver.exe /f')
else:
    os.system('killall -9 chrome')
    os.system('killall -9 chromedriver')

