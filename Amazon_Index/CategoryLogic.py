from Trendata import *

def get_category_tags():
    all_category_list = get_category_list()
    tags = []
    for cate in all_category_list:
        tag1 = cate.split('>')
        for tag1_t in tag1:
            new_tag = tag1_t.strip()
            if new_tag not in tags:
                if len(new_tag) > 1:
                    tags += [new_tag]
            tag2 = tag1_t.split('&')
            for tag2_t in tag2:
                new_tag = tag2_t.strip()
                if new_tag not in tags:
                    if len(new_tag) > 1:
                        tags += [new_tag]
                tag3 = tag1_t.split(' ')
                for tag3_t in tag3:
                    new_tag = tag3_t.replace(',','').replace('\'','').strip()
                    if new_tag not in tags:
                        if len(new_tag) > 1:
                            tags += [new_tag]
    tags.sort()
    for tag in tags:
        tag = tag.replace('&amp;','&')
    print '  '.join(tags)
    return tags


def search_category(name):
    all_category_list = get_category_list()
    category_list = []
    
    index = -1
    
    for category in all_category_list:
        category_split = category.split('>')
        if(category_split[2].lower().find(name.lower()) != -1):
            index = 2
        elif(category_split[1].lower().find(name.lower()) != -1):
            index = 1
        elif(category_split[0].lower().find(name.lower()) != -1):
            index = 0
        
    category_split1 = []
    for category in all_category_list:
        category_split1 = category.split('>')
        if(category_split1[index].lower().find(name.lower()) != -1):
            category_list.append(category)
            
    return category_list

def get_js_category_list():
    cate_list = get_category_list()
    js_cate_list = []
    for cate in cate_list:
        sp_cate = cate.split('>')
        for cate_item in sp_cate:
            
            if sp_cate.index(cate_item) == 0:
                if [cate_item.replace('&','$'),'root',cate_item.replace('&','and')] not in js_cate_list:
                    js_cate_list += [[cate_item.replace('&','$'),'root',cate_item.replace('&','and')]]
            else:
                if [cate_item.replace('&','$'),sp_cate[sp_cate.index(cate_item)-1].replace('&','$'),cate_item.replace('&','and')] not in js_cate_list:
                    js_cate_list += [[cate_item.replace('&','$'),sp_cate[sp_cate.index(cate_item)-1].replace('&','$'),cate_item.replace('&','and')]]
    print str(js_cate_list)
    return js_cate_list
