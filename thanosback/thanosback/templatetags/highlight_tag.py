from django import template
#from re import IGNORECASE, compile, escape as rescape
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter
def highlight(text, search):
	highlighted = text.replace(search, '<span class="highlight">{}</span>'.format(search))
	print(highlighted)
	return mark_safe(highlighted)