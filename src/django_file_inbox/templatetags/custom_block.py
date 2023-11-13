from django import template

register = template.Library()


@register.simple_tag
def customblock():
    """
    Dummy tag so the template compiles
    """


@register.simple_tag
def endcustomblock():
    """
    Dummy tag so the template compiles
    """
