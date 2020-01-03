

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import time

options = Options()
browser = None
wait = None


class WebdriverLogFacade(object):

    last_timestamp = 0

    def __init__(self, webdriver):
        self._webdriver = webdriver

    def get_log(self):
        last_timestamp = self.last_timestamp
        entries = self._webdriver.get_log("browser")
        filtered = []

        for entry in entries:
            # check the logged timestamp against the
            # stored timestamp
            if entry["timestamp"] > self.last_timestamp:
                filtered.append(entry)

                # save the last timestamp only if newer
                # in this set of logs
                if entry["timestamp"] > last_timestamp:
                    last_timestamp = entry["timestamp"]

        # store the very last timestamp
        self.last_timestamp = last_timestamp

        return filtered


def connect():
    global browser
    global wait
    # PROVJERA VERZIJA CROME DRIVERA
    try:
        CHROMEDRIVER_PATH = ChromeDriverManager().install()
    except Exception:
        return "Neuspješno osvježavanje drajvera. Provjerite vašu internet konekciju."

    profile = webdriver.CromeProfile()
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)
    profile.set_preference("network.http.use-cache", False)

    browser = webdriver.Chrome(
        CHROMEDRIVER_PATH, options=options, profile=profile)

    wait = WebDriverWait(browser, 10)
    browser.get("http://"+"192.168.100.1"+"/")

    try:
        assert "HG8245H" in browser.page_source
    except AssertionError:
        return "Niste na HG8245H ruteru, ili provjerite gateway IP adresu."

    # ovaj dole try je potreban ako se kacimo na H5 a greskom izaberemo H router. pa ce
    # prvi assert proci, posto je  "HG8245H" in "HG8245H5"
    try:
        username = wait.until(
            EC.presence_of_element_located((By.ID, "txt_Username")))

        username.send_keys("telecomadmin")

        password = wait.until(
            EC.presence_of_element_located((By.ID, "txt_Password")))

        password.send_keys("admintelecom")

        login = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="button"]')))

        login.click()

    except Exception:
        return "Niste na HG8245H ruteru, ili provjerite gateway IP adresu."

    try:
        assert "Incorrect account/password combination. Please try again." not in browser.page_source
    except AssertionError:
        return "Neispravna kombinacija korisničko ime/šifra. Pokušajte ponovo."

    # PROVJERA VERZIJE SOFTVERA NA MODEMU
    wait.until(
        EC.frame_to_be_available_and_switch_to_it('frameContent'))

    try:
        assert "V3R017C10S122" in browser.page_source
        return "KONEKCIJA USPOSTAVLJENA"
    except AssertionError:
        pass
    try:
        assert "V3R015C10S150" in browser.page_source
        return "KONEKCIJA USPOSTAVLJENA"
    except AssertionError:
        pass

    return "NEPODRZANA SOFTVERSKA VERZIJA"


def getWlanInfo():
    global browser
    global wait
    browser.switch_to_default_content()
    try:
        wlaninfo = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="nav"]/ul/li[3]')))
        wlaninfo.click()

        wait.until(
            EC.frame_to_be_available_and_switch_to_it('frameContent'))

        html_down = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[3]/table[1]/tbody/tr[3]/td[8]")))
        novibajt_down = int(
            html_down.get_attribute("innerHTML").split("&")[0])
        print("novibajt_down: ", novibajt_down)

        html_up = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[3]/table[1]/tbody/tr[3]/td[3]")))
        novibajt_up = int(
            html_up.get_attribute("innerHTML").split("&")[0])
        print("novibajt_up: ", novibajt_up)

    except (TimeoutException, StaleElementReferenceException) as e:
        print("Error", "Timeout Error ocured.\n " + str(e))

    return


connect()
#log_facade = WebdriverLogFacade(browser)
#logs = log_facade.get_log()

while True:
    time.sleep(4)
    getWlanInfo()
    #logs = log_facade.get_log()
    # print(logs)
