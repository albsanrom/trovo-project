from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from twocaptcha import TwoCaptcha
import sys
import time

username = sys.argv[1]
password = sys.argv[2]

email = username + "@mailinator.com"
birth_day = "17"
birth_year = "1990"

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

sys.stdout.write("accessing https://trovo.live...\n")
sys.stdout.flush()

wait = WebDriverWait(driver,20)

sys.stdout.write("creating " + username + " account...\n")
sys.stdout.flush()

time.sleep(3)

try:
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/nav/div[3]/div[3]/button"))).click()
except:
    sys.exit(print("error accessing login"))
    driver.quit()

try:
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div[3]/div/ul/li[2]"))).click()
except:
    sys.exit(print("error accessing signup"))
    driver.quit()

try:
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div[3]/div/div[1]/div/input"))).send_keys(email)
except:
    sys.exit(print("error with email input"))
    driver.quit()

try:
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div[3]/div/div[2]/div/input"))).send_keys(username)
except:
    sys.exit(print("error with username input"))
    driver.quit()

try:
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div[3]/div/div[3]/div/input"))).send_keys(password)
except:
    sys.exit(print("error with password input"))
    driver.quit()

try:
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div[3]/div/div[4]/div[1]/div[1]/div[1]"))).click()
except:
    sys.exit(print("error scrolling month"))
    driver.quit()

try:
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div[3]/div/div[4]/div[1]/div[1]/div[2]/ul/li[1]/span"))).click()
except:
    sys.exit("error clicking on January")
    driver.quit()

try:
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div[3]/div/div[4]/div[1]/div[2]/div[1]/input"))).send_keys(birth_day)
except:
    sys.exit("error with day input")
    driver.quit()

try:
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div[3]/div/div[4]/div[1]/div[3]/div[1]/input"))).send_keys(birth_year)
except:
    sys.exit("error with year input")
    driver.quit()

try:
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div[3]/div/button"))).click()
except:
    sys.exit("error with signup submit")
    driver.quit()

sys.stdout.write("waiting for captcha to be solved...\n")
sys.stdout.flush()

solver = TwoCaptcha('bf715cc7989429f5f43a6b948d2cc496')
result = solver.recaptcha(sitekey='6LfjEMoUAAAAAPv60USWs4LxOlTmoiGf7m2skV4O',
                          url='https://trovo.live')

TOKEN = result['code']

try:
    driver.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="";')
    driver.execute_script("""
      document.getElementById("g-recaptcha-response").innerHTML = arguments[0]
    """, TOKEN)
    driver.execute_script('___grecaptcha_cfg.clients[0].V.V.callback("{}")'.format(TOKEN))
except:
    sys.exit("error resolving captcha")
    driver.quit()

options_again = webdriver.FirefoxOptions()
options_again.headless = True
options_again.set_preference("dom.push.enabled", False)
options_again.set_preference("media.volume_scale", "0.0")

profile_again = webdriver.FirefoxProfile()
profile_again.set_preference("security.fileuri.strict_origin_policy", False)
profile_again.update_preferences()

mailinator = webdriver.Firefox(options=options_again, firefox_profile=profile_again, executable_path="./geckodriver")

try:
    mailinator.get('https://www.mailinator.com/v3/index.jsp?zone=public&query=' + username)
except:
    sys.exit(print("error accessing mail service"))
    mailinator.quit()
    driver.quit()

wait_again = WebDriverWait(mailinator,20)

sys.stdout.write("confirming account...\n")
sys.stdout.flush()

time.sleep(5)

try:
    wait_again.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[3]/div/div[5]/div/div/div/table/tbody/tr/td[3]"))).click()
except:
    sys.exit(print("error with clicking mail"))
    mailinator.quit()
    driver.quit()

time.sleep(2)

mailinator.switch_to.frame("msg_body")

confirmation_code = mailinator.find_element_by_class_name('size-36').text
input_confirmation = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div[3]/div/div/div[2]/div[1]/ul/li[1]")))
ActionChains(driver).move_to_element(input_confirmation).click().perform()
ActionChains(driver).move_to_element(input_confirmation).send_keys(confirmation_code).perform()

mailinator.quit()

time.sleep(3)

sys.stdout.write("account " + username + " with password " + password + " created!\n")

with open("created_accounts.txt", "a") as myfile:
    myfile.write(username + ":" + password + "\n")

driver.quit()
