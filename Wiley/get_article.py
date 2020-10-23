import requests
from bs4 import BeautifulSoup
import re
from science_direct import get_science_direct_link as sd

base_url = 'https://onlinelibrary.wiley.com'

headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko)'
        ' Chrome/80.0.3987.162 Safari/537.36'
}


def get_volume_link(journal_name, url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    div_tags = soup.find_all('div', class_='cover-image__image hasDetails')

    volume_max, year_max = -1, -1

    for div_tag in div_tags:
        year = div_tag.find('a')['href'].split('/')[-3]
        volume = div_tag.find('a')['href'].split('/')[-2]
        year_max, volume_max = max(int(year), year_max), max(int(volume), volume_max)

    journal_code = url.split('/')[-1]

    while year_max != 1995:
        for k in range(1, 15):
            volume_url = base_url + '/toc/' + journal_code + '/' + str(year_max) + '/' + str(volume_max) + '/' + str(k)

            response = requests.get(volume_url, headers=headers)
            print(volume_url, response.status_code)
            if response.status_code == 200:
                with open(sd.handle_journal_name_without_capital(journal_name) + '.txt', "a",
                          encoding='utf-8') as f1:
                    f1.write(volume_url + '\n')

        year_max = year_max - 1
        volume_max = volume_max - 1


def get_article_link(journal_name, url):
    volume_num, issue_num = url.split('/')[-2], url.split('/')[-1]

    print(volume_num, issue_num.replace('\n', ''), journal_name)

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    div_tags = soup('div', class_='card issue-items-container bulkDownloadWrapper')

    for div_tag in div_tags:
        # print(div_tag.find('h3').string == 'Original Articles')
        # if div_tag.find('h3').string == 'Articles' or div_tag.find('h3').string == 'SPECIAL ISSUE ARTICLES' \
        #         or div_tag.find('h3').string == 'Original Articles' or div_tag.find('h3').string == 'Original Article' \
        #         or div_tag.find('h3').string == 'HR Science Forum' or div_tag.find('h3').string == 'Research Articles' \
        #         or div_tag.find('h3').string == 'RESEARCH ARTICLES':
        div_tag2 = div_tag.find_all('div', class_='issue-item')

        for i in range(len(div_tag2)):
            article_url = base_url + div_tag2[i].find('a')['href']
            with open("../resources/txt/Wiley/" + sd.handle_journal_name_without_capital(journal_name) + '.txt',
                      "a", encoding='utf-8') as f2:
                f2.write(article_url + ' Volume' + volume_num + "_Issue" + issue_num)


def get_article(journal_name, journal_code):

    ind = 0

    txt_path = '../resources/txt/Wiley/' + sd.handle_journal_name_without_capital(journal_name) + '.txt'

    with open(txt_path, 'r', encoding='utf-8') as f:
        urls = f.readlines()
        for url in urls:

            article_link, volume, issue = url.split(' ')[0], url.split(' ')[1].split('_')[0], url.split(' ')[1].split('_')[1].replace('\n', '')

            article_path = '../../../../paper data/Wiley/' + journal_name + '/'

            response = requests.get(article_link, headers=headers)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                file_name = journal_code + str(ind) + '_' + volume + '_' + issue + '.txt'
                with open(article_path + file_name, "w", encoding='utf-8') as ff:
                    ind = ind + 1
                    ff.write(response.text)
                    print(journal_name + ' ' + str(ind) + ' ' + article_link)
                    with open('../resources/log/' + journal_name + '.log', "a", encoding='utf-8') as flog:
                        flog.write(article_link + ' ' + "Article_num: " + str(ind) + '\n')

                    flog.close()


if __name__ == "__main__":
    # with open("wiley.txt", "r", encoding='utf-8') as f2:
    #     line = f2.readline()
    #     journal_name, url = line.split('$')[0], line.split('$')[1].replace('\n', '')
    #     print(line.split('$'))
    #     get_volume_link(journal_name, url)
    # with open("wiley.txt", "r", encoding='utf-8') as f3:
    #     lines = f3.readlines()
    #     for line in lines:
    #         name = line.split('$')[0]
    #         path = sd.handle_journal_name_without_capital(line.split('$')[0]) + '.txt'
    #         with open(path, 'r', encoding='utf-8') as f4:
    #             volume_urls = f4.readlines()
    #             for volume_url in volume_urls:
    #                 get_article_link(name, volume_url)

    with open("wiley2.txt", "r", encoding='utf-8') as f3:
        lines = f3.readlines()
        for line in lines:
            journal_name, journal_code = line.split('$')[0], line.split('$')[1].replace('\n', '')

            get_article(journal_name, journal_code)
