import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from itertools import cycle
from time import sleep


proxies = {
    'https': '80.188.10.50:8080'
}
proxy_pool = cycle(proxies)


def get_search_url(search_query, language, region, domain, number_of_results):
    assert isinstance(search_query, str), "Search query must be a string."
    assert isinstance(number_of_results, int) and 10 <= number_of_results <= 100,\
        "Number of results must be an integer in range 10:100."
    assert region.isalpha() and len(region) == 2, "Region must be set with two-letter code (Ex.: 'ru', 'ua', 'uk')"
    assert language.isalpha() and len(language) == 2, "Language must be set with two-letter code " \
                                                      "(Ex.: 'ru', 'ua', 'en')"
    google_search_query = search_query.replace(' ', '+')
    search_url = 'https://{}/search?q={}&num={}&hl={}&gl={}'.format(domain, google_search_query, number_of_results,
                                                                    language, region)
    return search_url


def fetch_results(search_url):
    driver = webdriver.Chrome()
    driver.get(search_url)
    sleep(100)
    driver.find_element_by_xpath('//*[@id="rso"]/div[2]/div/div[2]/div/div/h3/a')
    #"//*[@id="rso"]/div[4]/div/div[19]/div/div/h3/a"
    #"//*[@id="rso"]/div[4]/div/div[11]/div/div/h3/a"
    #"//*[@id="rso"]/div[2]/div/div[1]/div/div/h3/a"
    #"//*[@id="rso"]/div[2]/div/div[2]/div/div/h3/a"
    #"//*[@id="rso"]/div[4]/div/div[44]/div/div/h3/a"


def test_proxies():
    for i in range(0,10):
        proxy = next(proxy_pool)
        print("request #%d"%i)
        try:
            response = requests.get("https://www.google.com.ua/search?q=sanya", proxies={"http": proxy, "https": proxy})
            print(response.json())
        except:
            print("Sss")


if __name__ == "__main__":
    fetch_results(get_search_url('sanya beliy', 'ru', 'ua', 'www.google.com.ua', 50))