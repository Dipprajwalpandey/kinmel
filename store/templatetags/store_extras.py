from django import template

register = template.Library()


@register.filter
def star_icons(rating):
    """Given a numeric average rating (0-5), return a list of 5 icon
    types: 'full', 'half', or 'empty' — for rendering star icons."""
    try:
        rating = float(rating)
    except (TypeError, ValueError):
        rating = 0.0

    full = int(rating)
    remainder = rating - full
    half = 1 if remainder >= 0.5 else 0
    empty = 5 - full - half

    return (['full'] * full) + (['half'] * half) + (['empty'] * empty)