from Trendata import *
from datetime import date
from datetime import datetime
from datetime import timedelta


def get_commodity_info(data):
    commodity_info = {}

    commodity_info['commodity_asin'] = data['ASIN']

    name = data['productInfo'][0]['name']
    if len(name) > 120:
        name = name[0:120] + "..."
    commodity_info['commodity_name'] = name

    commodity_info['commodity_sales'] = data['stats_info']['review_count']

    commodity_info['commodity_avg_star'] = data['stats_info']['avg_info']

    img_url = []

    for img in data['productInfo']:
        img_url += [img['img']]

    commodity_info['commodity_img'] = img_url

    commodity_info['commodity_avg_price'] = round(get_avg_price(data), 2)

    commodity_tags = data['stats_info']['keywords']
    tag = ''
    for tags_info in commodity_tags:
        tags_info.reverse()

    commodity_tags.sort()

    if (len(commodity_tags) <= 4):
        for tags in commodity_tags:
            tag += tags[1] + " "

    else:
        for i in range(4):
            tag += commodity_tags[i][1] + " "

    commodity_info['commodity_tags'] = tag

    return commodity_info


def get_star_count(data):
    star_list = [float(single_review['star'].split()[0]) \
                 for single_review in data['review']]
    dic = count(star_list)
    star_count = [0, 0, 0, 0, 0]
    if (dic.has_key(1.0)):
        star_count[0] = dic[1.0]
    if (dic.has_key(2.0)):
        star_count[1] = dic[2.0]
    if (dic.has_key(3.0)):
        star_count[2] = dic[3.0]
    if (dic.has_key(4.0)):
        star_count[3] = dic[4.0]
    if (dic.has_key(5.0)):
        star_count[4] = dic[5.0]
    return star_count


def count(ta):
    la = []
    lth = len(ta)

    for i in range(lth):
        la.append(ta[i])

    la.sort()
    da = {}
    i = 0
    while i < lth:
        da[la[i]] = la.count(la[i])
        i = i + da[la[i]]

    return da


def get_price_info(data):
    list = []
    price_info = {}
    for offer in data['offer']:
        for info in offer['info']:
            if info['seller']['name'] == 'Null':
                price = info['price']
                if type(price) == str:
                    price = price.replace('$', '')
                    price = price.replace(',', '')
                list += [['Amazon', float(price), datetime.strptime(info['timestamp'], "%Y-%m-%d %H:%M:%S")]]
            else:
                price = info['price']
                if type(price) == str:
                    price = price.replace('$', '')
                    price = price.replace(',', '')
                list += [
                    [info['seller']['name'], float(price), datetime.strptime(info['timestamp'], "%Y-%m-%d %H:%M:%S")]]
    list = sorted(list, key=lambda e: e[2], reverse=False)
    if list:
        price_info['earliest_time'] = list[0][2]
        price_info['latest_time'] = list[-1][2]
        time_list = []
        avg_price = []
        lowest_price = []
        highest_price = []
        price_list = []
        for each_price in list:
            time_list += [each_price[2]]
        for each_time in set(time_list):
            for i in range(0, len(list)):
                if each_time == list[i][2]:
                    price_list += [list[i][1]]
            price_list.sort()
            lowest_price += [price_list[0]]
            highest_price += [price_list[-1]]
            avg_price += [sum(price_list) / len(price_list)]
            price_list = []

        price_info['lowest_price'] = lowest_price
        price_info['highest_price'] = highest_price
        price_info['avg_price'] = avg_price
        tmp = [i for i in set(time_list)]
        tmp.sort(key=lambda x: x)
        tmp2 = []
        for item in tmp:
            tmp2 += [str(item.year) + str(item.month) + str(item.day)]
        price_info['time_list'] = tmp2

    return price_info


def handle_price_info(price_list, time_list):
    data = []
    for i in range(0, len(price_list)):
        year = (time_list[i]).year
        month = (time_list[i]).month
        day = (time_list[i]).day
        data += [year, month, day, price_list[i]]
    return data


