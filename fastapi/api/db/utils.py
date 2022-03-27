def paginate(query, page: int, page_size: int):
    # Page comes 1-indexed
    offset = (page - 1) * page_size
    return query.offset(offset).limit(page_size)
