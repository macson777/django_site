from django import forms


class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    phone = forms.CharField(max_length=13, min_length=13)
    message = forms.CharField(max_length=500)
