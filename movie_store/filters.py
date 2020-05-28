from rest_framework import filters

class ModelAttributeFiltering(filters.BaseFilterBackend):

    # TODO: typing?
    def filter_queryset(self, request, queryset, view):
        # Get searchable fields from view
        searchable_fields = getattr(view, "search_fields", [])

        # Dict of arguments that will be passed to queryset.filter()
        queryset_filter_kwargs = {}

        # For each param in query_params, if it matches any of the searchable_fields,
        # add it to the queryset_filter_kwargs along with its value
        for param in request.query_params:
            if param in searchable_fields:
                # Construct the argument name from the given parameter
                # queryset.filter works with argument names as "attributeName__operation=value"
                # e.g. "title__contains=foo"
                # Here we use "icontains" for case-insensitive non-exact match search
                arg = "{}__{}".format(param, "icontains")
                queryset_filter_kwargs[arg] = request.query_params.get(param)

        # Return the filtered queryset
        return queryset.filter(**queryset_filter_kwargs)


class GenreFiltering(filters.BaseFilterBackend):

    GENRE_PARAM_NAME = "genre"

    def filter_queryset(self, request, queryset, view):

        # If the genre param is in the query, filter against it
        if GenreFiltering.GENRE_PARAM_NAME in request.query_params:
            genre = request.query_params.get(GenreFiltering.GENRE_PARAM_NAME)
            qs = queryset.filter(genres__title__iexact=genre)
            return qs
        else:
            # Don't filter at all
            return queryset
