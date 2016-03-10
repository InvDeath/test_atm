from django import template

register = template.Library()


@register.inclusion_tag('atm/keyboard_tag.html')
def keyboard(input_css_id, **kwargs):
    tag_context = {
        'input_css_id': input_css_id,
        'with_exit': kwargs.get('with_exit', False)
    }
    return tag_context
