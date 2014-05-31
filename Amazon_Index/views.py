from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.template import Context
import CategoryLogic
import CommodityLogic
import Trendata
import datetime


def index(request):
    t = get_template('index.html')
    tags = CategoryLogic.get_category_tags()
    html = t.render(Context({"cate_tags": tags}))
    return HttpResponse(html)


def category(request):
    t = get_template('category.html')
    # old request
    old_get_request = request.GET
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
    html = t.render(Context(locals()))
    return HttpResponse(html)


def commodity(request):
    html = "error"
    if 'asin' in request.GET:
        html = "You are at commodity " + request.GET['asin']

    return HttpResponse(html)