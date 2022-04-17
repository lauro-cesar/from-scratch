import imp
from django import template
import json
register = template.Library()
from django.urls import reverse

@register.filter(name="add_attr")
def add_attr(field, css):
    attrs = {}
    definition = css.split(",")

    for d in definition:
        if ":" not in d:
            attrs["class"] = d
        else:
            key, val = d.split(":")
            attrs[key] = val

    return field.as_widget(attrs=attrs)


@register.filter(name="debug_me")
def debug_me(value):
    print(dir(value))  
    return value


@register.filter(name="is_right_msg")
def is_left_msg(v_1,v_2):
    l = [str(v_1)]
    if (str(v_2) in l):
        return "right"
    return "left"


@register.filter(name="active_item")
def active_item(v_1,v_2):
    l = [str(v_1)]
    if (reverse(str(v_2)) in l):
        return "menu-open active selected"
    return ""


@register.filter(name="active_class")
def active_class(v_1,v_2):
    l = [str(v_1)]
    if (str(v_2) in l):
        return "active selected"
    return ""


@register.filter(name="is_active_option")
def is_active_option(v_1,v_2):
    l = [str(v_1)]
    if (str(v_2) in l):
        return "active selected"
    return ""



@register.filter(name="debug_me")
def debug_me(value):
    print(dir(value))  
    return value


@register.filter(name="sum_float")
def sum_float(value,arg):
    return value + arg


@register.filter(name="x_or_none")
def x_or_none(value,arg):
    return value + arg