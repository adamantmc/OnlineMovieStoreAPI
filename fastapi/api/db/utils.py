def paginate(query, page, page_size):
    offset = page * page_size
    return query.offset(offset).limit(page_size)
