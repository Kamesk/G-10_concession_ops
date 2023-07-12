import lib_file_bin_check
import location_1

import csv
import os
import pandas as pd
import time
user = os.getlogin()
import json

path = 'bin_check_input.xlsx'

def write_excel_log(data_dict):
    d = data_dict
    d['date'] = pd.datetime.today()
    list_data = list(d.values())
    if len(list_data) != 0:
        f = open('blma_bin_check.csv', 'a', newline='', encoding="utf-8")
        writer = csv.writer(f)
        writer.writerow(list_data)



df = pd.read_excel(path, sheet_name='Sheet1')
print(df)

for index, row in df.iterrows():


    print(row)

    d = {}

    d['upc'] = str(row['UPC'])
    d['fc'] = str(row['FC'])
    d['linking_asins'] = str(row['linking_asins'])

    details_1 = str(row['Corres'])

    details = "Hello FC,"\
              \
              \
              +details_1

    fc = str(row['FC'])
    print(fc)

    details = "Hi Team" \
               "%0aIssue:" + details_1 + "" \
               "%0aThank You"""



    a = str(row['linking_asins'])
    print(a)
    bad_chars = ['[', ']', "'"]

    for i in bad_chars :
        a = a.replace(i, '')

    print(a)
    asins = str(a)

    print(d)

    if lib_file_bin_check.fc_city(fc) == 'Exception' or lib_file_bin_check.fc_b_id(fc)== 'Exception':

        d['tt_id'] = 'Exception'
        write_excel_log(d)

    else:

        bin_check = lib_file_bin_check.file_bin_check(details,asins,fc)
        print(bin_check)
        d['tt_id'] = bin_check
        write_excel_log(d)