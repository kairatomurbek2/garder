from django import template


register = template.Library()

@register.inclusion_tag('partial/google_map.html')
def load_google_map_js():
    return {}