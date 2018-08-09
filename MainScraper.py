import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from itertools import cycle
from time import sleep
from user_agent import generate_user_agent
import re
import csv
from random import uniform
from random import choice
from multiprocessing import Pool
import time

headers = {'User-Agent': generate_user_agent(device_type="all", navigator=('chrome', 'firefox', 'ie'),
                                             os=('mac', 'linux'))}


def write_single_query_set(search_query, language, region, domain, number_of_results):
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
    proxy_list = open('proxies.txt').read().splitlines()
    page_response = requests.get(search_url, proxies={'http': choice(proxy_list)}, headers=headers, timeout=5)
    print(page_response.status_code)
    soup = BeautifulSoup(page_response.content, "html5lib")
    for i in soup.findAll("h3", attrs={'class':'r'}):
        query_set.append(i.find('a')['href'])
    with open('output.tsv', 'a') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
        writer.writerow(query_set)
    return query_set


def run(query):
        write_single_query_set(query, 'ru', 'ua', 'www.google.com.ua', 10)
        sleep(uniform(0.2, 0.5))


if __name__ == "__main__":
    query_list = open("queries.txt").read().splitlines()
    #query_pool = cycle(query_list)
    start_time = time.time()
    with Pool(4) as p:
        p.map(run, query_list)
    print(time.time() - start_time)