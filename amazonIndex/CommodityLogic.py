from Trendata import *

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

    commodity_info['commodity_avg_price'] = round(get_avg_price(data),2)

    commodity_tags = data['stats_info']['keywords']
    tag = ''
    for tags_info in commodity_tags:
           tags_info.reverse()

    commodity_tags.sort()

    if(len(commodity_tags)<=4):
        for tags in commodity_tags:
            tag += tags[1] + " "

    else:
        for i in  range(4):
            tag += commodity_tags[i][1] + " "

    commodity_info['commodity_tags'] = tag

    return commodity_info

