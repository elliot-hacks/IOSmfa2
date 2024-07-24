from django import forms

class FingerprintForm(forms.Form):
    fingerprint_image = forms.ImageField()
