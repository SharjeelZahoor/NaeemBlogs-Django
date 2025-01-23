from django import template

register = template.Library()

@register.filter
def endswith(value, suffix):
    """
    Checks if the given value ends with the specified suffix.
    """
    return str(value).lower().endswith(suffix.lower())
