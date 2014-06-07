from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.template import Context
import CategoryLogic
import CommodityLogic
import Trendata
import copy


def index(request):
    t = get_template('index.html')
    tags = CategoryLogic.get_category_tags()
    html = t.render(Context({"cate_tags": tags}))
    return HttpResponse(html)


def category(request):
    page_title = ''
    t = get_template('category.html')
    # old request
    old_get_request = request.GET
    old_request = '&' + request.GET.urlencode()
    tmp_get = copy.deepcopy(request.GET)
    # full category list from trendata
    full_cate_list = Trendata.get_category_list()
    # transfer category list to js select type
    js_cate_list = CategoryLogic.get_js_category_list(full_cate_list)
    # which category type
    if 'tf' in old_get_request:
        page_title = old_get_request['tf'] + ' -- Search Result'
        search_result_dict = CategoryLogic.search_category(full_cate_list, old_get_request['tf'].split(' '))
    elif 'cate1' in request.GET:
        category_selected = request.GET['cate1']
        for i in range(2, 5):
            if request.GET['cate' + str(i)] != "":
                category_selected += '>' + request.GET['cate' + str(i)]
        search_result_dict = CategoryLogic.choose_category(full_cate_list, category_selected.replace('$', "&"))
        page_title = search_result_dict['cate_show'].replace('&', 'and') + ' -- Category'
    else:
        raise Http404
        return HttpResponse("")

    result_cate_list = search_result_dict['cate_list']
    show_cate_sp = search_result_dict['cate_show'].split('>')
    # get list to show
    for i in range(len(show_cate_sp)):
        show_cate_sp[i] = show_cate_sp[i].replace("&", "$")

    result_list = []
    for single_cate in result_cate_list:
        asin_list = Trendata.get_category_asin_list(single_cate)
        for single_asin in asin_list:
            data = Trendata.get_commodity_data(single_asin)
            info = CommodityLogic.get_commodity_info(data)
            if info['commodity_name'] != "":
                info['star_pic_width'] = int(8 + 29 * float(info['commodity_avg_star']))
                result_list += [info]

    statistics_data = CategoryLogic.get_category_sales_statistics(search_result_dict['cate_show'])

    # if sort
    sort_tag = {'name': '(up)', 'avg_price': '(up)', 'sales': '(down)', 'avg_star': '(down)'}
    rev = {'name': False, 'avg_price': False, 'sales': True, 'avg_star': True}
    href_tag = {'name': '', 'avg_price': '', 'sales': '', 'avg_star': ''}
    if 'sortby' in old_get_request:
        if request.GET['sortby'][-1] == '_':
            result_list = sorted(result_list, key=lambda e: e['commodity_' + request.GET['sortby'][:-1]],
                                 reverse=not rev[request.GET['sortby'][:-1]])
        else:
            result_list = sorted(result_list, key=lambda e: e['commodity_' + request.GET['sortby']],
                                 reverse=rev[request.GET['sortby']])
            if sort_tag[request.GET['sortby']] == '(down)':
                sort_tag[request.GET['sortby']] = '(up)'
            else:
                sort_tag[request.GET['sortby']] = '(down)'
            href_tag[request.GET['sortby']] = '_'
        tmp_get.pop('sortby')
    old_request = '&' + tmp_get.urlencode()
    html = t.render(Context(locals()))

    return HttpResponse(html)


def commodity(request):
    t = get_template('commodity.html')
    html = "error"
    if 'asin' in request.GET:
        asin = request.GET['asin']
        data = Trendata.get_commodity_data(asin)
        info = CommodityLogic.get_commodity_info(data)
        star_count = CommodityLogic.get_star_count(data)
        price_info = CommodityLogic.get_price_info(data)
        earliest_date = str((price_info['earliest_time']).year) + "-" + str(
            (price_info['earliest_time']).month) + "-" + str((price_info['earliest_time']).day)
        latest_date = str((price_info['latest_time']).year) + "-" + str((price_info['latest_time']).month) + "-" + str(
            (price_info['latest_time']).day)
        time_list = (price_info['time_list'])
        lowest_price = (price_info['lowest_price'])
        highest_price = (price_info['highest_price'])
        avg_price = (price_info['avg_price'])
        if info['commodity_name'] != "":
            info['star_pic_width'] = int(8 + 29 * float(info['commodity_avg_star']))
        html = t.render(Context(locals()))
        return HttpResponse(html)

    return HttpResponse(html)