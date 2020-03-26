"""
Search View Mixin to implement search in django list views
"""
from functools import reduce

from django.db.models import Q
from django.views.generic import ListView


class SearchView(ListView):
    """
    Implements search in ListView

    set search fields by defining iterable to `search_fields`

    :var search_param: Query Param used to send search values
    :var search fields: Iterable containing list of field names to search
    """
    search_param = "q"
    search_fields = None

    def get_search_parm(self):
        """Returns search param"""
        return self.search_param

    def get_search_fields(self):
        """Returns search fields (Iterable containing list of field names to search)"""
        if not self.search_fields:
            raise AttributeError(
                "%s must set `search_fields` "
                "attribute or define `get_search_fields`"
                % self.__class__
            )
        return self.search_fields

    def get_search_query(self):
        """
        Builds and returns search query Q object for search
        """
        fields = self.get_search_fields()
        search_value = self.get_search_value()
        if search_value:
            individual_queries = [Q(**{f"{field}__icontains": search_value}) for field in fields]

            return reduce(
                lambda q1, q2: q1 | q2,
                individual_queries
            )
        return Q()

    def get_search_value(self):
        """Extracts search value from request"""
        return self.request.GET.get(self.get_search_parm())

    def get_queryset(self):
        return self.search(super().get_queryset())

    def search(self, queryset):
        """Apply search to given queryset"""
        return queryset.filter(self.get_search_query())
