from pprint import pprint
import csv
import re
import pandas as pd


with open('phonebook_raw.csv', encoding='utf8') as f:
    rows = csv.reader(f, delimiter=',')
    contact_list = list(rows)

# pprint(contact_list)

patter_name = r'^(\w+)[\s|,]{1}(\w+)[\s|,]{1}(\w+)?'
replace_name = r'\1, \2, \3'

patter_phone = r'((\+7|8)\s?\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2}))\s?(\(?(\w{3}\.)\s(\d{4})\)?)?'
replace_phone = r'+7(\3)\4-\5-\5 \8\9'

class Phonebook:
    def __init__(self, phone_list):
            self.phone_list = phone_list

    def text(self, text):

        result_name = re.sub(patter_name, replace_name, ','.join(text[:2])).replace(' ','').split(',')
        if len(result_name) >= 4:
            result_name.pop(-1)
        for i in range(len(result_name)):
            text[i] = result_name[i]
        result_phone = re.sub(patter_phone, replace_phone, text[5])
        text[5] = result_phone

        return text
    
    def list_handler(self):

        for i in range(1, len(self.phone_list)):
            pre_res = self.text(self.phone_list[i])
            self.phone_list[i] = pre_res
    def list_clean(self):
        self.list_handler()
        temp_d = self.phone_list
        for i in range(len(temp_d)-1, 0, -1):
            for j in range(i-1, 1, -1):
                if temp_d[i][0] == temp_d[j][0] and temp_d[i][1] == temp_d[j][1]:
                    for k in range(7):
                        if temp_d[j][k] == temp_d[i][k]:
                            continue
                        else:
                            temp_d[j][k] += temp_d[i][k]
                    temp_d.pop(i)
                    break

        return temp_d

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
#     datawriter.writerows(contacts_list)

if __name__ == '__main__':
    fns = Phonebook(phone_list = contacts_list)

    # pprint(fns.text(fns.phone_list[1]))
    # fns.list_handler()
    fns.list_clean()

    pprint(pd.DataFrame(fns.phone_list))

    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(fns.phone_list)