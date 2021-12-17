from selenium import webdriver
from selenium.webdriver import ChromeOptions
from time import sleep
import pandas as pd
from flask_restful import Resource
from flask import  jsonify
import pandas as pd

import os

def get_flights(orgin, destination, date, adults, children, infants):
    date = date.split('-')
    date = date[-1]+date[1]+date[0]
    date = ''.join(date)
    url = f"https://www.ixigo.com/search/result/flight?from={orgin.upper()}&to={destination.upper()}&date={date}&returnDate=&adults={adults}&children={children}&infants={infants}&class=e&source=Search%20Form"
    print(url)
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument('--headless')
    driver = webdriver.Chrome(
        executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
    driver.maximize_window()
    driver.get(url)
    sleep(2)
    total_items = []
    pages = driver.find_element_by_class_name('c-pagination') 
    all_pages = pages.find_elements_by_xpath('.//span[@class = "page-num"]')
    for page in all_pages:
        cards = driver.find_elements_by_class_name('c-flight-listing-row-v2')
        for card in cards:
            k = {}
            fight_img = card.find_element_by_xpath('.//div[@class = "logo"]').find_element_by_tag_name('img').get_attribute('src')
            fight_name = card.find_element_by_xpath('.//a[@class = "flight-name"]').text
            orgin_details = card.find_element_by_class_name('left-wing')
            orgin_code = orgin_details.find_element_by_class_name('airport-code').text
            orgin_date = orgin_details.find_element_by_class_name('date').text
            orgin_time = orgin_details.find_element_by_class_name('time').text
            orgin_city = orgin_details.find_element_by_xpath('.//div[4]').text
            ####
            destination_details = card.find_element_by_class_name('right-wing')
            dest_code = destination_details.find_element_by_class_name('airport-code').text
            dest_date = destination_details.find_element_by_class_name('date').text
            dest_time = destination_details.find_element_by_class_name('time').text
            dest_city = destination_details.find_element_by_xpath('.//div[4]').text
            ####
            duration_stops_div = card.find_element_by_class_name('flight-summary')
            duration_of_flight = duration_stops_div.find_element_by_xpath('.//div[2]//div[1]//div[2]').text
            duration_stops = duration_stops_div.find_element_by_xpath('.//div[2]//div[1]//div[6]').text

            flight_price = card.find_element_by_class_name('price-section').text
            discount_credit = card.find_element_by_class_name('dynot').text
            k['fight_img']  = fight_img 
            k['fight_name'] = fight_name
            k['orgin_code'] = orgin_code 
            k['orgin_date'] = orgin_date 
            k['orgin_time'] = orgin_time
            k['orgin_city'] = orgin_city
            k['dest_code']  = dest_code
            k['dest_date']  = dest_date
            k['dest_time']  = dest_time
            k['dest_city']  = dest_city
            k['duration_of_flight'] = duration_of_flight
            k['duration_stops'] = duration_stops
            k['flight_price'] = flight_price
            k['discount_credit'] = discount_credit
            total_items.append(k)
        sleep(2)
        page.click()
    data = pd.DataFrame(total_items)
    driver.close()
    return [data.T.to_dict()[i] for i in data.T.to_dict()]


class GetFlights(Resource):
    def get(self, orgin, destination, date, adults, children, infants):
        data = get_flights(orgin, destination, date, adults, children, infants)
        return jsonify({'data': data})
