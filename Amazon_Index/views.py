from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.template import Context
import CategoryLogic
import CommodityLogic
import Trendata
import datetime

def hello(request):
    ua = request.META.get('HTTP_USER_AGENT', 'unknown')
    return HttpResponse("Your browser is %s" % ua)
    #return HttpResponse("Welcome to the page at %s" % request.path)
    #return HttpResponse("Hello world")

def meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

def index(request):
    t = get_template('index.html')
    tags = CategoryLogic.get_category_tags()
    html = t.render(Context({"cate_tags": tags}))
    return HttpResponse(html)

def category(request):
    t = get_template('category.html')
    old_request = "&" + request.GET.urlencode()
    if 'tf' in request.GET:
        search_tag = request.GET['tf']
        cate_list = CategoryLogic.get_js_category_list()
        category_list = CategoryLogic.search_category(search_tag)
        category_sp = category_list[0].split(">")
        for i in range(len(category_sp)) :
            category_sp[i] = category_sp[i].replace("&","$")
        
        result_list = []
        for single_cate in category_list:
            asin_list = Trendata.get_category_asin_list(single_cate)
            for single_asin in asin_list:
                data = Trendata.get_commodity_data(single_asin)
                info = CommodityLogic.get_commodity_info(data)
                if info['commodity_name'] != "":
                    info['star_pic_width'] = int(8+29*float(info['commodity_avg_star']))
                    result_list += [info]
        html = t.render(Context(locals()))
        return HttpResponse(html)
    elif 'cate1' in request.GET:
        category = request.GET['cate1']
        for i in range(2,5):
            if request.GET['cate' + str(i)] != "":
                category = category + '>' + request.GET['cate' + str(i)]
        return HttpResponse(category)
    else:
        message = 'You submitted an empty form.'
        return HttpResponse(message)

def commodity(request):
    html = "error"
    if 'asin' in request.GET:
        html = "You are at commodity " + request.GET['asin']

    return HttpResponse(html)
    
def time(request):
    now = datetime.datetime.now()
    html = "<html>\n<body>\n<p>It is now %s.</p></body></html>" % now
    return HttpResponse(html)

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)
