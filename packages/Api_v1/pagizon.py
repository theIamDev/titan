from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class UniversalPaginator:
    def __init__(self, queryset, params, default_per_page=20):
        self.queryset = queryset
        
        # Safely handle integer conversion for page and per_page
        try:
            self.page_num = int(params.get('page', 1))
            self.per_page = int(params.get('per_page', default_per_page))
        except (ValueError, TypeError):
            self.page_num, self.per_page = 1, default_per_page

        self.paginator = Paginator(self.queryset, self.per_page)

    def get_page(self):
        try:
            return self.paginator.page(self.page_num)
        except (PageNotAnInteger, EmptyPage):
            return self.paginator.page(1)

    @staticmethod
    def get_meta(page_obj):
        """Returns metadata standard for API responses"""
        return {
            "total_items": page_obj.paginator.count,
            "total_pages": page_obj.paginator.num_pages,
            "current_page": page_obj.number,
            "per_page": page_obj.paginator.per_page,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
        }