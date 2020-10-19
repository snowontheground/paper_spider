
def compare_url():
    with open("../paper data/FT50/Journal of Business Venturing.txt", "r", encoding='utf-8') as f1:
        lines = f1.readlines()
        for line in lines:
            with open("../paper data/FT50/Journal_of_Business_Venturing.log", "r",
                      encoding='utf-8') as f2:
                lines2 = f2.readlines()
                if line in lines2:
                    pass
                else:
                    with open("../paper data/FT50/undownload_Journal_of_Business_Venturing.log",
                              "a", encoding='utf-8') as f3:
                        f3.write(line)


if __name__ == "__main__":
    compare_url()