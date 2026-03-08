from django_filters import rest_framework as filters


class DashboardFilterSet(filters.FilterSet):
    period = filters.CharFilter(field_name="period")
    site = filters.CharFilter(field_name="site")
