import requests

save_dir = "/home/zyz/paper_data/FT50"


def down_source_code():
    headers = {
        'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko)'
            ' Chrome/80.0.3987.162 Safari/537.36'
    }

    ind = 1

    with open("/home/zyz/paper_data/Journal_of_Accounting_and_Economics.txt", "r", encoding='utf-8') as f:
        urls = f.readlines()
        for url in urls:
            re = requests.get(url, headers=headers)
            re.encoding = 'utf-8'
            with open("/home/zyz/paper_data/FT50/Journal of Accounting and Economics/jae{}.html".format(str(ind)), "w",
                      encoding='utf-8') as f2:
                f2.write(re.text)
                if re.text != "":
                    with open("/home/zyz/paper_data/success6.log", "a", encoding='utf-8') as f3:
                        f3.write(url)
                    f3.close()
                ind = ind + 1
            f2.close()


if __name__ == '__main__':
    down_source_code()
