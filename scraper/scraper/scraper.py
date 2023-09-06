b="""
Ideas about new project:

use selenium 4 i think 
get everything working like before
try and fix the clicking issue
potentially download the files with the extension? cut out middle man
this would mean the extension and selenium could more directly speak to one another and likely not hinder performance

"""
from selenium import webdriver
import linkdownloadersite
import multiprocessing 
# help(selenium)
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service as ChromeService
#CHROME WGET LINK:
#wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/118.0.5982.0/linux64/chrome-linux64.zip -P chrome
# from selenium.webdriver.firefox.options import Options


# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.core.utils import ChromeType
# from webdriver_manager.firefox import GeckoDriverManager


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_binary
# from selenium.webdriver import ActionChains


import urllib.parse 
import time

search = "dog"
offset = 0
num = 5


options = Options()
# print(options.arguments)
options.add_argument('lang=en') 


options.add_argument('--headless=new') 
    
options.add_argument('--no-sandbox')
options.page_load_strategy = 'none'

options.add_argument('--disable-dev-shm-usage')

options.add_extension("scraper/blockerextension.crx")

options.add_argument('--disable-infobars')
options.add_argument('--disable-gpu')
options.add_experimental_option('excludeSwitches', ['enable-logging'])



# try:
KeyError
options.binary_location = "chrome/chrome-linux64/chrome"

driver = webdriver.Chrome(options=options)#"driver",options=options)

url = "https://www.google.com/search"
a = linkdownloadersite.downloader()
def run_server(s):
    s.run()
ts = multiprocessing.Process(target=run_server,args=(a,))
ts.start()

params = {
    "q":search,
    "tbm": "isch",                # image results
    "hl": "en",                   # language of the search
    "gl": "us",                   # country where search comes from
    "ijn": "0",                    # page number
}

# print(params)

query_string = urllib.parse.urlencode(params)

print("[INFO] Gathering image links")

address = f"{url}?{query_string}"

driver.get(address)
print(f"[{offset}] got {address} found {driver.title}")
driver.add_cookie({"name":"count","value":str(num)})

try:
    wait = WebDriverWait(driver, 6)
    # wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,"bRMDJf")))
except:
    print("didn't work")
highest_index = 0#
count = 5
while len(driver.find_elements(By.ID, f"DONE")) == 0:
        
    thumbnails = driver.find_elements(By.CLASS_NAME,"bRMDJf")
    thumbnails = thumbnails[highest_index:]
    tries = 0
    # thumbnails = thumbnails[highest_index:][::]
    for nail in thumbnails:

        # while tries < self.tries:
        try:
            # print("about to click! so excited")
            nail.click()
            # if self.slower:
            #     time.sleep(1)
            
            # break
        except Exception as e:
            
            print(f"[{offset}-ERROR] failed to click: ", e)
            tries +=1
            if tries == 5:
                print("[ERROR] RAN OUT OF TRIES :/")
            continue
        class_name = "f2By0e"
        # waitstart = time.time()
        count += 1
        try:
            wait = WebDriverWait(driver, 3)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name))) # looking for image holder
        except:
            continue
        
        if(len(driver.find_elements(By.ID, f"DONE")) > 0):
            print(f"[{offset}DONE] !!! FOUND A DONE")
            break 
        
        print(f"[IMAGE] {offset} got image {count}/{num}")
    
        highest_index += 1#*ind

ts.terminate()

