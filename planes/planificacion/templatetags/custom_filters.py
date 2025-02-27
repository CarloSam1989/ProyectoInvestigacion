from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Permite acceder a un diccionario en los templates de Django."""
    return dictionary.get(key, None)
