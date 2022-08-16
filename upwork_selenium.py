from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time

options = Options()

options.headless = False

proxy_ip_port = '127.0.0.1:5566'
proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.httpProxy = proxy_ip_port
proxy.sslProxy = proxy_ip_port


capabilities = webdriver.DesiredCapabilities.CHROME
proxy.add_to_capabilities(capabilities)

driver = webdriver.Chrome("/usr/bin/chromedriver", options=options, desired_capabilities=capabilities)

driver = uc.Chrome(use_subprocess=True)
driver.get("https://www.upwork.com/nx/jobs/search/?q=airflow&sort=recency")
time.sleep(10)
# link = driver.find_element("xpath", "//h4[@class='my-0.p-sm-right.job-tile-title']")
# print(link)
# continue_link = driver.find_element(By.LINK_TEXT, 'Next')
title = driver.find_elements(By.CLASS_NAME, "my-0.p-sm-right.job-tile-title")
links = driver.find_elements(By.CSS_SELECTOR, "h4>a")
for link in links:
    link = link.get_attribute('href')
    print(link)
    # driver.get(link)
    # print(driver.title)

# def parse():
#     title = link.find_elements(By.CLASS_NAME, "my-0.mr-10.display-rebrand")
#     desc = link.find_elements(By.CLASS_NAME, "job-description.break.mb-0")


# print(driver.page_source)
with open('items.txt', 'w') as f:
    f.write(driver.page_source)


driver.quit()
