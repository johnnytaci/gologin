import time
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from gologin import GoLogin
from random import randrange,choice
from functions import *

"""
1. install all the requirements on the terminal with:
pip install selenium
pip install imageio
pip install Pillow
pip install numpy
2. Run this file, you can change the number on the variable below.
"""
phone_number = '775000000'
def open_uc(phone_number,headless=False):
	gl = GoLogin({
		'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2MWExNTdkZjAxOTg5MzdmZGFhZGI5NmEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2MWExNTg0YmNjYjU4YWY0MGFiZTM5OTAifQ.8KJlR9hE3JBfhmR26M1aJBvwKMk91SIZcHrAPH2V63Q',
		'profile_id': '61a160fc8eecc3b0bad25c72',
	})
	print(gl.getProfile())
	if platform == "linux" or platform == "linux2":
		chrome_driver_path = "./chromedriver"
	elif platform == "darwin":
		chrome_driver_path = "./mac/chromedriver"
	elif platform == "win32":
		chrome_driver_path = "chromedriver.exe"

	debugger_address = gl.start()
	chrome_options = Options()
	chrome_options.add_experimental_option("debuggerAddress", debugger_address)
	driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
	driver.get("http://tiktok.com/signup")
	date_of_birth= [randrange(1,28),randrange(1,12),randrange(1980,2000)]
	country = 'Iraq'
	WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"Use phone")]'))
	).click()
	WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"When’s your birthday?")]'))
	).click()
	month = choice(
		['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
		 'December'])
	day = str(date_of_birth[0])
	year = str(date_of_birth[2])
	driver.find_element_by_xpath('//div[contains(text(),"Month")]').click()
	driver.find_element_by_xpath(f'//span[contains(text(),"{month}")]').click()
	sleep(0.1)
	driver.find_element_by_xpath('//div[contains(text(),"Day")]').click()
	driver.find_element_by_xpath(f'//span[contains(text(),"{day}")]').click()
	sleep(0.6)
	driver.find_element_by_xpath('//div[contains(text(),"Year")]').click()
	driver.find_element_by_xpath(f'//span[contains(text(),"{year}")]').click()
	sleep(0.4)
	driver.find_element_by_xpath('//div[contains(text(),"+")]').click()
	driver.find_element_by_xpath(f'//span[contains(text(),"{country}")]').click()
	phone_field = driver.find_element_by_xpath("//input[@placeholder='Phone number']")
	phone_field.send_keys(phone_number)
	send_code = driver.find_element_by_xpath('//button[contains(text(), "Send code")]')
	sleep(0.6)
	send_code.click()
	sleep(2)
	try:
		WebDriverWait(driver, 3).until(
			EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Too many attempts. Try again later.")]'))
		)
	except:
		pass
	else:
		send_code.click()
		sleep(2)
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


	verify_captcha(driver)
	too_many = check_for_too_many_attempts(driver)
	if too_many == 'Too many attempts. IP is Bad':
		driver.quit()
		return 'Too many attempts. IP is Bad'

	################################################################################################################################################
	# Wait for resend_code_button to be visible and Try x times to resend the code
	################################################################################################################################################
	api_number = '+994' + phone_number
	number_of_retries = 4
	code = check_code_x_times(driver, api_number, number_of_retries)
	if code == 'Code never arrived':
		driver.quit()
		return 'Code never arrived'
	code_field = WebDriverWait(driver, 10).until(
		EC.visibility_of_element_located(
			(By.XPATH, "//input[@placeholder='Enter 4-digit code']"))
	)

	code_field.send_keys(code)
	WebDriverWait(driver, 2).until_not(
		EC.element_attribute_to_include((By.XPATH, '//button[contains(text(), "Next")]'), "disabled"))
	next_button = driver.find_element_by_xpath('//button[contains(text(), "Next")]')
	sleep(0.5)
	next_button.click()
	try:
		WebDriverWait(driver, 5).until(
			EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Too many attempts. Try again later.")]'))
		)
	except:
		pass
	else:
		sleep(0.2)
		next_button.click()
		try:
			WebDriverWait(driver, 5).until(
				EC.presence_of_element_located(
					(By.XPATH, '//div[contains(text(), "Too many attempts. Try again later.")]'))
			)
		except:
			pass
		else:
			driver.quit()
			print('Too many attempts. IP is Bad')

	################################################################################################################################################
	# Klik next dhe prit faqe tbehet load (Vendos username + pass)
	################################################################################################################################################

	skip_button = WebDriverWait(driver, 10).until(
		EC.visibility_of_element_located(
			(By.XPATH, '//button[contains(text(), "Skip")]'))
	)
	# driver.find_element_by_xpath("//input[@placeholder='Username']").send_keys(username)
	# driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys(password)
	sleep(0.5)
	skip_button.click()
	sleep(10)

	time.sleep(30)

	driver.close()
	time.sleep(3)
	gl.stop()

open_uc(phone_number)
