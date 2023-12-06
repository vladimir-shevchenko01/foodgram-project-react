from django_filters import CharFilter, FilterSet

from components.models import IngredientModel


class IngredientFilterSet(FilterSet):
    
    @classmethod 
    def get_filter_name(cls, field_name, lookup_expr):
        if field_name == 'name':
            return 'name'
    
    class Meta:
        model = IngredientModel
        fields = {
            'name': ['istartswith']
        }
