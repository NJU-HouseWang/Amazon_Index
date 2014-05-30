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