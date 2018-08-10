# GoogleParser

#### About project:
  Simple no UI project for parsing google results for specific queries from `.txt` file, writing results into `.tsv` file.
  
  Has the following attributes as parameters of the search query:
  `domain, language, country, number of results` (10-100).
  
#### Files:
  - `MainScraper.py` - main python scipt which includes all the methods and logics of the project.
  - `proxies.txt` - text file which has proxies listed on each line in the format of IP:PORT.
  - `queries.txt` - test file which has search queries for google on each line.
  - `output.tsv` - the file with table separated values, used to write sets of results.
  - `report.txt` - text file showing which requests and queries couldn't been completed due to pause/interruption.
  - `banned_proxies.txt` - text file which includes proxies that were banned or timed out during execution.
  
#### Required modules for the run: 
  `requests, urllib3, bs4, html5, user_agent`

#### Usage:
  - Fill out the above described files (`proxies.txt` and `queries.txt`) with the list of proxies and queries respectively.
  - Set the required attributes (language, region, domain, number of results) in `MainScraper.py` at
  > LINE 77 `'ru', 'ua', 'www.google.com.ua', 100`
  - Set the maximum amount threads to be run at
  > LINE 102 `max_workers=100`
  - Run `MainScraper.py`
  - See the results in `output.tsv` file
  
#### Additional:
  - Use `create_report_file` function in case of any type of interrupted execution to get the list of queries that were not executed (`report.txt`)
  - Check the `banned_proxies.txt` files for the list of proxies that were banned.
