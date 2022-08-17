from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from bs4 import BeautifulSoup
# from sqlalchemy import func
from selenium.webdriver.common.by import By
from fileParse import *

username = "scol0601@csd99.org"
password = "https://2024cc"

url = "https://quizlet.com"

driver = webdriver.Chrome("assets/chromedriver.exe")
driver.implicitly_wait(5)

driver.get(url)

def login():
    # click sign in
    driver.find_element(By.XPATH, "/html/body/div[3]/div/header/div/div[2]/div[3]/button/span").click()

    #click login with google
    driver.find_element(By.XPATH, "/html/body/div[10]/div/div/div[2]/section/div[2]/div/div[2]/div[1]/div/a").click()

    # enter username
    driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input").send_keys(username)
    driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span").click()
    sleep(1)

    #enter password
    driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input").send_keys(password)
    driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span").click()

login()

input("Go to the card deck and press enter when finished.")


try:
    set = driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div[1]/div[2]/div/div[1]/div[2]/div/div/div[2]/section/div/div/div/div[1]/section[1]/div[1]/div/div/div/div/div").get_attribute("outerHTML")
    print("worked!")
except:
    try:
        set = driver.find_element(By.XPATH, "//*").get_attribute("outerHTML")
    except:
        set = list(driver.find_elements(By.CLASS_NAME, "UISection SetPageTerms-termsWrapper SetPage-termsList").get_attribute("outerHTML"))[0]
with open("yee.html", 'w') as file:
    file.write(set)

flashCards = convertDataToDict(set)

print(flashCards)
print()
print()



# flashCards = getFlashCards()