from django import template
from pages.models import FooterText

register = template.Library()
@register.inclusion_tag('partials/_footer_inclusion.html')
def show_description():
    contents = FooterText.objects.first()
    return {'contents':contents}
