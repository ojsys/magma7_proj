from django import template

register = template.Library()


@register.filter(name="add_class")
def add_class(field, css_classes: str):
    """Add CSS classes to a form field widget when rendering.
    Usage: {{ form.field|add_class:"my-class another" }}
    """
    existing = field.field.widget.attrs.get("class", "")
    classes = f"{existing} {css_classes}".strip()
    attrs = {**field.field.widget.attrs, "class": classes}
    return field.as_widget(attrs=attrs)

