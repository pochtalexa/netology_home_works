from django import template

register = template.Library()


@register.filter
def my_set_color(cell_val):
    if isinstance(cell_val, str):
        return ''

    if cell_val < 0:
        return 'less_0'
    elif 0 <= cell_val < 1:
        return 'between_0_1'
    elif 1 <= cell_val < 2:
        'between_1_2'
    elif 2 <= cell_val < 5:
        return 'between_2_5'
    else:
        return 'more_5'
