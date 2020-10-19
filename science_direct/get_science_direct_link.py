from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver


base_url = 'https://www.sciencedirect.com'


def handle_journal_name_without_capital(journal_name):
    journal_name = journal_name.replace(' ', '-')
    journal_name = journal_name.casefold()
    return journal_name


def handle_journal_name(journal_name):
    journal_name = journal_name.replace(' ', '_')
    return journal_name


def get_volume_and_issue_link(url, volume_link, journal_issues, issn):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko)'
            ' Chrome/80.0.3987.162 Safari/537.36'
    }

    headers2 = {
        'Host': 'www.sciencedirect.com',
        'Referer': volume_link,
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko)'
            ' Chrome/80.0.3987.162 Safari/537.36'
    }

    re = requests.get(url, headers=headers)
    soup = BeautifulSoup(re.text, 'html.parser')

    year_lists = soup.find_all('span', class_='accordion-title js-accordion-title')

    for year_list in year_lists:
        year = year_list.string.split(' ')[0]
        if int(year) <= 1996:
            break
        request_url = base_url + '/journal/' + issn + '/year/' + year + '/issues'
        try:
            re_ajax = requests.get(request_url, headers=headers2)
            if re_ajax.status_code == 200:
                js = re_ajax.json()
                length = len(js.get('data'))
                for i in range(length):
                    volume_code = js.get('data')[i].get('uriLookup')
                    with open('../resources/txt/' + journal_issues + '.txt', 'a', encoding='utf-8') as f:
                        des_link = base_url + '/journal/' + journal_issues + volume_code
                        print(des_link)
                        f.write(des_link + '\n')
        except requests.ConnectionError as e:
            print('Error', e.args)


# 生成volume和issue的链接
def generate_volume_page(journal_name):
    journal_issues = handle_journal_name_without_capital(journal_name)
    url = base_url + '/journal/' + journal_issues + '/issues'

    headers = {
        'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko)'
            ' Chrome/80.0.3987.162 Safari/537.36'
    }

    re = requests.get(url, headers=headers)
    soup = BeautifulSoup(re.text, 'html.parser')

    volume_and_issue_link_tag = soup.find('span', class_='pagination-pages-label')
    page = volume_and_issue_link_tag.string.split(' ')[3]

    issn_tag = soup.find('p', class_='u-margin-xs-bottom text-s u-display-block js-issn')
    issn = issn_tag.string.split(' ')[1].replace('-', '')
    print(issn)

    for i in range(1, int(page)+1):
        volume_link = url + '?page=' + str(i)
        print(volume_link)
        get_volume_and_issue_link(volume_link, volume_link, journal_issues, issn)


def get_article_link(journal_name):
    journal_name_handled = handle_journal_name_without_capital(journal_name)
    i = 0
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko)'
            ' Chrome/80.0.3987.162 Safari/537.36'
    }

    path = '../../paper data/FT50/' + journal_name + '.txt'
    with open('../resources/txt/' + journal_name_handled + '.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            try:
                re = requests.get(line, headers=headers)
                if re.status_code == 200:
                    soup = BeautifulSoup(re.text, 'html.parser')
                    article_link_tags = soup.find_all('a', class_='anchor article-content-title u-margin-xs-top u-margin-s-bottom')
                    for article_link_tag in article_link_tags:
                        with open(path, "a", encoding='utf-8') as f2:
                            article_link = base_url + article_link_tag['href']
                            i = i + 1
                            print(line + ' ' + article_link + ' ' + str(i))
                            f2.write(article_link + '\n')
            except requests.ConnectionError as e:
                print('Error, link num: {}'.format(i), e.args)


def down_source_code(journal_name):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko)'
            ' Chrome/80.0.3987.162 Safari/537.36'
    }
    ind = 1
    journal_name_handled = handle_journal_name(journal_name)
    path1 = '../../txt/' + journal_name_handled + '.txt'
    path2 = '../../FT50/' + journal_name
    path3 = '../../log/' + journal_name_handled + '.log'
    with open(path1, "r", encoding='utf-8') as f1:
        urls = f1.readlines()
        for url in urls:
            try:
                re = requests.get(url, headers=headers)
                if re.status_code == 200:
                    re.encoding = 'utf-8'
                    with open(path2 + '/jbv{}.html'.format(str(ind)), "w", encoding='utf-8') as f2:
                        if re.text != "":
                            with open(path3, "a", encoding='utf-8') as f3:
                                f3.write(url)
                            f3.close()
                        f2.write(re.text)
                        ind = ind + 1
                    f2.close()
            except requests.ConnectionError as e:
                print("Error num {}".format(str(ind)), e.args)


if __name__ == "__main__":
    # generate_volume_page("Journal of Business Venturing")
    # get_article_link("Journal of Business Venturing")
    down_source_code('Journal of Business Venturing')
