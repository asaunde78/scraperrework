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
        '''
        Hi
        '''
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

    def get_images(self, search: str, num: int, offset: int=0, clear: bool = False) -> None:
        
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
        if(clear):
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
            thumbnails = self.driver.find_elements(By.CLASS_NAME,"wXeWr")
            thumbnails = thumbnails[highest_index:]
            tries = 0
            for nail in thumbnails:
                try:
                    nail.click()
                
                except Exception as e:
                    
                    print(f"[{offset}-ERROR] failed to click: ", e)
                    tries +=1
                    if tries == 5:
                        print("[ERROR] RAN OUT OF TRIES :/")
                    continue
                
                count += 1
                
                
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
        self.scraper.get_images(search, num, 10,clear=True)
    def close(self):
        self.ts.terminate()

if __name__ == "__main__":
    a  = manager()
    a.start()# <- we don't need this 
    a.getimages("rabbit stew", 1)
    # a.getimages("large landscale", 20)
    a.getimages("nature landscape", 50)
    time.sleep(3)
    a.close()