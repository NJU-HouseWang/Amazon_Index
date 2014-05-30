from Trendata import *


def get_cate_list(all_category_list, category_part):
    cate_list = []
    for category in all_category_list:
        if category.startswith(category_part):
            cate_list.append(category)
    return cate_list


def get_is_matched(name, category):
    check = False
    category_part_list = category.split(' ')
    for category_part in category_part_list:
        if category_part.lower() == name.lower():
            check = True
            break
    return check


def search(all_category_list, key_list):
    name_list = []
    for key in key_list:
        name_list += [key.lower()]
    category_dict = {'cate_show': '', 'cate_list': []}
    
    for category in all_category_list:
        category_split_list = category.split('>')
        
        check = True
        if len(category_split_list) == 4:
            for name in name_list:
                if not get_is_matched(name, category_split_list[3]):
                    check = False
            if check:
                category_dict['cate_show'] = category
                category_dict['cate_list'] = get_cate_list(all_category_list,category_dict['cate_show'])
                return category_dict
        
    for category in all_category_list:
        category_split_list = category.split('>')
        if len(category_split_list) >= 3:
            check = True
            for name in name_list:
                if not get_is_matched(name,category_split_list[2]):
                    check = False
            if check:
                category_dict['cate_show'] = category_split_list[0] + '>' + category_split_list[1] + '>' + category_split_list[2]
                category_dict['cate_list'] = get_cate_list(all_category_list, category_dict['cate_show'])
                return category_dict

    for category in all_category_list:
        category_split_list = category.split('>')
        if len(category_split_list) >= 2:
            check = True
            for name in name_list:
                if not get_is_matched(name, category_split_list[1]):
                    check = False
            if check:
                category_dict['cate_show'] = category_split_list[0] + '>' + category_split_list[1]
                category_dict['cate_list'] = get_cate_list(all_category_list,category_dict['cate_show'])
                return category_dict

    for category in all_category_list:
        category_split_list = category.split('>')
        check = True
        for name in name_list:
            if not get_is_matched(name, category_split_list[0]):
                check = False
                break
        if check:
            category_dict['cate_show'] = category_split_list[0]
            category_dict['cate_list'] = get_cate_list(all_category_list, category_dict['cate_show'])
            return category_dict

    return category_dict
