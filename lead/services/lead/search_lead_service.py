from django.db.models import Q, Case, When, Value, IntegerField
from ...models.lead import Lead

def search_lead(keyword, user):
    """
    Basic relevance scoring for MySQL using icontains and startswith.
    Returns top 25 matches with simple manual ranking.
    """
    if not user:
        return [], keyword

    keyword = keyword.strip()
    if not keyword:
        return [], keyword

    query = Q(name__icontains=keyword) | Q(email__icontains=keyword) | Q(valid_contact__icontains=keyword)
    if keyword.isdigit():
        query |= Q(id=int(keyword))

    results = (
        Lead.objects.for_user(user) # type: ignore
        .filter(query)
        .annotate(
            relevance=Case(
                When(name__istartswith=keyword, then=Value(3)),
                When(name__icontains=keyword, then=Value(2)),
                When(email__icontains=keyword, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        )
        .order_by('-relevance', '-id')
        .values('id', 'name', 'email', 'contact','valid_contact')[:25]
    )
    return list(results), keyword
