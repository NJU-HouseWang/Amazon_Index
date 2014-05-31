# -*- encoding:utf-8 -*-
from Trendata import *


def calc_cate_sales_turnover():
    result_dict = {}
    cate_list = get_category_list()

    for single_cate in cate_list:
        result_dict[single_cate] = {'sales': 0, 'turnover': 0}
        asin_list = get_category_asin_list(single_cate)
        for single_asin in asin_list:
            data = get_commodity_data(single_asin)
            if data:
                price = get_avg_price(data)
                if not price:
                    price = get_latest_price(data)
                sales = data['stats_info']['review_count']
                if not (price and sales):
                    result_dict[single_cate]['sales'] += sales
                    result_dict[single_cate]['turnover'] += price
            else:
                print 'Error: Empty Commodity Data'
        print single_cate + '--' + str(result_dict[single_cate]['sales']) + '--' + str(result_dict[single_cate]['turnover'])
        file_object = open('tmp.txt','w+')
        file_object.write(single_cate + '--' + str(result_dict[single_cate]['sales']) + '--' + str(result_dict[single_cate]['turnover']) + '\r\n')
        file_object.close()
    print '==========================RESULT=========================='
    print str(result_dict)
    file_object = open('turnover.txt','w')
    file_object.write(str(result_dict))
    file_object.close()

if __name__ == "__main__":
    calc_cate_sales_turnover()
