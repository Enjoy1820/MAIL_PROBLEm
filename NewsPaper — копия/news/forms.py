from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'author',
            'text',
            'category',
        ]


def clean_text(self):
    cleaned_data = super().clean()
    text = cleaned_data.get("text")
    if text is not None and len(text) < 20:
        raise ValidationError({
            "text": "Описание не может быть менее 20 символов."
        })

    return cleaned_data

def clean(self):
    cleaned_data = super().clean()
    author = cleaned_data['author']
    today = date.today()
    post_limit = Post.objects.filter(author=author, date_in__date=today).count()
    if post_limit >= 3:
        raise ValidationError('Нельзя публиковать больше трех постов в сутки!!!')
    return cleaned_data