from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class CustomLimitPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10


class CustomPagePagination(PageNumberPagination):
    page_size = 2