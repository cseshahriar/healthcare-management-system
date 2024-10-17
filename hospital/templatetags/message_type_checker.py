from django import template

register = template.Library()


@register.filter
def message_check(take_message):
    print('----------------msg ')
    try:
        if str(take_message.tags) == "warning":
            return True
        else:
            return False
    except Exception:
        return True
