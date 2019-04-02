from django import forms


class ImageProcessingFrom(forms.Form):
    CHOICES = [
        ('none', 'None'),
        ('rgb', 'RGB'),
        ('hsv', 'HSV (Brightness)')
    ]

    add_constant = forms.IntegerField(required=False)
    multiply_constant = forms.FloatField(required=False,
                                           label="Multiply by a constant")
    power_transform = forms.FloatField(required=False)
    logarithmic_transformation = forms.BooleanField(required=False)
    negative = forms.BooleanField(required=False)
    linear_contrasting = forms.BooleanField(required=False)
    histogram_equalization = forms.ChoiceField(required=False,
                                               choices=CHOICES)


class ChooseImageFrom(forms.Form):
    image = forms.ImageField()
