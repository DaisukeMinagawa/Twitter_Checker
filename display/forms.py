from django import forms

from .models import TwitterUsers


class PostForm(forms.ModelForm):

    class Meta:
        model = TwitterUsers
        fields = ('name', 'comment',)
