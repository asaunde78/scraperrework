from selenium import webdriver
import linkdownloadersite
import multiprocessing 

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_binary
import requests
import time
import urllib.parse 


class scraper():
    def __init__(self):
        options = Options()
        options.add_argument('lang=en') 
        options.add_argument('--headless=new') 
        options.add_argument('--no-sandbox')
        options.page_load_strategy = 'none'
        options.add_argument('--disable-dev-shm-usage')
        options.add_extension("scraper/blockerextension.crx")
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-gpu')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.binary_location = "chrome/chrome-linux64/chrome"

        self.driver = webdriver.Chrome(options=options)#"driver",options=options)

        

        
    def get_images(self, search, offset, num):
        
        url = "https://www.google.com/search"

        params = {
            "q":search,
            "tbm": "isch",                # image results
            "hl": "en",                   # language of the search
            "gl": "us",                   # country where search comes from
            "ijn": "0",                   # page number
        }
        query_string = urllib.parse.urlencode(params)

        print("[INFO] Gathering image links")
        address = f"{url}?{query_string}"
        requests.get(f"http://localhost:6969/kill")
        self.driver.get(address)


        print(f"[{offset}] got {address} found {self.driver.title}")
        sT1 = time.time()
        self.driver.add_cookie({"name":"count","value":str(num)})

        try:
            wait = WebDriverWait(self.driver, 6)
            # wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            wait.until(EC.presence_of_element_located((By.CLASS_NAME,"bRMDJf")))
        except:
            print("didn't work")
        highest_index = 0#
        count = 0
        while len(self.driver.find_elements(By.ID, f"DONE")) == 0:
                
            # thumbnails = self.driver.find_elements(By.CLASS_NAME,"bRMDJf")
            thumbnails = self.driver.find_elements(By.CLASS_NAME,"wXeWr")
            
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
                    wait = WebDriverWait(self.driver, 3)
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name))) # looking for image holder
                except:
                    continue
                
                if(len(self.driver.find_elements(By.ID, f"DONE")) > 0):
                    print(f"[{offset}DONE] !!! FOUND A DONE")
                    eD1 = time.time()
                    print(f"finished in {eD1 -sT1}")
                    return
                
                print(f"[IMAGE] {offset} got image {count}/{num}")
                highest_index += 1#*ind
        

class manager():
    def __init__(self):
        self.site = linkdownloadersite.downloader()
        self.scraper = scraper()
    def add(self):
        self.workers.append(scraper())
    def start(self):
        def run_server(s):
            s.run()
        self.ts = multiprocessing.Process(target=run_server,args=(self.site,))
        self.ts.start()
    def getimages(self,search, num):
        self.scraper.get_images(search, 0, num)
    def close(self):
        self.ts.terminate()

if __name__ == "__main__":
    a  = manager()
    a.start()# <- we don't need this 
    a.getimages("rabbit stew", 1)
    # a.getimages("large landscale", 20)
    a.getimages("funny monkey", 50)
    time.sleep(3)
    a.close()