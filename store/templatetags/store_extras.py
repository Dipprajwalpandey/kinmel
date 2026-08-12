from datetime import date, timedelta
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


@register.filter
def is_new(pub_date):
    """True if the product was published within the last 14 days.
    Uses the real pub_date field — no fabricated data."""
    if not pub_date:
        return False
    return (date.today() - pub_date).days <= 14