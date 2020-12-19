from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, TimeoutException
import requests
import json
import time
import simplejson
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

email = "ENTER EMAIL ADDRESS"
password = "SYNACK PASSWORD"
proxies = {"http": "http:127.0.0.1:8080", "https": "http://127.0.0.1:8080"} #If you want to enable burp for trouble shooting
totalMissions = []


caps = DesiredCapabilities().FIREFOX
caps["pageLoadStrategy"] = "eager"
caps["acceptInsecureCerts"] = True
caps["acceptUntrustedCerts"] = True




def getMissions(driver, count, missionCount, token):
	while True:
		try:
			validSession = sessionTimeOut(driver)
			if not validSession:
				alert_obj = driver.switch_to.alert
				alert_obj.accept()
				print("Session was not valid but is now!")
			else:
				pass
			count = count + 1
			headers = {"Authorization": "Bearer " + token}
			url = 'https://platform.synack.com/api/tasks/v1/tasks?withHasBeenViewedInfo=true&status=PUBLISHED&page=0&pageSize=20'
			s = requests.Session()

			#resp = s.get(url, verify=False, headers=headers, proxies=proxies) #Enable for Burp access
			resp = s.get(url, verify=False, headers=headers)

			print(resp.status_code)
			print("This is the resp.json()")
			print(resp.json())
			if resp.json():
				print("There are missions!")
				print(resp.json())
				missionCount = missionCount + 1
				data = resp.json()
				tasks = data[0]['id']
				organizations = data[0]['organization']['id']
				listings = data[0]['listing']['id']
				campaigns = data[0]['campaign']['id']
				print("The task id is :" + str(tasks))
				print("The organization id is :" + str(organizations))
				print("The listing id is :" + str(listings))
				print("The campaign id is :" + str(campaigns))


				url2 = 'https://platform.synack.com/api/tasks/v1/organizations/' + str(organizations) + '/listings/' + str(listings) + '/campaigns/' + str(campaigns) + '/tasks/' + str(tasks) + '/transitions'
				#resp2 = s.post(url2, json={"type":"CLAIM"}, verify=False, headers=headers, proxies=proxies)  #Enable for burp trouble shooting
				resp2 = s.post(url2, json={"type":"CLAIM"}, verify=False, headers=headers)


				totalMissions.append(resp.text)
			else:
				print("There are no missions!")
				print(resp.json())


			print("Script has run " + str(count) + " times and " + str(missionCount) + " missions")
			print("")
			print("")
			time.sleep(8)

		except (TimeoutException, simplejson.errors.JSONDecodeError):
			time.sleep(8)
			print("No missions trying again : " + str(count) + " Total missions claimed: " + str(missionCount))


def sessionTimeOut(driver):
	try:
		driver.switch_to.alert
		return False
	except NoAlertPresentException:
		return True



def login():
	count = 0
	missionCount = 0
	driver = webdriver.Firefox(desired_capabilities=caps)
	driver.get("https://login.synack.com/")
	try:
		WebDriverWait(driver, 10).until(EC.title_contains("Login"))

		emailAdd = driver.find_element_by_name('email')
		emailAdd.send_keys(email)

		passwordLogin = driver.find_element_by_name('password')
		passwordLogin.send_keys(password, Keys.ENTER)
		time.sleep(25)
		driver.get("https://platform.synack.com/tasks/user/available")
		token = input("Enter your Authorization token: ")
		getMissions(driver, count, missionCount, token)

	except (NoSuchElementException, TimeoutException):
		return False
	return True

try:
	login()
except KeyboardInterrupt:
	print(totalMissions)
	exit()


