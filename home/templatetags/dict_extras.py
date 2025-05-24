from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def dict_get(obj, key):
    try:
        return obj.get(key)
    except:
        return None
