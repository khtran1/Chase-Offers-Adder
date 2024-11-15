from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import json
from pathlib import Path
import time

def loadCredentialsFromJson():
    accountPath = Path(__file__).resolve().parent / "account.json"

    if not accountPath.exists():
        accountPath.write_text(
            json.dumps(
                {"username": "Your Username", "password": "Your Password"}, indent=4
            ),
            encoding="utf-8",
        )

        noAccountNotice = """
        [ACCOUNT] Account credential file "account.json" not found.
        [ACCOUNT] A new file has been created, please edit with your credentials and save.
        """

        print(noAccountNotice)
        exit()

    credentials = json.loads(accountPath.read_text(encoding="utf-8"))

    return credentials


def login():
    # Locate the username and password fields
    username_field = driver.find_element(By.ID, "userId")
    password_field = driver.find_element(By.ID, "password")

    credentials = loadCredentialsFromJson()

    username_field.send_keys(credentials['username'])
    password_field.send_keys(credentials['password'])

    time.sleep(1)

    login_button = driver.find_element(By.ID, "signin-button")
    login_button.click()

    if waitForElement("validator-error-header", "5"):
        print("Incorrect credentials! Please check account.json and ensure that your information is correct.")
        exit()
    
    print("Login successful!")


def waitForElement(id, timeLimit):
    # Wait for page to load
    try:
        element = WebDriverWait(driver, timeLimit).until(
            EC.presence_of_element_located((By.ID, id))  # Replace with an actual element on the page
        )

        return True
    except:
        return False

if __name__ == "__main__":
    driver = webdriver.Chrome()

    # Open the login page
    driver.get("https://secure.chase.com/web/auth/#/logon/logon/chaseOnline")

    if waitForElement("signin-button", 10):
        login()
    
    