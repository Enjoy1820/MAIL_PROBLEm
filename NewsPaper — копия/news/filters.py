from django_filters import FilterSet, DateFilter
from django.forms import DateInput
from .models import Post

class PostFilter(FilterSet):
    create_time = DateFilter(
        field_name='date_in',
        widget=DateInput(attrs={'type': 'date'}),
        label='Дата',
        lookup_expr='date__gte',
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['exact'],

        }