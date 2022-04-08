from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import time


class Bot:

    def __init__(self):
        # create instance of Chrome webdriver

        # options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')        
        # self.driver = webdriver.Chrome("./driver/chromedriver",chrome_options=options)

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver=webdriver.Chrome("/usr/local/bin/chromedriver", chrome_options=options)

        self.flag=True

    def twitter_login(self, email, password,username="MarketingRns"):
        """
        Gets email and password of the user and logged him in to the twitter
        """
        try:
            # Move to the Twitter login page
            self.driver.get("https://twitter.com/login")
            self.driver.maximize_window()

            # fill the number or mail
            time.sleep(5)
            self.driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[5]/label/div/div[2]/div/input').send_keys(email)
            time.sleep(2)
            # clicking on Next element
            self.driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[6]/div').click()


            if self.check_username_required():
                #entering Username
                time.sleep(5)
                self.driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input').send_keys(username)
                time.sleep(2)
                # clicking on Next element
                self.driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div').click()
                time.sleep(5)


            # fill the password
            time.sleep(5)
            self.driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input').send_keys(password)
            time.sleep(2)            
            # clicking on Login element
            self.driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div').click()
            time.sleep(5)

        except Exception as e:
            self.flag=False
            self.driver.close()
        return self.flag

    def check_username_required(self):
        flag=False
        try:
            time.sleep(3)
            span=self.driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div[1]/span/span')
            if "username" in span.text.lower() or "phone" in span.text.lower():
                flag=True
        except Exception as e:
            print(e)

        return flag

    def post_tweet(self, tweet):
        """
        Gets tweet from the user and post it on the twitter timeline
        """
        try:

            #select text area
            self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div').send_keys(tweet)
            time.sleep(5)
            self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/span/span').click()
            time.sleep(5)

            # close the web browser
            self.driver.close()

        except:
            self.driver.close()
            self.flag=False

        return self.flag


