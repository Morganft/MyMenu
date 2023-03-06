from django import forms


class ImageWidget(forms.widgets.ClearableFileInput):
    template_name = 'field_image.html'
