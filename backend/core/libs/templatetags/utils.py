

import logging
from django.template.defaulttags import register
from django.utils.html import format_html


@register.filter
def blod_text(text):
    return format_html('<b>%s</b>' % text)