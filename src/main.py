# from selenium.webdriver import Firefox
from seleniumwire.webdriver import Firefox # https://pypi.org/project/selenium-wire/
from seleniumwire.utils import decode
import time
import json
import csv

class Scrape:
    def __init__(self):
        """
        """
        self.LOAD_MORE = '/html/body/div[1]/div[2]/div[3]/div[4]/div/div/div[2]/div/button'
        self.SEE_PROMO = '/html/body/div[1]/div[2]/div[3]/div[5]/div[1]/div/button'
        self.executable_path=r'C:\Users\0x6f736f646f\Downloads\geckodriver-v0.30.0-win64\geckodriver.exe'
        self.url = 'https://food.grab.com/ph/en/'
        self.contained_url = "https://portal.grab.com/foodweb/v2/"
        self.loadmore = True
        self.data = []
        self.columntitles = ['name', 'latitude', 'longitude']
        self.filename = "anakindata.csv"
        print("INFO: Starting Firefox")
        self.driver = Firefox(executable_path = self.executable_path)
        time.sleep(60)


    def change_location(self):
        """"
        Changes location from where the request is being made from
        Not being used since it was resulting in some error
        """
        self.latitude = 1.290270
        self.longitude = 103.851959
        self.accuracy = 100
        driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "accuracy": self.accuracy
            })
    
    def load_promotions(self):
        """
        Loads promotion by clicking the promotions button.
        It finds the button by searching the xpath
        """
        print("INFO: Clicking the see promotions button")        
        self.driver.get(self.url)
        time.sleep(60)
        promo = self.driver.find_element_by_xpath(self.SEE_PROMO)
        promo.click()
        time.sleep(60)

    def load_more(self):
        """
        Continually clicks the load more button until they finish
        It finds the button by searching the xpath
        """
        print("INFO: Loading more")
        while self.loadmore is True:
            try:
                loadMoreButton = self.driver.find_element_by_xpath(self.LOAD_MORE)
                loadMoreButton.click()
                time.sleep(30)
            except:
                print("INFO: No more load more buttons")
                self.loadmore = False

    
    def get_location(self):
        """
        Get the geo location of each hospital
        it looks out for this "https://portal.grab.com/foodweb/v2/category?latlng=14.5995,120.9842&categoryShortcutID=305&searchID=&offset=94&pageSize=32" request
        """
        print("INFO: Getting geolocation data")
        for request in self.driver.requests:
            if request.response:
                if request.url.__contains__(self.contained_url):
                    try:
                        body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'gzip'))
                        body = json.loads(body)
                        for i in range(0, len(body['searchResult']['searchMerchants']),1):
                            latitude = body['searchResult']['searchMerchants'][i]['latlng']['latitude']
                            longitude = body['searchResult']['searchMerchants'][i]['latlng']['longitude']
                            name = body['searchResult']['searchMerchants'][i]['chainID']
                            self.data.append({"name": name, "latitude": latitude, "longitude": longitude})
                    except KeyError as e:
                        print(e)
    
    def write_csv(self):
        """
        Writes to csv
        Takes the data that was generated and writes to csv
        """
        print("INFO: Writing to {}".format(self.filename))
        with open(self.filename, 'w') as csvfile: 
            # creating a csv dict writer object 
            writer = csv.DictWriter(csvfile, fieldnames = self.columntitles) 
            # writing headers (field names) 
            writer.writeheader() 
            # writing data rows 
            writer.writerows(self.data) 

    def run(self):
        """
        Runs the scraping process. Starts wih loading ptromotiosn the loading more
        """
        self.load_promotions()
        self.load_more()
        self.get_location()
        self.write_csv()

if __name__ == "__main__":
    scrape = Scrape()
    scrape.run() 
