# coding: utf-8
from django.utils.translation import ugettext_lazy as _

SIGNS = [('aries', _(u'Aries')),
             ('taurus', _(u'Taurus')),
             ('gemini', _(u'Gemini')),
             ('cancer', _(u'Cancer')),
             ('leo', _(u'Leo')),
             ('virgo', _(u'Virgo')),
             ('libra', _(u'Libra')),
             ('scorpio', _(u'Scorpio')),
             ('sagittarius', _(u'Sagittarius')),
             ('capricorn', _(u'Capricorn')),
             ('aquarius', _(u'Aquarius')),
             ('pisces', _(u'Pisces'))]

PLANET_NAMES = {'sun': _('Sun'),
            'moon': _('Moon'),
            'mercury': _('Mercury'),
            'venus': _('Venus'),
            'mars': _('Mars'),
            'jupiter': _('Jupiter'),
            'saturn': _('Saturn'),
            'uranus': _('Uranus'),
            'neptune': _('Neptune'),
            'pluto': _('Pluto'),
            'mean_node': _('Mean_Node'),
            'true_node': _('True_Node'),
            'mean_apog': _('Mean_Apog'),
            'oscu_apog': _('Oscu_Apog'),
            'earth': _('Earth'),
            'chiron': _('Chiron'),
            'pholus': _('Pholus'),
            'ceres': _('Ceres'),
            'pallas': _('Pallas'),
            'juno': _('Juno'),
            'vesta': _('Vesta'),
            'intp_apog': _('Intp_Apog'),
            'intp_perg': _('Intp_Perg'),
            }



def dms(angle_float):

    angle = abs(angle_float)
    d = int(angle)
    m = int((angle - d) * 60)
    s = int((angle - d - m/60.0) * 3600)
    d = int(angle_float)

    if s:
        return '%d %d %d' % (d,  m, s)
    elif m:
        return '%d %d' % (d,   m)
    else:
        return '%d' % (d)