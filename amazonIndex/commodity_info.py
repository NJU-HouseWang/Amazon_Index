#-*- encoding:utf-8 -*-


from datetime import date, datetime, timedelta
import numpy as np
import urllib
import simplejson as json

ROOT_URL = "http://112.124.1.3:8004"
CATEGORY_URL = "api/commodity"


def get_commodity_data(asin):
    """
    得到某个商品的json型数据
    """
    target_url = '/'.join([ROOT_URL, CATEGORY_URL, asin])
    print "## Fetching commodity_info ## " + target_url
    return json.loads(urllib.urlopen(target_url).read())

def get_commodity_info(data):
    commodity_info = {}
    commodity_name = data['productInfo'][0]['name']
    commodity_info['commodity_name'] = commodity_name

    sales = data['stats_info']['review_count']
    commodity_info['commodity_sales'] = sales

    avg_star = data['stats_info']['avg_info']
    commodity_info['commodity_avg_star'] = avg_star

    img_url = []

    for img in data['productInfo']:
        img_url += [img['img']]

    commodity_info['commodity_img'] = img_url

    list = []
    # 提取整体价格数据
    for offer in data['offer']:
        for info in offer['info']:
            if info['seller']['name'] == 'Null':
                price = info['price']
                if type(price) == str:
                    price = price.replace('$','')
                    price = price.replace(',','')
                list += [['Amazon', float(price), datetime.strptime(info['timestamp'], "%Y-%m-%d %H:%M:%S")]]
            else:
                price = info['price']
                price = info['price']
                if type(price) == str:
                    price = price.replace('$','')
                    price = price.replace(',','')
                list += [[info['seller']['name'], float(price), datetime.strptime(info['timestamp'], "%Y-%m-%d %H:%M:%S")]]
    #print list
    list = sorted(list,key=lambda e:e[2],reverse=False)

    # 按照商家分类(时间合并)
    seller_list = []
    seller_price_dict = {}
    for item in list:
        if item[0] not in seller_list:
            seller_list += [item[0]]
    for seller in seller_list:
        tmplist = []
        tmptime = None
        tmpsumprice = 0
        tmpcount = 0
        for item in list:
            if item[0] == seller:
                #如果时间和上次相同
                if item[2] == tmptime:
                    #累计时间和计算次数
                    tmpsumprice += item[1]
                    tmpcount += 1
                #如果时间和上次不同，输出上个时间的价格，记录本次
                else:
                    if tmptime != None:
                        tmplist += [[seller,tmpsumprice/tmpcount,tmptime]]
                    tmptime = item[2]
                    tmpsumprice = item[1]
                    tmpcount = 1
        if tmptime != None:
            tmplist += [[seller,tmpsumprice/tmpcount,tmptime]]
        seller_price_dict[seller] = tmplist

    #print seller_list
    #print seller_price_dict
    total_price_list = []
    for seller in seller_list:
        # 时间加权，计算一个商家的平均售价
        current_price_list = seller_price_dict[seller]
        #print current_price_list
        i = 0
        sum = 0
        if len(current_price_list) > 2:
            while i < len(current_price_list)-2:
                sum += current_price_list[i][1] * (current_price_list[i+1][2] - current_price_list[i][2]).seconds
                i = i+1
            #print sum/(current_price_list[len(current_price_list)-1][2] - current_price_list[0][2]).seconds
            total_price_list += [sum/(current_price_list[len(current_price_list)-1][2] - current_price_list[0][2]).seconds]
        elif len(current_price_list) == 2:
            #print (current_price_list[0][1] + current_price_list[1][1])/2
            total_price_list += [(current_price_list[0][1] + current_price_list[1][1])/2]
        else:
            #print current_price_list[0][1]
            total_price_list += [current_price_list[0][1]]

    sum = 0
    for price in total_price_list:
        sum += price
    if len(total_price_list) != 0:
        avg = sum/len(total_price_list)
    else:
        print "Error Occured"
    commodity_info['commodity_avg_price'] = avg

    return commodity_info

if __name__ == '__main__':
    asin = 'B0097WXC3Y'
    data = get_commodity_data(asin)
    print get_commodity_info(data)
    pass



