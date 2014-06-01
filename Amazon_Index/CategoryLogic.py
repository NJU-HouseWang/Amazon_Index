from Trendata import *
import CategorySearcher


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
                    new_tag = tag3_t.replace(',', '').replace('\'', '').strip()
                    if new_tag not in tags:
                        if len(new_tag) > 1:
                            tags += [new_tag]
    tags.sort()
    for tag in tags:
        tag = tag.replace('&amp;', '&')
    print '  '.join(tags)
    return tags


def search_category(full_cate_list, name):
    return CategorySearcher.search(full_cate_list, name)


def get_js_category_list(cate_list):
    js_cate_list = []
    for cate in cate_list:
        sp_cate = cate.split('>')
        for cate_item in sp_cate:

            if sp_cate.index(cate_item) == 0:
                if [cate_item.replace('&', '$'), 'root', cate_item.replace('&', 'and')] not in js_cate_list:
                    js_cate_list += [[cate_item.replace('&', '$'), 'root', cate_item.replace('&', 'and')]]
            else:
                if [cate_item.replace('&', '$'), sp_cate[sp_cate.index(cate_item) - 1].replace('&', '$'),
                    cate_item.replace('&', 'and')] not in js_cate_list:
                    js_cate_list += [
                        [cate_item.replace('&', '$'), sp_cate[sp_cate.index(cate_item) - 1].replace('&', '$'),
                         cate_item.replace('&', 'and')]]
    return js_cate_list


def choose_category(category_list, cate):
    result_dict = {'cate_show': cate, 'cate_list': []}

    for single_cate in category_list:
        if single_cate.startswith(cate):
            result_dict['cate_list'] += [single_cate]
    return result_dict


def get_category_sales_statistics(cate):
    root_cate = 'amazon'
    cate_sp = cate.split('>')
    if len(cate_sp) > 1:
        cate_sp = cate_sp[:-1]
        root_cate = '>'.join(cate_sp)

    t_file = open('turnover.txt', 'r')
    data_list = t_file.read().split('\n')
    t_file.close()

    data_chose = []
    result = {'sales_statistics': [], 'turnover_statistics': []}
    if root_cate != 'amazon':
        for data_line in data_list:
            if data_line.startswith(root_cate):
                tmp = data_line.split('--')
                if len(tmp) == 2:
                    tmp[2] = 0
                name = [i for i in tmp[0].split('>') if i not in root_cate.split('>')][0]
                if tmp[0] == cate:
                    result['sales_statistics'] += [[name.replace("&", "$"), tmp[1], 1]]
                    result['turnover_statistics'] += [[name.replace("&", "$"), tmp[2], 1]]
                else:
                    result['sales_statistics'] += [[name.replace("&", "$"), tmp[1], 0]]
                    result['turnover_statistics'] += [[name.replace("&", "$"), tmp[2], 0]]
    else:
        etc_sales = 0
        etc_turnover = 0
        for data_line in data_list:
            tmp = data_line.split('--')
            if len(tmp) == 2:
                tmp[2] = 0
            if data_line.startswith(cate):
                result['sales_statistics'] += [[cate, tmp[1], 0]]
                result['turnover_statistics'] += [[cate, tmp[2], 0]]
            else:
                etc_sales += tmp[1]
                etc_turnover += tmp[2]
        result['sales_statistics'] += [['Other categories', etc_sales, 1]]
        result['turnover_statistics'] += [['Other categories', etc_turnover, 1]]
    return result