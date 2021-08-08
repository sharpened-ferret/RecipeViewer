from django import forms

class AddRecipeForm(forms.Form):
    url = forms.URLField(label="URL")

class SearchForm(forms.Form):
    searchTerm = forms.CharField(label="", label_suffix="")