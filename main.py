import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

response = requests.get("https://www.trulia.com/for_sale/Honolulu,HI/3p_beds/0-1500000_price/SINGLE-FAMILY_HOME_type/",
                        headers={
                            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0",
                            "Accept-Language": "en-US,en;q=0.5"})
trulia = response.text

soup = BeautifulSoup(trulia, "html.parser")
listing_link = soup.find_all(class_="PropertyCard__StyledLink-m1ur0x-3 dgzfOv", href=True)
all_listing_links = []

for links in listing_link:
    link = links["href"]
    if "http" not in link:
        all_listing_links.append(f"https://www.trulia.com{link}")
    else:
        all_listing_links.append(link)

print(all_listing_links)

listing_price = soup.find_all(class_="Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 keMYfJ")
all_listing_prices = []
for prices in listing_price:
    price = prices.getText()
    all_listing_prices.append(price)

print(all_listing_prices)

listing_address = soup.find_all(class_="Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 dZyoXR")
all_listing_addresses = []
for addresses in listing_address:
    address = addresses.getText()
    all_listing_addresses.append(address)
    new_addresses = all_listing_addresses[1::2]

print(new_addresses)

service = Service("/Users/bean/Development/chromedriver")
driver = webdriver.Chrome(service=service)

for i in range(len(all_listing_links)):

    driver.get('https://docs.google.com/forms/d/e/1FAIpQLSenm_pDkbbrJ7UDNmx0TBmL7t3h8l-hj6pd08VqYOYoUgNqtA/viewform?usp=sf_link')
    time.sleep(2)
    address = driver.find_element(by=By.XPATH, value="/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
    price = driver.find_element(by=By.XPATH, value="/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")
    link = driver.find_element(by=By.XPATH, value="/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")
    submit_button = driver.find_element(by=By.XPATH, value="/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span/span")

    address.clear()
    address.send_keys(new_addresses[i])

    price.clear()
    price.send_keys(all_listing_prices[i])

    link.clear()
    link.send_keys(all_listing_links[i])

    submit_button.click()



