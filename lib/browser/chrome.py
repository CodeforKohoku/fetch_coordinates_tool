import re
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import settings as C
import lib.utils as utils
from .base import BaseDriver
from ..decorator.chrome import *

__all__ = [
    "ChromeDriver"
]


COORD_REGEX = re.compile('@([0-9.]+),([0-9.]+),').search

class ChromeDriver(BaseDriver):

    def __init__(self):
        super().__init__()
        self._drivers = []

        if C.VISUAL_CHECK:
            self.options = None
            self.capability = None
        else:
            self.options = Options()
            self.options.add_argument('--headless')
            self.capability = DesiredCapabilities.CHROME
            self.capability["pageLoadStrategy"] = "none"
            self.async_mode = C.ASYNC_MODE


    def __del__(self):
        for driver in self._drivers:
            try:
                driver.quit()
            except:
                pass


    def new_driver(self):
        self._drivers.append(
            webdriver.Chrome(C.CHROME_DRIVER_PATH,
            chrome_options=self.options, desired_capabilities=self.capability))

        return self._drivers[-1]


    def run_adds(self):
        driver    = self.new_driver()
        searchbox = new_searchbox(driver)

        for add in self._adds:

            self._coords.append(
                self.fetch_coord(add, driver, searchbox)) # (x, y)

            if not C.VISUAL_CHECK:
                searchbox.clear()
                # time.sleep(1)
                continue
            
            if len(driver.window_handles) >= C.MAX_TAB_NUM:
                print(f'waiting for the window tabs to be less than { C.MAX_TAB_NUM }')
                driver_wait(driver)

            searchbox = newtab_searchbox(driver)


    # decorator not allowed as passed to async function
    def async_fetch_coord(self, add):
        assert isinstance(add, str)

        driver = self.new_driver()
        x, y = self.fetch_coord(add, driver, new_searchbox(driver))

        try: driver.quit()
        except: pass

        return x, y


    @deco_fetch_coord
    def fetch_coord(self, add, driver, searchbox):
        assert isinstance(add, str)
        assert isinstance(driver, WebDriver)
        assert isinstance(searchbox, WebElement)

        searchbox.send_keys(add)
        m = fetch_coord_regex(driver)

        if m:
            return m.group(1), m.group(2)

        return None, None
            

def driver_wait(driver):
    assert isinstance(driver, WebDriver)

    try:
        WebDriverWait(driver, 10).until(
            EC.number_of_windows_to_be(C.MAX_TAB_NUM - 1))

    except exceptions.TimeoutException:
        driver_wait(driver)


def newtab_searchbox(driver):
    assert isinstance(driver, WebDriver)

    try:
        driver.execute_script("window.open()")

    except exceptions.NoSuchWindowException: # when browser tab has been deleted
        driver.switch_to.window(driver.window_handles[-1])
        driver.execute_script("window.open()")

    driver.switch_to.window(driver.window_handles[-1])
    return new_searchbox(driver)


@deco_new_searchbox
def new_searchbox(driver):
    assert isinstance(driver, WebDriver)

    driver.get(C.MAP_URL)

    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "searchboxinput")))     


def fetch_coord_regex(driver):
    assert isinstance(driver, WebDriver)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='searchbox-searchbutton']"))).click()

    if not WebDriverWait(driver, 10).until(
        EC.url_contains("www.google.co.jp/maps/place/")):
        time.sleep(3) # another wait for browser transition

    return COORD_REGEX(driver.current_url)
