from django import forms
# from.models import Tag
# from django.core.exceptions import ValidationError

class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    phone = forms.CharField(max_length=13, min_length=13)
    message = forms.CharField(max_length=500)


    # def clean_slug(self):
    #     new_slug = self.cleaned_data['slug'].lower()
    #     if new_slug == 'create':
    #         raise ValidationError("Slug may not be 'create'")
    #     return new_slug


    # def save(self):
    #     new_form = Form.objects.create(name=self.cleaned_data['title'],
    #                                  email=self.cleaned_data['email']
    #                                  phone=self.cleaned_data['phone']
    #                                  message=self.cleaned_data['message']
    #                                  )
    #     return new_form