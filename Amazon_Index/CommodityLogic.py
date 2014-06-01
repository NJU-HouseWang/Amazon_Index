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
	
def get_price_info(data):
	list = []
	price_info = {}
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
				if type(price) == str:
					price = price.replace('$','')
					price = price.replace(',','')
				list += [[info['seller']['name'], float(price), datetime.strptime(info['timestamp'], "%Y-%m-%d %H:%M:%S")]]
	list = sorted(list,key=lambda e:e[2],reverse=False)
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
			for i in range(0,len(list)):
				if each_time == list[i][2]:
					price_list +=[list[i][1]]
			price_list.sort()
			lowest_price += [price_list[0]]
			highest_price += [price_list[-1]]
			avg_price +=[sum(price_list)/len(price_list)]
			price_list = []

		price_info['lowest_price'] = lowest_price
		price_info['highest_price'] = highest_price
		price_info['avg_price'] = avg_price
		tmp = [i for i in set(time_list)]
		tmp.sort(key=lambda x:x)
		tmp2 = []
		for item in tmp:
			tmp2+=[str(item.year)+str(item.month)+str(item.day)]
        price_info['time_list'] = tmp2

	return price_info
    
def handle_price_info(price_list, time_list):
    data = []
    for i in range(0,len(price_list)):
        year = (time_list[i]).year
        month = (time_list[i]).month
        day = (time_list[i]).day
        data += [year,month,day,price_list[i]]
    return data