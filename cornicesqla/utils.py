import re

FILTER_RE = re.compile(r'^filter\[([\w|-]+)\]$')

def batching(request, items, count_k='count', page_k='page'):
    """ batch tool """
    count = int(request.params.get(count_k, 0))
    page = int(request.params.get(page_k, 0))
    total = len(items)
    page_s, page_e = (0, None)
    if page and count:
        page_s = (page - 1) * count
        page_e = page_s + count
    return items[page_s:page_e]

def get_filters(request, mapping):
    """ Parsing url params and return filters from  it
    returns (date_start, date_end, query_filters)
    filter example:
        filter[col_name]=data
    """
    filters = dict([(FILTER_RE.match(k).group(1), v)
                    for (k, v) in request.params.items()
                    if FILTER_RE.match(k)])
    date_start = filters.get('from', None)
    date_end = filters.get('to', None)
    # getting fields list from mapping
    fields = mapping.get_fields_list()
    # filtering list of filters from request by object existing fields
    query_filters = dict([(k, v) for k, v in filters.items()
                          if k in fields and v])
    return date_start, date_end, query_filters

def apply_filters_from_request(request, mapping, query):
    """ query factory for database """
    date_start, date_end, filters = get_filters(request, mapping)
    if date_end and date_start:
        query = query.filter(mapping.date.between(date_start, date_end))
    elif date_start:
        query = query.filter(mapping.date >= date_start)
    elif date_end:
        query = query.filter(mapping.date <= date_end)
    return query.filter_by(**filters)
