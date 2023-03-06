from django import template

register = template.Library()


@register.filter
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__


@register.filter
def input_class(bound_field):
    css_class = ''
    base_class = 'form-control'
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class = 'is-invalid'
        elif field_type(bound_field) != 'PasswordInput':
            css_class = 'is-valid'

        if field_type(bound_field) == 'ImageInput':
            base_class = 'custom-file-input'
    return f'{base_class} {css_class}'


@register.filter
def group_class(bound_field):
    base_class = 'form-group'
    if field_type(bound_field) == 'ImageInput':
        base_class = 'custom-file'
    return f'{base_class}'
