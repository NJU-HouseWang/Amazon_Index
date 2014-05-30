# -*- encoding:utf-8 -*-

from datetime import datetime
# from matplotlib.patches import Polygon
# from matplotlib.ticker import MaxNLocator
# import pylab
# import matplotlib.pyplot as plt
# import numpy as np
import os

import urllib
import simplejson as json


ROOT_URL = "http://112.124.1.3:8004"
CATEGORY_URL = "api/commodity"


def get_category_list():
    """
    得到分类列表
    """
    file_obj = open('D:\\trendata/category.txt','r')
    #cate_list_data = json.loads(file_obj.read())
    category = file_obj.read().split('/n')
    file_obj.close()
    category_list = []
    for single_cate in category:
        category_list += [single_cate]
    return category_list


def get_category_asin_list(cate):
    """
    得到一个分类下所有商品的编号
    """
    cate = cate.split('>')
    print cate
    asin_list = []
    commodity_data = []
    first_commodity_data_name = []
    for index in range(0,117):
        path = 'D:/trendata/'+str(index)
        list  = os.listdir(path)
        if os.listdir(path):
           list1 = os.listdir(path)[0]
           file_obj = open('D:\\trendata/'+str(index)+'/'+list1,'r')
           first_commodity_data = json.loads(file_obj.read())
           print first_commodity_data
           file_obj.close()
           if (str(first_commodity_data['category'][0]).startswith(str(cate))):
                for each_asin_txt in list:
                    file_obj = open('D:\\trendata/'+str(index)+'/'+each_asin_txt,'r')
                    commodity_data += json.loads(file_obj.read())
                for each_commodity in commodity_data:
                    asin_list += each_commodity['ASIN']
    return asin_list



def get_commodity_data(asin):
    """
    得到某个商品的json型数据
    """
    for index in range(0,117):
        path = 'D:\\trendata'+'/'+str(index)
        list = os.listdir(path)
        for each_asin_txt in list:
            each_asin = each_asin_txt.split('.')[0]
            if (asin == each_asin):
                file_obj = open('D:\\trendata/'+str(index)+'/'+each_asin_txt,'r')
                return json.loads(file_obj.read())
                file_obj.close()
    print 'asin not exists'
    return -1

def get_category_top_sales_asin_list(cate, top_count):
    """
    得到某个分类下销量最高的几个商品asin
    调用了get_category_asin_list，get_commodity_data
    返回{'asin':*,'sales':*}
    """
    category_asin_list = get_category_asin_list(cate)
    asin_sales_list = []
    for asin in category_asin_list:
        commodity_data = get_commodity_data(asin)
        asin_sales = {'asin': asin, 'sales': len(commodity_data['review'])}
        asin_sales_list += [asin_sales]
    asin_sales_list = sorted(asin_sales_list, key=lambda e: e['sales'], reverse=True)
    return asin_sales_list[:top_count]


def get_commodity_name(raw_data):
    return raw_data['productInfo'][0]['name']


def get_avg_price(data):
    """
    得到一个商品的历史平均价格
    """
    list = []
    # 提取整体价格数据
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
    print list
    list = sorted(list, key=lambda e: e[2], reverse=False)

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
                        tmplist += [[seller, tmpsumprice / tmpcount, tmptime]]
                    tmptime = item[2]
                    tmpsumprice = item[1]
                    tmpcount = 1
        if tmptime != None:
            tmplist += [[seller, tmpsumprice / tmpcount, tmptime]]
        seller_price_dict[seller] = tmplist

    #print seller_list
    #print seller_price_dict
    total_price_list = []
    for seller in seller_list:
        # 时间加权，计算一个商家的平均售价
        current_price_list = seller_price_dict[seller]
        print current_price_list
        i = 0
        sum = 0
        if len(current_price_list) > 2:
            while i < len(current_price_list) - 2:
                sum += current_price_list[i][1] * (current_price_list[i + 1][2] - current_price_list[i][2]).seconds
                i = i + 1
            print sum / (current_price_list[len(current_price_list) - 1][2] - current_price_list[0][2]).seconds
            total_price_list += [
                sum / (current_price_list[len(current_price_list) - 1][2] - current_price_list[0][2]).seconds]
        elif len(current_price_list) == 2:
            print (current_price_list[0][1] + current_price_list[1][1]) / 2
            total_price_list += [(current_price_list[0][1] + current_price_list[1][1]) / 2]
        else:
            print current_price_list[0][1]
            total_price_list += [current_price_list[0][1]]

    sum = 0
    for price in total_price_list:
        sum += price
    if len(total_price_list) != 0:
        avg = sum / len(total_price_list)
    else:
        print "Error Occured"
        return 0
    print "Average: " + str(avg)
    return avg


if __name__ == '__main__':
   # cate_list = get_category_list()
   # print cate_list
    #asin = 'B000YFNZLC'
   # data = get_commodity_data(asin)
    cate = 'Baby Products>Diapering>Diaper Bags'
    print get_category_asin_list(cate)
    pass
