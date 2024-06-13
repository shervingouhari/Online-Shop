from django import template
from django.conf import settings
from django.utils.translation import get_language
from persiantools.jdatetime import JalaliDate
from persiantools.digits import en_to_fa


register = template.Library()


@register.filter
def intcomma(number):
    try:
        return f'{int(number):,}'
    except:
        return number


@register.filter(name='sub')
def subtract(number1, number2):
    return number1 - number2


@register.filter(name='P')
def to_price(number):
    lan = get_language()
    if lan == 'en':
        return f'{intcomma(number)} IRT'
    elif lan == 'fa':
        return f'{en_to_fa(str(intcomma(number)))} تومان'
    return number


@register.filter(name='getattr')
def get_attribute(obj, arg):
    try:
        return obj[arg]
    except KeyError:
        return obj[settings.LANGUAGE_CODE]


@register.simple_tag(name='date_trans')
def date_translator(date):
    lan = get_language()
    if lan == 'en':
        return date.strftime('%Y-%m-%d')
    elif lan == 'fa':
        date = JalaliDate.to_jalali(date.year, date.month, date.day)
        return en_to_fa(str(date.strftime('%Y/%m/%d')))
    return date.strftime('%Y-%m-%d')


@register.simple_tag(name='num_trans')
def number_translator(number):
    lan = get_language()
    if lan == 'en':
        return number
    elif lan == 'fa':
        return en_to_fa(str(number))
    return number
