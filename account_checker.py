from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sys
import time

username = sys.argv[1]
password = sys.argv[2]

email = username + "@mailinator.com"

options = webdriver.FirefoxOptions()
options.headless = True
options.set_preference("dom.push.enabled", False)
options.set_preference("media.volume_scale", "0.0")

profile = webdriver.FirefoxProfile()
profile.set_preference("security.fileuri.strict_origin_policy", False)
profile.update_preferences()

driver = webdriver.Firefox(options=options, firefox_profile=profile, executable_path="./geckodriver")

try:
    driver.get('https://trovo.live')
except:
    sys.exit(print("error accessing website"))
    driver.quit()

wait = WebDriverWait(driver,30)

time.sleep(3)

try:
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/nav/div[3]/div[3]/button"))).click()
except:
    sys.exit(print("error accessing login"))
    driver.quit()

try:
    email_input = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div[3]/div/div[1]/div/input"))).send_keys(email)
except:
    sys.exit(print("error with email input"))
    driver.quit()

try:
    password_input = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div[3]/div/div[3]/div/input"))).send_keys(password)
except:
    sys.exit(print("error with password input"))
    driver.quit()

try:
    submit_login = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div[3]/div/button"))).click()
except:
    sys.exit(print("error with login submit"))
    driver.quit()

time.sleep(3)

try:
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/nav/div[3]/div[5]"))).click()
    sys.stdout.write(username + " account exists!\n")

    with open("checked_accounts.txt", "a") as myfile:
        myfile.write(username + ":" + password + "\n")
except:
    sys.stdout.write("unable to check " + username + " account :(\n")

driver.quit()
