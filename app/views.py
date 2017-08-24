from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from operator import itemgetter
from .wordcloud import *
from .utils import *

@csrf_exempt
def updateTable(request): # /update
    pub_s = int(request.POST.get("pub_syear"))
    pub_e = int(request.POST.get("pub_eyear"))
    cit_s = int(request.POST.get("cit_syear"))
    cit_e = int(request.POST.get("cit_eyear"))
    weight = request.POST.get("weight")
    conflist = request.POST.get("conflist")
    # print(conflist, [pub_s, pub_e], [cit_s, cit_e], weight)
    data = getPaperScore(conflist.split(' '), [pub_s, pub_e], [cit_s, cit_e], weight!="equal")
    return JsonResponse(data, safe=False)

@csrf_exempt
def selectKeyword(request): # /select
    keywords = request.POST.get("keyword")

    conf = []
    for key in keywords.split(','):
        conf.extend(getVenueList(key.lower()))
    set_conf = list(set(conf))
    sorted_conf = sorted(set_conf, key=itemgetter(2), reverse=True)
    return JsonResponse(sorted_conf, safe=False)

def main(request):
    loadData()
    tags = createCategorycloud()
    return render(request, "main.html", {
        "words": {
            "title": "Institutional Publication Metrics for Computer Science",
            "label_year": "Year",
            "label_category": "Category",
            "slider_desc": "Year of publication",
            "forward": "Estimated",
            "forward_tooltip": "Estimated impact is calculated by the number of publication",
            "forward_info": "Estimated Impact",
            "backward": "Measured",
            "backward_tooltip": "Measured impact is calculated by the number of citations",
            "backward_info": "Measured Impact",
            "ctable_label_0": "Abbr.",
            "ctable_label_1": "Conference",
            "ctable_label_2": "Venue Weight",
            "ctable_label_2_tooltip": "Venue Weight is either Equal or Geometric mean of the citation count/paper count",
            "select_weight_option_equal": "Equal",
            "select_weight_option_geo": "Geo Mean",
            "rank_button": "Rank",
            "select_region_all": "all",
            "select_region_inlist": "CRA members only",
            "rtable_label_0": "Rank",
            "rtable_label_1": "Institution",
            "rtable_label_2": "Measured",
            "rtable_label_3": "Estimated",
            "rtable_label_4": "Combined",
        },
        "tags": tags
    })
