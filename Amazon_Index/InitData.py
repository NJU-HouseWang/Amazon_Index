# -*- encoding:utf-8 -*-
from Trendata import *


def calc_cate_sales_turnover():
    cate_list = get_category_list()
    for single_cate in cate_list:
        print '---' + single_cate
        cate_sales = 0
        cate_turnover = 0
        asin_list = get_category_asin_list(single_cate)
        for single_asin in asin_list:
            data = get_commodity_data(single_asin)
            if data:
                price = get_avg_price(data)
                if not price:
                    price = get_latest_price(data)
                sales = data['stats_info']['review_count']
                if not price and sales:
                    cate_sales += sales
                    cate_turnover += price
            else:
                print 'Error: Empty Commodity Data'
        print '---' + str(sales)
        print '---' + str(price)


if __name__ == "__main__":
    calc_cate_sales_turnover()