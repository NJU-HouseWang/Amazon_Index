# -*- encoding:utf-8 -*-
from Trendata import *


def calc_cate_sales_turnover():
    al_f = open('d:/tmp1.txt', 'r')
    al_l = al_f.read().split('\n')
    al_cates = []
    for l in al_l:
        al_cates += [l.split('--')[0]]
    print len(al_cates)

    result_dict = {}
    cate_list = get_category_list()
    file_object = open('d:/tmp.txt', 'w')
    for single_cate in cate_list:
        if single_cate not in al_cates:
            result_dict[single_cate] = {'sales': 0, 'turnover': 0}
            asin_list = get_category_asin_list(single_cate)
            for single_asin in asin_list:
                try:
                    data = get_commodity_data(single_asin)
                except Exception, e:
                    print e
                    continue
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

            file_object.write(single_cate + '--' + str(result_dict[single_cate]['sales']) + '--' + str(result_dict[single_cate]['turnover']) + '\r\n')
    file_object.close()
    print '==========================RESULT=========================='
    print str(result_dict)
    file1_object = open('d:/turnover.txt','w')
    file1_object.write(str(result_dict))
    file1_object.close()

if __name__ == "__main__":
    calc_cate_sales_turnover()
