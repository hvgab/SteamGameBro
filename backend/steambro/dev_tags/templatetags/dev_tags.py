from django import template
import json

register = template.Library()

@register.filter
def json_dumps(value):
    return json.dumps(value)

@register.filter
def dump(object):
    fields = object._meta.get_fields()
    return fields