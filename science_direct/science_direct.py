from bs4 import BeautifulSoup
import requests
from lxml import etree

base_url = 'https://www.sciencedirect.com'


def get_paper_link(url, journal_name):
    headers = {
        'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko)'
            ' Chrome/80.0.3987.162 Safari/537.36'
    }

    re = requests.get(url, headers=headers)
    soup = BeautifulSoup(re.text, 'html.parser')

    url_lists = soup.find_all('a', class_='result-list-title-link u-font-serif text-s')

    for url_list in url_lists:
        real_url = base_url + url_list['href']
        with open(journal_name + '.txt', "a", encoding='utf-8') as f:
            f.write(real_url + '\n')


def science_direct(journal_name):
    url = base_url + "/search?pub=" + journal_name + "&show=100"
    get_paper_link(url, journal_name=journal_name)

    for i in range(1, 18):
        url = base_url + "/search?pub=" + journal_name + "&show=100&offset=" + str(i * 100)
        get_paper_link(url, journal_name=journal_name)


if __name__ == '__main__':
    science_direct("Journal of Operations Management")


import requests

save_dir = "/home/zyz/paper_data/FT50"


def down_source_code():
    headers = {
        'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko)'
            ' Chrome/80.0.3987.162 Safari/537.36'
    }

    ind = 1806

    with open("/home/zyz/paper_data/Organizational_Behavior_and_Human_Decision_Processes.txt", "r", encoding='utf-8') as f:
        urls = f.readlines()
        for url in urls:
            re = requests.get(url, headers=headers)
            re.encoding = 'utf-8'
            with open("/home/zyz/paper_data/FT50/Organizational Behavior and Human Decision Processes/obhdp{}.html".format(str(ind)), "w",
                      encoding='utf-8') as f2:
                f2.write(re.text)
                if re.text != "":
                    with open("/home/zyz/paper_data/log/Organizational_Behavior_and_Human_Decision_Processes.log", "a", encoding='utf-8') as f3:
                        f3.write(url)
                    f3.close()
                ind = ind + 1
            f2.close()


if __name__ == '__main__':
    down_source_code()

