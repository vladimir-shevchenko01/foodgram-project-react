from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    '''Количество объектов на странице.'''

    page_size_query_param = 'limit'
