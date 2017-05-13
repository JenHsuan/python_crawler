#
# Jen-Hsuan Hsieh 2017/05/13
#

import sys
from bs4 import BeautifulSoup as BS
import requests
import csv
import codecs
import argparse

reload(sys)
sys.setdefaultencoding('utf8')


parser = argparse.ArgumentParser(
    description='''It's a crawler tool target on ''' +
    '''Yahoo store (https://tw.buy.yahoo.com/)''',
    epilog="""All's well that ends well.""")
parser.add_argument('account', help="Yahoo account name")
parser.add_argument('password', help="Yahoo account password")
args = parser.parse_args()


def export_list_to_csv(product_list):
    with open('product_list.csv', 'wb') as csvfile:
        csvfile.write(codecs.BOM_UTF8)
        spamwriter = csv.writer(csvfile, dialect='excel')
        for i in range(0, len(product_list), 1):
            spamwriter.writerow(product_list[i])


def get_orig_price(spec, price):
    if len(spec) != 0:
        orig_price = spec[0].select('.price')[0].text
        orig_price_len = orig_price.split('$')
        if len(orig_price_len) != 0:
            if len(orig_price.split('$')[1].split(',')) != 0:
                temp = orig_price_len[1].split(',')[0]
                temp_len = len(orig_price_len[1].split(','))
                for i in range(1, temp_len):
                    temp = temp + orig_price_len[1].split(',')[i]
                orig_price = temp
            else:
                orig_price = orig_price.split('$')[1]
    else:
        orig_price = str(price)

    return orig_price


