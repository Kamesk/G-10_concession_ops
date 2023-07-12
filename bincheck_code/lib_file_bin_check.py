import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import subprocess
import location_1



def choose_fc(driver,asin,mp, building):
    try:
        delay = 30
        ct = 0

        mp = mp.lower()

        if mp == 'us':
            marketplace = '1'
            merchant = '1'
            market = 'na'

        elif mp == 'ca':
            marketplace = '7'
            merchant = '13'
            market = 'na'

        elif mp == 'ae':
            marketplace = '338801'
            merchant = '18034145125'
            market = 'eu'

        elif mp == 'de':
            marketplace = '4'
            merchant = '10'
            market = 'eu'


        elif mp == 'es':
            marketplace = '44551'
            merchant = '695831032'
            market = 'eu'

        elif mp == 'fr':
            marketplace = '5'
            merchant = '11'
            market = 'eu'



        elif mp == 'uk':
            marketplace = '3'
            merchant = '9'
            market = 'eu'

        elif mp == 'it':
            marketplace = '35691'
            merchant = '755690533'
            market = 'eu'

        elif mp == 'mx':
            marketplace = '771770'
            merchant = '8833336105'
            market = 'na'

        elif mp == 'br':
            marketplace = '526970'
            merchant = '2091039151'
            market = 'na'

        else:
            # to default alaska set to us marketplace
            marketplace = '1'
            merchant = '1'
            market = 'na'

        url = 'https://alaska-' + str(market) + '.amazon.com/index.html?viewtype=summaryview&use_scrollbars=&fnsku_simple=' + str(asin) + '&marketplaceid=' + str(marketplace) + '&merchantid=' + str(merchant) + '&AvailData=Get+Availability+Data'

        # url = 'https://alaska-na.amazon.com/index.html?viewtype=summaryview&use_scrollbars=&fnsku_simple=' + str(asin) + '+&marketplaceid=1&merchantid=1&AvailData=Get+Availability+Data'
        # print(url)
        driver.get(url)
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="view"]/table[1]/tbody/tr/td[1]/b[2]')))
        except TimeoutException:
            print('Loading took too much time!')

        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="view"]/table[2]')))
        except TimeoutException:
            return 'No Inventory'

        fc_ignore_list = ['EUK5', 'HWA3', 'HKG3', 'SCK1', 'EUK5', 'PESB', 'MME1', 'PILH', 'PILE', 'HUK3', 'HUK5', 'FRA3', 'LAX6', 'BCN1', 'KRB1', 'BTS2', 'YUL2', 'DEN7', 'IMXI', 'PICV',
                          'DCA6', 'MEM6', 'IMXJ', 'SLC2', 'PIT2', 'PIJA', 'HOU7', 'JVL1', 'IMXK', 'BFL1', 'KRB2', 'MQJ2', 'IAH1', 'MTY1', 'DAL2', 'SBD2', 'ATL2', 'LGB9', 'AGS2', 'CSG1',
                          'AKC1', 'BFI2', 'TPA6', 'PCW1', 'AZA4', 'MEM4', 'SCK3', 'GYR1', 'GDL1', 'PIOA', 'TPA3', 'RDG1', 'DSM5', 'HNE1']

        tags = driver.find_element_by_xpath('//*[@id="view"]/table[2]')
        trs = tags.find_elements_by_tag_name('tr')
        ct = len(trs)
        bin_fc = []
        # bin_fc_3p = []
        fcs = ''
        if ct > 5:
            for tr in trs[2:ct - 3]:
                td = tr.find_elements_by_tag_name('td')
                fc_id = td[0].text
                # print(fc_id)
                inventory = int(td[1].text)
                # print(inventory)
                if inventory != 0 and fc_id != building and fc_id[0] != 'U' and fc_id[0] != 'X' and fc_id not in fc_ignore_list:
                    bin_fc.append(fc_id)

            # print(bin_fc)
            if len(bin_fc) == 1:
                fcs = random.sample(bin_fc, k=1)
            elif len(bin_fc) > 1:
                fcs = random.sample(bin_fc, k=2)
            elif len(bin_fc) == 0:
                return 'No Inventory'

            if fcs == '':
                return 'No Inventory'
            else:
                # print("choosing 2 FCs to file bin check", fcs)
                return fcs
    except TimeoutException:
        # print('Exception in choosing FC for bin check')
        return 'Exception'