def get_sell_info(commodity_data):
    sell_info = []
    for content in commodity_data['review']:
        info = {'consumer': content['consumer'], 'ASIN': commodity_data['ASIN'],
                'time': datetime.strptime(content['publishTime'].split(' ')[0], "%Y-%m-%d").date()}
        sell_info += [info]
    return sell_info


def get_buy_time(sell_info, consumer):
    for info in sell_info:
        if info['consumer'] == consumer:
            return info['time']


def get_relative_commodities(asin):
    sell_info = get_sell_info(get_commodity_data(asin))

    # get consumer list
    consumer_list = []
    for info in sell_info:
        if info['consumer'] not in consumer_list:
            consumer_list += [info['consumer']]

            # get relative sell info
    relative_sell_info = []
    source_file = open('/Amazon_Index/Amazon_Index/recommender.data', 'r')
    data_line = source_file.readline()
    while data_line:
        tmp = data_line.split('////')
        if tmp[0] in consumer_list:
            str_date = tmp[2][:-1]
            if str_date == '':
                data_line = source_file.readline()
                continue
            date = datetime.strptime(str_date, "%Y-%m-%d").date()

            base_buy_date = get_buy_time(sell_info, tmp[0])
            delta = base_buy_date - date
            if delta > timedelta(-5) and delta < timedelta(5) and tmp[1] != asin:
                line_info = {'consumer': tmp[0], 'asin': tmp[1], 'date': date}
                relative_sell_info += [line_info]
        data_line = source_file.readline()

        # stastics
    relative_asin_list = []
    relative_asin_stastics = {}
    for info in relative_sell_info:
        if info['asin'] not in relative_asin_list:
            relative_asin_list += [info['asin']]
            relative_asin_stastics[info['asin']] = 1
        else:
            relative_asin_stastics[info['asin']] = relative_asin_stastics[info['asin']] + 1
    sorted_asin_stastics = sorted(relative_asin_stastics.items(), key=lambda e: e[1], reverse=True)

    keys = []
    values = []
    for k, v in sorted_asin_stastics:
        keys += [k]
        values += [v]

    count = 10;
    i = 0
    keys_show = []
    for key in keys:
        if i != count:
            keys_show += [autosplit(get_commodity_name(get_commodity_data(key)))]
        else:
            break
        i += 1
    values_show = values[:10]
    keys_show.reverse()
    values_show.reverse()
    result = {'commodity': keys_show, 'sales': values_show}
    return result


def get_sales_info(data):
    sales_info = {}
    time_list = []
    time_list1 = []
    sales_list = []
    review = data['review']

    for each_review in review:
        time_list1 += [each_review['publishTime'].split(' ')[0][0:7]]
    for each_time in time_list1:
        if each_time not in time_list:
            time_list += [each_time]
    time_list.sort()

    sales_info['first_sales_time'] = time_list[0]
    sales_info['latest_sales_time'] = time_list[-1]

    for each_time in time_list:
        sales = 0
        for each_review in review:
            if each_review['publishTime'].startswith(each_time):
                sales = sales + 1
        sales_list += [sales]

    for i in range(0, len(time_list)):
        time_list[i] = time_list[i].replace('-', '', )
    sales_info['time_list'] = time_list
    sales_info['sales_list'] = sales_list
    return sales_info


def read_dic(path):
    source_file = open(path, 'r')
    data_line = source_file.read()
    dic = data_line.split('\n')
    print str(dic)
    source_file.close()
    return dic


def analyse_data(data, dic):
    review = data['review']
    result = {}
    for each_review in review:
        content = each_review['content']
        content = content.lower()
        content = content.replace(',', '')
        content = content.replace('.', '')
        content = content.replace('?', '')
        content = content.replace('!', '')
        words = content.split(' ')
        for word in words:
            if word in dic:
                if word in result:
                    result[word] += 1
                else:
                    result[word] = 1
    return result


def count_data(dic):
    sum = 0
    for key in dic.keys():
        sum += dic[key]
    return sum


def get_emotion_count(data):
    positive_words = read_dic('dic/positive.txt')
    negative_words = read_dic('dic/nagative.txt')
    positive_count = count_data(analyse_data(data, positive_words))
    negative_count = count_data(analyse_data(data, negative_words))
    return [positive_count, negative_count]

