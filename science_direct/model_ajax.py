import requests
from urllib.parse import urlencode


def handle_journal_name(journal_name):
    journal_name = journal_name.replace(' ', '-')
    journal_name = journal_name.casefold()
    return journal_name


base_url = 'https://www.sciencedirect.com/journal'


def get_ajax_data(journal_name):
    referer_url = 'https://www.sciencedirect.com/journal/' + journal_name + '/issues'

    headers = {
        'Host': 'www.sciencedirect.com',
        'Referer': referer_url,
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko)'
            ' Chrome/80.0.3987.162 Safari/537.36'
    }

    url = base_url + '/07495978/year/2019/issues'

    try:
        re = requests.get(url, headers=headers)
        if re.status_code == 200:
            print(re.json())
    except requests.ConnectionError as e:
        print('Error', e.args)


if __name__ == '__main__':
    get_ajax_data(handle_journal_name('Organizational Behavior and Human Decision Processes'))
