from rest_framework.pagination import LimitOffsetPagination, NotFound
from rest_framework.response import Response
from rest_framework import status


class DefaultLimitOffsetPagination(LimitOffsetPagination):
    max_limit = 20
    default_limit = 10

    def generate_response(self, query_set, serializer_obj, request):
        try:
            page_data = self.paginate_queryset(query_set, request)
        except NotFound:
            return Response(
                {"error": "No results found for the requested page"},
                status=status.HTTP_400_BAD_REQUEST)

        serialized_page = serializer_obj(page_data, many=True)
        return self.get_paginated_response(serialized_page.data)
