from django import template

register = template.Library()


@register.filter(name='change')
def change(value):
    return value.replace(":",",")

@register.filter(name='tolist')
def tolist(value):
    value = value[:-1]
    lst=value.split(',')
    return lst

    
    
