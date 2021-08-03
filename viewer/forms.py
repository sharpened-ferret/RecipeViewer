from django import forms

class AddRecipeForm(forms.Form):
    url = forms.URLField(label="URL")