def list_popular_products(user_name, password, product_list):
    title_list = ['type', 'name', 'price', 'original price', 'discount', 'id']
    product_list.append(title_list)
    # define request header
    header_info = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X' +
        ' 10_9_1) Apple' +
        'WebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1581.2 Sa' +
        'fari/537.36',
        'Host': 'login.yahoo.com',
        'Origin': 'https://login.yahoo.com',
        'Connection': 'keep-alive',
        'Referer': 'https://login.yahoo.com/config/login?.pd=c' +
        '%3Dcbh6yDW72e4PVguS5V9HYCf6gg--&.intl=tw&.src=shp&.done=' +
        'https' +
        '%3A%2F%2Ftw.buy.yahoo.com%2Flogin%3F.done%3Dhttps%25' +
        '3A%252F%252F' +
        'tw.buy.yahoo.com%252F%253Fsub%253D566',
        'Content-Type': 'application/x-www-form-urlencoded'}
    url_prefix = 'https://tw.buy.yahoo.com'
    url_login = 'https://login.yahoo.com/'
    category = 'https://tw.buy.yahoo.com/help/helper.asp'
    category = category + '?p=sitemap&hpp=sitemap'
    r = requests.get(category)
    # set encoding
    r.encoding = 'big5'

    # visit
    soup = BS(''.join(r.text), 'html.parser')
    site_list = soup.select('.site-list')
    len_category = len(site_list)
    count = 0
    for i in range(0, len_category, 1):
        flag = False
        label = 'category' + str(i) + " :"
        label_title = site_list[i].find('a').text
        label = label + label_title
        index = site_list[i].find('a').get('href').split('=')[1]
        print label
        new_link = 'https://tw.buy.yahoo.com'
        new_link = new_link + site_list[i].find('a').get('href')
        new_r = requests.get(new_link)
        new_r.encoding = 'utf8'
        new_soup = BS(''.join(new_r.text), 'html.parser')
        type_one = new_soup.select('#lnk_sub' + index + '_rank_01_v7')
        type_two = new_soup.select('.pditem')
        if len(type_one) != 0:
            flag = True
            hot = new_soup.select('#lnk_sub' + index + '_rank_01_v7')[0]
            hot_info = hot.select('.intro')[0]
            hot_link = hot.select('.pic')[0].find('a').get('href')
            hot_name = hot_info.select('.text')[0].find('a').text
            if len(hot_info.select('.red-price')[0].find('a').text) == 0:
                price = -1
            else:
                price = float(hot_info.select('.red-price')[0].find('a').text)
            if len(hot_link.split(':')) == 1:
                orig_price = price
            else:
                hot_r = requests.get(hot_link)
                hot_r.encoding = 'utf8'
                hot_soup = BS(''.join(hot_r.text), 'html.parser')
                spec = hot_soup.select('.item-spec')
                orig_price = str(price)
                orig_price = get_orig_price(spec, price)
                orig_price = float(orig_price)
        elif len(type_two) != 0:
            flag = True
            price = new_soup.select('.pditem')[0].select('.price')[0]
            hot_name = new_soup.select('.pditem')[0].select('.desc')[0].text
            hot_link = new_soup.select('.pditem')[0].find('a').get('href')
            # print new_soup.select('.mainitem')[0].text
            hot_r = requests.get(url_prefix + hot_link)
            hot_r.encoding = 'utf8'
            hot_soup = BS(''.join(hot_r.text), 'html.parser')
            spec = hot_soup.select('.item-spec')
            price = float(price.select('.shpprice')[0].text)
            orig_price = str(price)
            orig_price = get_orig_price(spec, price)
            orig_price = float(orig_price)
        else:
            _index = new_r.url.split('=')[1]
            type_one = new_soup.select('#lnk_sub' + _index + '_rank_01_v7')
            if len(type_one) != 0:
                flag = True
                hot = new_soup.select('#lnk_sub' + _index + '_rank_01_v7')[0]
                hot_info = hot.select('.intro')[0]
                hot_link = hot.select('.pic')[0].find('a').get('href')
                _hot_price = hot_info.select('.red-price')[0].find('a').text
                hot_name = hot_info.select('.text')[0].find('a').text
                if len(hot_info.select('.red-price')[0].find('a').text) == 0:
                    price = -1
                else:
                    price = float(_hot_price)
                if len(hot_link.split(':')) == 1:
                    orig_price = price
                else:
                    hot_r = requests.get(hot_link)
                    hot_r.encoding = 'utf8'
                    hot_soup = BS(''.join(hot_r.text), 'html.parser')
                    spec = hot_soup.select('.item-spec')
                    orig_price = str(price)
                    orig_price = get_orig_price(spec, price)
                    orig_price = float(orig_price)
            else:
                payload = {}
                s = requests.Session()
                # 1.login
                r2 = s.get(url_login)
                _soup = BS(''.join(r2.text), 'html.parser')
                for i in range(0, len(_soup.find_all('input')), 1):
                    temp = _soup.find_all('input')[i]
                    payload[str(temp.get('name'))] = str(temp.get('value'))
                payload['username'] = user_name
                payload['passwd'] = password
                # print payload
                s.post(url_login, data=payload, headers=header_info)
                # 2.authetication
                r4 = s.get('https://tw.buy.yahoo.com/?sub=' + index)
                # print index
                r5 = s.get(r4.url)
                _soup = BS(''.join(r5.text), 'html.parser')
                # print r5.text
                payload2 = {}
                if _soup.find("form", class_="yui3-u") is not None:
                    flag = True
                    temp = _soup.find("form", class_="yui3-u").find('input')
                    payload2[str(temp.get('name'))] = str(temp.get('value'))
                    url_sec = _soup.find("form", class_="yui3-u").get('action')
                    r6 = s.post(url_prefix + url_sec, data=payload2)
                    _soup = BS(''.join(r6.text), 'html.parser')
                    hot = _soup.select('#lnk_sub' + index + '_rank_01_v7')[0]
                    hot_info = hot.select('.intro')[0]
                    hot_price = hot_info.select('.red-price')[0]
                    price = float(hot_price.find('a').text)
                    hot_link = hot_info.select('.text')[0].find('a')
                    hot_name = hot_link.text
                    hot_r = requests.get(hot_link.get('href'))
                    hot_r.encoding = 'utf8'
                    hot_soup = BS(''.join(hot_r.text), 'html.parser')
                    spec = hot_soup.select('.item-spec')
                    orig_price = str(price)
                    orig_price = get_orig_price(spec, price)
                    orig_price = float(orig_price)
        temp_dict = []
        temp_dict.append(label_title)
        temp_dict.append(hot_name)
        temp_dict.append(price)
        temp_dict.append(orig_price)
        temp_dict.append(price / orig_price)
        disnum = temp_dict[4]
        # last_index = len(product_list) - 1
        if count == 0:
            count = count + 1
            temp_dict.append(count)
            product_list.append(temp_dict)
        elif count == 1:
            count = count + 1
            temp_dict.append(count)
            # compare with first one
            if disnum < product_list[1][4]:
                product_list.insert(1, temp_dict)
            else:
                product_list.append(temp_dict)
        elif flag:
            notInsert = True
            for j in range(1, count):
                temp_num1 = product_list[j][4]
                temp_num2 = product_list[j + 1][4]
                temp_name1 = product_list[j][1]
                temp_name2 = product_list[j + 1][1]
                if temp_dict[1] == temp_name1 or temp_dict[1] == temp_name2:
                    notInsert = False
                    break
                if disnum < temp_num1:
                    count = count + 1
                    temp_dict.append(count)
                    product_list.insert(j, temp_dict)
                    notInsert = False
                    break
                elif disnum >= temp_num1 and disnum < temp_num2:
                    count = count + 1
                    temp_dict.append(count)
                    product_list.insert(j + 1, temp_dict)
                    notInsert = False
                    break
            if notInsert:
                count = count + 1
                temp_dict.append(count)
                product_list.append(temp_dict)
        if flag:
            print 'host one:' + hot_name
            print 'price: ', price
            print 'original price:', orig_price
            print 'discount rate: ', price / orig_price
            print ' --- '
        # elif len(type_two) != 0:
        # else:
    return 0


def main():
    user_name = args.account
    password = args.password
    the_product_list = []
    list_popular_products(user_name, password, the_product_list)
    export_list_to_csv(the_product_list)


if __name__ == "__main__":
    main()
