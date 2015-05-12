from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def planet_in_sign(request, planet, sign):
    params = dict()
    params['planet'] = planet
    params['sign'] = sign
    return render(request, 'interpretation/planet_in_sign.html', params)