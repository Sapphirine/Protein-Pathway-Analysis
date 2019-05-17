import json
import pandas as pd
import numpy as np
import seaborn as sns
import os
import re
import urllib
from urllib.error import HTTPError
from urllib.request import urlopen
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from . import search,generator
from django.views.decorators import csrf
 




def search_form(request):
    return render_to_response('search_form.html')

def search(request):  
    request.encoding='utf-8'
    if 'q' in request.GET:
        p_list = request.GET['q']
    pro_list = p_list.split(",")
    generator.generate_json(pro_list)
#     generator.score_to_graph(pro_list)
#     generator.corr_to_json(pro_list)
#     generator.to_corr_json(pro_list)
    return render(request,'choose.html')
def choose(request):
    if 'corr' in request.GET:
        return render(request,'corr.html')
    elif 'str' in request.GET:
        return render(request,'str.html')
    elif 'corrmat' in request.GET:
        return render(request,'corrmat.html')
    elif 'clu' in request.GET:
        return render(request, 'hier.html')
          