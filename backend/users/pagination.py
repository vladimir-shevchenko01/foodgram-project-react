from rest_framework.pagination import PageNumberPagination


class CustomSubscribeListPagination(PageNumberPagination):
    page_size = 1