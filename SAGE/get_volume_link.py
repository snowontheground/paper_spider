import requests
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from bs4 import BeautifulSoup
from science_direct import get_science_direct_link as sd

base_url = "https://journals.sagepub.com"

journal_code = {
    "Entrepreneurship Theory and Practice": "etpd",
    "Human Relations": "huma",
    "Journal of Management": "jom",
    "Journal of Marketing": "jmxa",
    "Journal of Marketing Research": "mrja",
    "Journal of the Academy of Marketing Science": "jams",
    "Organization Studies": "oss"
}


def get_volume_link(journal_name):

    url = 'https://journals.sagepub.com/loi/etpb?%20-%20201918&expanded=2017&expanded=2016&expanded=2015&expanded=2014&expanded=2013&expanded=2012&expanded=2011%20-%202009&expanded=2008&expanded=2007&expanded=2006&expanded=2005&expanded=2004&expanded=2003&expanded=2002&expanded=2001&expanded=26&expanded=25&expanded=24&expanded=1990%20-%201999&expanded=1998&expanded=1997&expanded=1996&expanded=22&expanded=28'

    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko)'
            ' Chrome/80.0.3987.162 Safari/537.36'
    }

    ind = 1
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    volume_links = soup.find_all('a', class_='issue-link h6')

    for volume_link in volume_links:
        print(base_url + volume_link['href'])

    for volume_link in volume_links:
        volume_url = base_url + volume_link['href']
        try:
            year = list(volume_link.next_siblings)[1].string.split(' ')[1]
            print(list(volume_link.next_siblings))
        except IndexError as e:
            print("Error", e.args)

        if int(year) < 1996:
            break
        volume, issue = volume_url.split('/')[-2], volume_url.split('/')[-1]

        try:
            response = requests.get(volume_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            elements = soup.find_all('div', class_='art_title linkable')
            for element in elements:
                if element.previous_sibling.string == 'Articles' or element.previous_sibling.string == 'Article':
                    href = element.find('a')['href']
                    article_url = base_url + href
                    with open("../resources/txt/" + sd.handle_journal_name_without_capital(journal_name) +
                              '.txt', "a", encoding='utf-8') as f:
                        f.write(article_url + ' Volume' + volume + '_Issue' + issue + ' ' + str(ind) + '\n')
                        print("Volume: " + volume + ' Issue: ' + issue + ' ' + str(ind))
                        ind = ind + 1
        except requests.ConnectionError as e:
            print("Error", e.args)


def get_article_en(journal_name, text, article_url, journal_num, volume_info, issue_info):
    if text != '':
        file_name = journal_code[journal_name] + str(journal_num) + '_' + volume_info + '_' + issue_info + '.html'
        print("EN文件 " + article_url + ' ' + str(journal_num))
        path = "../../../../paper data/SAGE/" + journal_name + "/en/"
        with open(path + file_name, "w", encoding='utf-8') as f:
            f.write(text)
            with open("../resources/log/" + sd.handle_journal_name_without_capital(journal_name) + '.log',
                      "a", encoding='utf-8') as f_log:
                f_log.write(article_url + ' Article_num:' + str(journal_num) + '\n')
            f_log.close()
            return 1
    else:
        return 0


def get_article_cn(journal_name, article_url, journal_num, volume_info, issue_info):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko)'
            ' Chrome/80.0.3987.162 Safari/537.36'
    }
    try:
        # 下载成功
        response = requests.get(article_url, headers=headers)
        if response.status_code == 200:
            response.encoding = 'utf-8'

            file_name = journal_code[journal_name] + str(journal_num) + '_' + volume_info + '_' + issue_info + '.html'
            print("CN文件 " + article_url + ' ' + str(journal_num))
            path = "../../../../paper data/SAGE/" + journal_name + '/cn/'
            with open(path + file_name, "w", encoding='utf-8') as f:
                f.write(response.text)
                with open("../resources/log/" + sd.handle_journal_name_without_capital(journal_name) + '.log',
                          "a", encoding='utf-8') as f_log:
                    f_log.write(article_url + ' Article_num:' + str(journal_num) + '\n')
                f_log.close()
        return 1
        # 下载失败
    except requests.ConnectionError as e:
        print("Error", e.args)

    return 0


def get_article(journal_name):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko)'
            ' Chrome/80.0.3987.162 Safari/537.36'
    }

    journal_num = 1
    path = "../resources/txt/" + sd.handle_journal_name_without_capital(journal_name) + ".txt"
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            url, date_info = line.split(' ')[0], line.split(' ')[1]
            volume_info = date_info.split('_')[0]
            issue_info = date_info.split('_')[1].replace('\n', '')
            print(url, volume_info, issue_info)
            try:
                response = requests.get(url, headers=headers)

                soup = BeautifulSoup(response.text, "html.parser")
                a_tags = soup.find_all('a')

                for a_tag in a_tags:
                    is_data_item_exist = bool('data-item-name' in a_tag.attrs)
                    # 可以直接下载
                    if is_data_item_exist and a_tag.attrs['data-item-name'] == 'download-PDF' and a_tag['href'][0] != '#':
                        journal_num = journal_num + get_article_en(journal_name, response.text, url, journal_num,
                                                                   volume_info, issue_info)
                    # 需要使用机构接口获得新的url以下载
                    elif is_data_item_exist and a_tag.attrs['data-item-name'] == 'cnp-link':
                        journal_num = journal_num + get_article_cn(journal_name, a_tag['href'], journal_num, volume_info, issue_info)
            except requests.ConnectionError as e:
                print("Error", e.args)

whe
if __name__ == '__main__':
    # get_volume_link('Entrepreneurship Theory and Practice')
    get_article("Organization Studies")



