from rest_framework import pagination
from rest_framework.response import Response

class HotelPaginator(pagination.PageNumberPagination):
    page_size = 25

    def get_paginated_response(self, data):
        return Response({
            "current_page": self.page.number,
            "total_pages": self.page.paginator.num_pages,
            "count": self.page.paginator.count,
            "results": data,
        })