def fc_city(fc):
    try:
        city = location_1.problem_location[fc]['city']

        return city

    except Exception as ex:
        print(ex)
        return 'Exception'


def fc_b_id(fc):
    try:
        b_id = location_1.problem_location[fc]['city']

        return b_id

    except Exception as ex:
        print(ex)
        return 'Exception'


def file_bin_check(details,asin,fc):


    item = 'check item in bin'
    print(fc)
    print(asin)

    try:

        # details = "Hi Team" \
        #           "%0a%0aProduct Details:""" \
        #           "%0a%0aASIN:" + asin + "" \
        #            "%0aIssue: Please confirm whether the item in hand matches the catalog details and also provide us images for the same." \
        #            "%0aThank You"""

        city = location_1.problem_location[fc]['city']
        b_id = location_1.problem_location[fc]['b_id']
        # print(city)
        # print(b_id)
        # print(fc)
        # item = 'Andon Cord Bin Check'
        ag = "ISS-" + fc

        # print ('Ticket create module API')internet
        category = 'iss'
        type = 'Retail Request'

        short_description = '100 percent Bin Check :' + asin + ''

        # Ticket API - Don't use '-k' if you have proper SSL certificate

        command = 'curl -i -k -u "flx-rbs-dr-maa2:test1234" -d "status=Assigned&impact=5&short_description=' + str(
            short_description) + '&details=' + str(details) + '&category=' + str(category) + '&type=' + str(
            type) + '&item=' + str(item) + '&city=' + str(city) + '&building=' + str(
            b_id) + '&requester_login=flx-rbs-dr-maa2&asin=' + str(asin) + '&quantity=0&assigned_group=' + str(
            ag) + '&upc=-&vendor_id=-&isd=-&title=-" https://ticket-api.amazon.com/tickets/'

        # print(command, '\n')

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out1, err1 = p.communicate()
        response_txt = out1.decode('ASCII')
        print(response_txt)

        for line in response_txt.splitlines():
            if 'Location:' in line:
                location = line.split('/')
                try:
                    tt_id = int(location[4])
                    return '{:0>10}'.format(tt_id)
                except:
                    return 'Exception'

        return 'Exception'

    except TimeoutException:
        print('nooo')
        return 'Exception'



def create_relation(parent,child):
    # command = 'curl -u flx-rbs-dr-maa2:flx-rbs-dr-maa2 -prod -k https://ticket-api.amazon.com/tickets/'+case_id+''
    # -X PUT
    command = 'curl -k -i -u "flx-rbs-andon-maa2:andon747" -d "Operation=CreateRelation&related_items.related_item.1.id='+parent+'&related_items.related_item.1.type=Trouble%20Ticket&related_items.related_item.1.relation=Parent%20Of&related_items.related_item.2.id='+child+'&related_items.related_item.2.type=Trouble%20Ticket&related_items.related_item.2.relation=is%20related%20to&submitter=flx-rbs-dr-maa2" https://wfa-api.amazon.com'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    response_txt = out.decode('ASCII')
    if 'HTTP/1.1 200 OK' in response_txt:
        return 'relation created successfully'
    else:
        return 'Failed to create relation'

def file_bin(driver,asin, marketplace, building, qty, tt):
    bin_tickets = []
    a = choose_fc(driver, asin,marketplace, building)
    print(a)
    if a == 'No Inventory':
        return 'No Inventory'
    else:
        for fc in a:
            b = file_bin_check(driver,asin,fc, qty)
            if b != 'Exception' or b != 'None':
                bin_tickets.append(b)
                c = create_relation(tt, b)
                print(c)

        return bin_tickets

# a = create_relation('0305562377', '0305557818')

'''
driver = webdriver.Chrome()
time.sleep(2)
url = 'https://alaska-na.amazon.com/'
driver.get(url)

fc_ids = ['EWR9', 'MDW7']
bin_tickets = []
for fc in fc_ids:
    a = file_bin_check(driver, 'B005D91DZ4' ,fc)
    bin_tickets.append(a)
print(bin_tickets)

bin_tickets = ['0411879510', '0411878756']
b = relate_bin_check(driver,bin_tickets,'0411700913')
'''

# driver = webdriver.Chrome()
# time.sleep(2)
# a = file_bin(driver, 'B07PQQDH5Y', 'us', 'JAX2', 2, '0529345141')
# print(a)
