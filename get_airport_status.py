from flask.json import jsonify
from flask_restful import Resource
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import pandas as pd


def get_details(link):
    options = ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome('chromedriver.exe',options=options)
    driver.maximize_window()
    driver.get(link)
    status = driver.find_element_by_class_name('row')
    driver.close()
    return status.text.split('\n')


def get_board():
    options = ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome('chromedriver.exe',options=options)
    driver.maximize_window()
    driver.get('https://www.bangaloreairport.com/kempegowda-departures')
    items = driver.find_elements_by_xpath('.//div[@class = "flight-row"]')
    data = []
    for item in items:
        try:
            k = {}
            k['departure'] = item.find_element_by_xpath('.//div[1]').text
            k['time'] = item.find_element_by_xpath('.//div[2]//div[1]').text
            k['flight'] = item.find_element_by_xpath('.//div[2]//div[2]').text
            k['airline'] = item.find_element_by_xpath('.//div[2]//div[3]').text
            k['info_url'] = item.find_element_by_xpath('.//div[2]').find_element_by_tag_name('a').get_attribute('href')
            k['status'] = item.find_element_by_xpath('.//div[contains(@class ,"flight-col flight-col__status")]').text
            data.append(k)
        except:
            pass
    df = pd.DataFrame(data)
    driver.close()
    return [df.T.to_dict()[i] for i in df.T.to_dict()]

class GetAirportBorad(Resource):
    def get(self):
        data = get_board()
        return jsonify({'data':data})
class GetDetailStatus(Resource):
    def get(self,link):
        data = get_details(link)
        return jsonify({"data":data})







    







