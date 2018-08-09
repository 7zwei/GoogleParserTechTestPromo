import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from itertools import cycle
from time import sleep
from user_agent import generate_user_agent
import re
import csv


proxies = {
    'https': '80.188.10.50:8080'
}
headers = {'User-Agent': generate_user_agent(device_type="all", navigator=('chrome', 'firefox', 'ie'),
                                             os=('mac', 'linux'))}


def get_single_query_set(search_query, language, region, domain, number_of_results):
    assert isinstance(search_query, str), "Search query must be a string."
    assert isinstance(number_of_results, int) and 10 <= number_of_results <= 100,\
        "Number of results must be an integer in range 10:100."
    assert region.isalpha() and len(region) == 2, "Region must be set with two-letter code (Ex.: 'ru', 'ua', 'uk')"
    assert language.isalpha() and len(language) == 2, "Language must be set with two-letter code " \
                                                      "(Ex.: 'ru', 'ua', 'en')"
    google_search_query = search_query.replace(' ', '+')
    search_url = 'https://{}/search?q={}&num={}&hl={}&gl={}'.format(domain, google_search_query, number_of_results,
                                                                    language, region)
    query_set = [search_query]
    page_response = requests.get(search_url, timeout=5)
    soup = BeautifulSoup(page_response.content, "html5lib")
    for i in soup.findAll("h3", attrs={'class':'r'}):
        query_set.append(i.find('a')['href'].split('=')[1])
    return query_set


def write_into_tsv(query_set):
    with open('output.tsv', 'a') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
        writer.writerow(query_set)


if __name__ == "__main__":
    q = get_single_query_set('dima', 'ru', 'ua', 'www.google.com.ua', 10)
    write_into_tsv(q)
