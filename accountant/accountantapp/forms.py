from django.forms import ModelForm
from .models import Category, Actions


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class ActionsForm(ModelForm):
    class Meta:
        model = Actions
        fields = ['sum', 'category', 'type']
