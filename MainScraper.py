import requests
from bs4 import BeautifulSoup
from itertools import cycle
from time import sleep
from user_agent import generate_user_agent
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import csv
from random import uniform
from random import choice
import time


# Using user_agent module to generate a random user_agent
headers = {'User-Agent': generate_user_agent(device_type="all", navigator=('chrome', 'firefox', 'ie'),
                                             os=('mac', 'linux'))}
# Building a list of proxies from the 'proxies.txt' files
proxy_list = open('proxies.txt').read().splitlines()


# The function takes search parameters for a single query, builds a google query,
# makes request, completes the set of 'query: results' and writes the set into the .tsv file
def single_set_processing(search_query, language, region, domain, number_of_results):
    # Assert restrictions for the arguments
    assert isinstance(search_query, str), "Search query must be a string."
    assert isinstance(number_of_results, int) and 10 <= number_of_results <= 100,\
        "Number of results must be an integer in range 10:100."
    assert region.isalpha() and len(region) == 2, "Region must be set with two-letter code (Ex.: 'ru', 'ua', 'uk')"
    assert language.isalpha() and len(language) == 2, "Language must be set with two-letter code " \
                                                      "(Ex.: 'ru', 'ua', 'en')"
    google_search_query = search_query.replace(' ', '+')
    search_url = 'https://{}/search?q={}&num={}&hl={}&gl={}'.format(domain, google_search_query, number_of_results,
                                                                    language, region)
    # Creating a list, filling the 0 cell with the search query and will add results on top of it
    query_set = [search_query]
    soup = BeautifulSoup(make_request(search_url).content, "html5lib")
    for i in soup.findAll("h3", attrs={'class': 'r'}):
        # Adding results into list, building set
        query_set.append(i.find('a')['href'])
    # Writing a single set into .tsv file
    with open('output.tsv', 'a') as tsv_file:
        writer = csv.writer(tsv_file, delimiter='\t', lineterminator='\n')
        writer.writerow(query_set)


# Simple func to make a request by search URL, uses random proxies from file and headers from user agent module
# Return the response from the request if the request was successful, status code 200
def make_request(search_url):
    current_proxy = {'http': choice(proxy_list)}
    page_response = requests.get(search_url, proxies=current_proxy, headers=headers, timeout=5)
    if check_status_code(page_response.status_code):
        return page_response
    else:
        # Handling banned proxies
        add_banned_proxy(current_proxy)
        return


# Simple func to check if request was successful and status code is 200
# Returns bool: True if status_code == 200
def check_status_code(code):
    return code == 200


# Create a list of banned proxies for handling
def add_banned_proxy(proxy):
    with open('banned_proxies.txt', 'a') as a:
        a.write("%s\n" % proxy)


# The function which is used to set the parameters of execution
# Automatically takes the first argument 'query' from a list of queries (queries.txt)
# Arguments to set: language, region, domain, number of results to show
def run(query):
        single_set_processing(query, 'ru', 'ua', 'www.google.com.ua', 100)
        # I was using some delays for not getting banned using free proxies
        sleep(uniform(0.2, 0.5))


# Create a file with a report about queries which were not executed
def create_report_file(queries_file, completed_queries_file, report_file):
    queries_list = open(queries_file).read().splitlines()
    completed_queries = []
    with open(completed_queries_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            completed_queries.append(row[0].split('\t')[0])
    queries_left = list(set(queries_list) - set(completed_queries))
    with open(report_file, 'w') as w:
        for item in queries_left:
            w.write("%s\n" % item)

# The function to build the query list and map with 'run' function inside the ThreadPoolExecutor
# Here is the argument to set is 'max_workers', the number of threads to be executed
def main():
    queries_list = open("queries.txt").read().splitlines()
    #query_pool = cycle(query_list)
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(run, queries_list)


    # Tracking execution time for tests
    print(time.time() - start_time)


if __name__ == "__main__":
    #create_report_file('queries.txt', 'output.tsv', 'report.txt')
    main()
