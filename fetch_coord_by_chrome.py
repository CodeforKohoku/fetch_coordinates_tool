import asyncio
import csv
import datetime
import re
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DRIVER_PATH = "c:/driver/chromedriver.exe"   # change to your chrome driver path
ASYNC_LIMIT = 5     # maximal number of asynchronous concurrent IOs
MAX_ADDRESS = 50    # limit the number of addresses to fetch coordinates, None if no limit in need

class MapHandler:
    def __init__(self, driver_path, addrs):
        self.async_mode = True
        self.driver_path = driver_path
        self.url = "https://www.google.co.jp/maps/?hl=ja" # google maps
        self.options = Options()
        self.options.add_argument('--headless')
        self.capability = DesiredCapabilities.CHROME
        self.capability["pageLoadStrategy"] = "none"

        self.addrs = addrs
        self.coords = [] # [[x-cord, y-cord]]
        self.regex = re.compile('@([0-9.]+),([0-9.]+),')
        self.errs = []


    def make_driver(self):
        return webdriver.Chrome(self.driver_path, chrome_options=self.options, desired_capabilities=self.capability)


    def setup_driver_searchbox(self):
        driver = self.make_driver()
        driver.get(self.url)
        try:
            searchbox = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "searchboxinput")))     
            return driver, searchbox  
        except Exception as e:
            raise e


    def run(self):
        if self.async_mode:
            self.async_create_cordinates()
            return

        driver, searchbox = self.setup_driver_searchbox()
        for addr in self.addrs:
            x, y = self.fetch_coord(addr, driver, searchbox)
            self.coords.append([x, y])
        if driver:
            driver.quit()


    def async_create_cordinates(self):
        args = [None] # just placeholder for future any usage
        loop = asyncio.get_event_loop()
        futures = async_run(self.fetch_coord, self.addrs, *args)
        self.coords = loop.run_until_complete(futures)


    def fetch_coord(self, addr, driver=None, searchbox=None):
        if not addr:
            return
        print('fetching coordinates for %s ...' % addr)

        if self.async_mode:
            driver, searchbox = self.setup_driver_searchbox()
        try:
            searchbox.send_keys(addr)
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='searchbox-searchbutton']"))).click()

            if not WebDriverWait(driver, 5).until(EC.url_contains("www.google.co.jp/maps/place/")):
                time.sleep(3) # another wait for browser transition

            m = self.regex.search(driver.current_url)
            if m is None:
                raise Exception('search failed for %s' % addr)

        except Exception as e:
            # raise e
            self.errs.append('{}: {}'.format(addr, e))
            
        finally:
            if self.async_mode and driver:
                driver.quit()

            if 'm' in locals():
                return m.group(1), m.group(2)
            return None, None


async def async_run(func, iters, *args):
    semaphore = asyncio.Semaphore(ASYNC_LIMIT)
    async def async_semaphore(func, *args):
        async with semaphore:
            return await async_executor(func, *args)

    return await asyncio.gather(
        *[async_semaphore(func, item) for item in iters]
    )


async def async_executor(func, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args)


def load_address_list(file_path):
    with open(file_path, encoding="utf-8_sig") as f:
        data = csv.reader(f) # csv reader() doesn't close file yet

        for i, value in enumerate(next(data)):
            if value == 'Add1':
                addrs = [row[i] for row in data if row[i]] # skip empty "" value
                break
    return addrs

def make_csv_file(file_path, matrix):
    with open(file_path, mode='w', encoding="utf-8_sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(matrix)
        # for row in matrix:
        #     w = csv.writerow(row)


def format_unixtime(t, f="%Y%m%d%H%M%S"):
	return datetime.datetime.fromtimestamp(t).strftime(f)


def main():
    start = time.time()

    data_path = sys.argv[1]
    addrs = load_address_list(data_path)

    if MAX_ADDRESS:
        addrs = addrs[:MAX_ADDRESS]
    handler = MapHandler(DRIVER_PATH, addrs)
    handler.run()

    for err in handler.errs:
        print(err)

    matrix = []
    for addr, coord in zip(handler.addrs, handler.coords):
        matrix.append((addr, *coord))
        print(addr, *coord)

    tstamp = format_unixtime(time.time())
    path = '%s_%s.csv' % (data_path.split('.')[0], tstamp)
    make_csv_file(path, matrix)

    print(time.time() - start)

if __name__=='__main__':
    main()
