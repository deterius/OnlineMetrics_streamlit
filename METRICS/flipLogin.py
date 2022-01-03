

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep






def Flip_Login_Fin_report():
    
   options = webdriver.ChromeOptions() 
   prefs = {"download.default_directory": "/Users/simeonbourim/ML/OnlineMetrics/METRICS/data/flip/downloads", "safebrowsing.enabled":"false"}
   options.add_experimental_option("prefs", prefs)
   # # HEADLESS
   options.add_argument('--headless')
   options.add_argument('window-size=1920x1080');
   options.add_argument("--start-maximized")
   options.add_argument('--ignore-certificate-errors')
   # # END
   driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

   # LOGIN
   driver.get('https://auth.51hchc.com/login')
   sleep(2)
   driver.find_element_by_id('credential-id').send_keys(15821008747)
   driver.find_element_by_id('password').send_keys(2020666888)
   driver.find_element_by_id('hq-code').send_keys('brothers')
   driver.find_element_by_css_selector('form .buttons input[type=\'submit\']').click()
   print('Logged in')
   # GET FINANCIAL REPORT
   sleep(2)
   driver.get('https://console.51hchc.com/financial-report')
   print('Fincial report')
   sleep(2)
   driver.find_element_by_xpath("//*[@id='container']/div/div[2]/form/div[1]/div[2]/label[2]").click()
   sleep(1)
   print('Click 1')
   driver.find_element_by_xpath("//*[@id='container']/div/div[2]/form/div[2]/div[1]/div[2]/select/option[2]").click()
   sleep(2)
   print('Click 2')
   driver.find_element_by_xpath("//*[@id='container']/div/div[2]/form/div[2]/div[2]/button").click()
   sleep(10)
   print('Click 3')
Flip_Login_Fin_report()