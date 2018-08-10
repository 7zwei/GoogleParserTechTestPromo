import requests
from bs4 import BeautifulSoup
from itertools import cycle
from time import sleep
from user_agent import generate_user_agent
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
from random import uniform
from random import choice
import time


headers = {'User-Agent': generate_user_agent(device_type="all", navigator=('chrome', 'firefox', 'ie'),
                                             os=('mac', 'linux'))}
proxy_list = open('proxies.txt').read().splitlines()


def single_set_processing(search_query, language, region, domain, number_of_results):
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
    soup = BeautifulSoup(make_request(search_url).content, "html5lib")
    for i in soup.findAll("h3", attrs={'class': 'r'}):
        query_set.append(i.find('a')['href'])
    with open('output.tsv', 'a') as tsv_file:
        writer = csv.writer(tsv_file, delimiter='\t', lineterminator='\n')
        writer.writerow(query_set)


def make_request(search_url):
    page_response = requests.get(search_url, proxies={'http': choice(proxy_list)}, headers=headers, timeout=5)
    if check_status_code(page_response.status_code):
        return page_response
    print(page_response.status_code)


def check_status_code(code):
    return code == 200


def run(query):
        single_set_processing(query, 'ru', 'ua', 'www.google.com.ua', 10)
        #sleep(uniform(0.2, 0.5))


def main():
    query_list = open("queries.txt").read().splitlines()
    #query_pool = cycle(query_list)
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(run, query_list)
    print("Execution time:" + time.time() - start_time)


if __name__ == "__main__":
    main()
