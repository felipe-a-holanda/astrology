#coding: utf-8
from django import template
from ..utils import SIGNS

register = template.Library()


DEGREE_SIGN = '°'

@register.filter(name='dms')
def dms(value):

    d = int(value)
    m = (value - d) * 60
    s = int((m - int(m)) * 60)
    m = int(m)

    if s:
        return '%d%s %d\' %d\"' % (d, DEGREE_SIGN, m, s)
    elif m:
        return '%d%s %d\'' % (d, DEGREE_SIGN,  m)
    else:
        return '%d%s' % (d, DEGREE_SIGN)

@register.filter(name='sign')
def sign(value):
    return SIGNS[int(value/30)][1]