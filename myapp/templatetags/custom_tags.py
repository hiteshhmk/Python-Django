from django import template

register = template.Library()


@register.simple_tag()
def get_halfContent(postDetail):
    return postDetail[:int(len(postDetail) / 3)]
