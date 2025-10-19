from django import template

register = template.Library()


@register.filter
def humanize_duration(days):
    """
    Convert days to a human-readable duration format.
    Examples:
        30 days -> "1 Month"
        90 days -> "3 Months"
        365 days -> "1 Year"
        7 days -> "1 Week"
    """
    if not days:
        return "N/A"

    days = int(days)

    # Check for years
    if days >= 365:
        years = days // 365
        return f"{years} Year{'s' if years > 1 else ''}"

    # Check for months (approximate)
    if days >= 30:
        months = days // 30
        return f"{months} Month{'s' if months > 1 else ''}"

    # Check for weeks
    if days >= 7:
        weeks = days // 7
        return f"{weeks} Week{'s' if weeks > 1 else ''}"

    # Return days
    return f"{days} Day{'s' if days > 1 else ''}"
