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

    commodity_info['commodity_avg_price'] = round(get_avg_price(data), 2)

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

def get_star_count(data):
    star_list = [float(single_review['star'].split()[0]) \
                 for single_review in data['review']]
    dic = count(star_list)
    star_count = [0,0,0,0,0]
    if(dic.has_key(1.0)):
        star_count[0] = dic[1.0]
    if(dic.has_key(2.0)):
        star_count[1] = dic[2.0]
    if(dic.has_key(3.0)):
        star_count[2] = dic[3.0]
    if(dic.has_key(4.0)):
        star_count[3] = dic[4.0]  
    if(dic.has_key(5.0)):
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