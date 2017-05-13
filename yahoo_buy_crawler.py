import sys
from bs4 import BeautifulSoup as BS
import requests
import csv
import codecs


reload(sys)
sys.setdefaultencoding('utf8')


def export__list_to_csv(product_list):
    f = open("product_list.csv", "w")
    f.write(codecs.BOM_UTF8)
    w = csv.writer(f)
    w.writerows(product_list)
    f.close()
    return 0


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
    title_list = ['type', 'name', 'price', 'original price', 'discount']
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
                # print 'best one:' + hot_name
                # print 'price: ', price
                # print 'original price:', orig_price
                # print 'discount: ', price / orig_price
                # print ' --- '
                # continue
            else:
                hot_r = requests.get(hot_link)
                hot_r.encoding = 'utf8'
                hot_soup = BS(''.join(hot_r.text), 'html.parser')
                spec = hot_soup.select('.item-spec')
                orig_price = str(price)
                orig_price = get_orig_price(spec, price)
                orig_price = float(orig_price)
                # orig_price = price
                # if len(spec) != 0:
                #    orig_price = spec[0].select('.price')[0].text
                #    orig_price_len = orig_price.split('$')
                #    if len(orig_price_len) != 0:
                #        if len(orig_price.split('$')[1].split(',')) != 0:
                #            temp = orig_price_len[1].split(',')[0]
                #            temp_len = len(orig_price_len[1].split(','))
                #            for i in range(1, temp_len):
                #                temp = temp + orig_price_len[1].split(',')[i]
                #            orig_price = float(temp)
                #        else:
                #            orig_price = float(orig_price.split('$')[1])
                #    else:
                #        orig_price = float(orig_price)

            # print 'best one:' + hot_name
            # print 'price: ', price
            # print 'original price:', orig_price
            # print 'discount: ', price / orig_price
            # print ' --- '
        elif len(type_two) != 0:
            # count = count + 1
            # session_req = dryscrape.Session()
            # session_req.visit(new_link)
            # response = session_req.body()
            # new_soup = BeautifulSoup(''.join(response), 'html.parser')
            # hot = new_soup.select('.pditem mainitem yui3-u').find('a').text
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
            # orig_price = price
            # if len(spec) != 0:
            #    orig_price = spec[0].select('.price')[0].text
            #    orig_price_len = orig_price.split('$')
            #    if len(orig_price_len) != 0:
            #        if len(orig_price.split('$')[1].split(',')) != 0:
            #            tem = orig_price_len[1].split(',')[0]
            #            temp_len = len(orig_price_len[1].split(','))
            #            for i in range(1, temp_len):
            #                tem = tem + orig_price.split('$')[1].split(',')[i]
            #            orig_price = float(tem)
            #        else:
            #            orig_price = float(orig_price.split('$')[1])
            #    else:
            #        orig_price = float(orig_price)

            # print 'host one:' + hot_name
            # print 'price:', price
            # print 'original price:', orig_price
            # print 'discount rate: ', price / orig_price
            # print ' --- '
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
                    # print 'host one:' + hot_name
                    # print 'price: ', price
                    # print 'original price:', orig_price
                    # print 'discount rate: ', price / orig_price
                    # print ' --- '
                    # err_count = err_count + 1
                    # continue
                else:
                    hot_r = requests.get(hot_link)
                    hot_r.encoding = 'utf8'
                    hot_soup = BS(''.join(hot_r.text), 'html.parser')
                    spec = hot_soup.select('.item-spec')
                    orig_price = str(price)
                    orig_price = get_orig_price(spec, price)
                    orig_price = float(orig_price)
                    # orig_price = price
                    # if len(spec) != 0:
                    #    orig_price = spec[0].select('.price')[0].text
                    #    orig_price_len = orig_price.split('$')
                    #    if len(orig_price_len) != 0:
                    #        if len(orig_price.split('$')[1].split(',')) != 0:
                    #            tem = orig_price_len[1].split(',')[0]
                    #            temp_len = len(orig_price_len[1].split(','))
                    #            for i in range(1, temp_len):
                    #               tem = tem + orig_price_len[1].split(',')[i]
                    #            orig_price = float(tem)
                    #        else:
                    #            orig_price = float(orig_price.split('$')[1])
                    #    else:
                    #        orig_price = float(orig_price)
                # print 'host one:' + hot_name
                # print 'price: ', price
                # print 'original price:', orig_price
                # print 'discount:', price / orig_price
                # print ' --- '

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
                r3 = s.post(url_login, data=payload, headers=header_info)
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
                    # orig_price = price
                    # if len(spec) != 0:
                    #    orig_price = spec[0].select('.price')[0].text
                    #    orig_price_len = orig_price.split('$')
                    #    if len(orig_price_len) != 0:
                    #        orig_price_one = orig_price_len[1]
                    #        if len(orig_price_len[1].split(',')) != 0:
                    #            tem = orig_price_len[1].split(',')[0]
                    #            temp_len = len(orig_price_len[1].split(','))
                    #            for i in range(1, temp_len):
                    #                tem = tem +orig_price_len[1].split(',')[i]
                    #            orig_price = float(tem)
                    #        else:
                    #            orig_price = float(orig_price.split('$')[1])
                    # else:
                    #    orig_price = float(orig_price)

                    # count = count + 1
                    # print 'host one:' + hot_name
                    # print 'price: ', price
                    # print 'original price:', orig_price
                    # print 'discount rate: ', price / orig_price
                    # print ' --- '
        temp_dict = []
        temp_dict.append(label_title)
        temp_dict.append(hot_name)
        temp_dict.append(price)
        temp_dict.append(orig_price)
        temp_dict.append(price / orig_price)
        # last_index = len(product_list) - 1
        if i == 0:
            product_list.append(temp_dict)
            print 'host one:' + hot_name
            print 'price: ', price
            print 'original price:', orig_price
            print 'discount rate: ', price / orig_price
            print ' --- '
        elif flag:
            if temp_dict[4] < product_list[0][4]:
                product_list.insert(0, temp_dict)
            else:
                product_list.append(temp_dict)
                print 'host one:' + hot_name
                print 'price: ', price
                print 'original price:', orig_price
                print 'discount rate: ', price / orig_price
                print ' --- '
        # elif len(type_two) != 0:
        # else:
    return 0


def main():
    print '123'
    user_name = 'of_alpha12345@yahoo.com.tw'
    password = 'aa839962'
    the_product_list = []
    list_popular_products(user_name, password, the_product_list)
    print the_product_list[0][0]
    print the_product_list[0][1]
    print the_product_list[0][2]
    print the_product_list[0][3]
    print the_product_list[0][4]
    print len(the_product_list)
    export__list_to_csv(the_product_list)


if __name__ == "__main__":
    main()
