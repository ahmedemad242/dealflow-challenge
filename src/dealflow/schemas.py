from dealflow import ma, db

paginated_schema_cache = {}
pagination_query_cache = {}


class EmptySchema(ma.Schema):
    pass


class PaginationSchema(ma.Schema):
    class Meta:
        ordered = True

    limit = ma.Integer()
    offset = ma.Integer()
    count = ma.Integer(dump_only=True)
    total = ma.Integer(dump_only=True)


def PaginatedCollection(schema):
    if schema in paginated_schema_cache:
        return paginated_schema_cache[schema]

    class PaginatedSchema(ma.Schema):
        class Meta:
            ordered = True

        pagination = ma.Nested(PaginationSchema)
        data = ma.Nested(schema, many=True)

    PaginatedSchema.__name__ = f"Paginated{schema.__class__.__name__}"
    paginated_schema_cache[schema] = PaginatedSchema
    return PaginatedSchema


def PaginatedQueryParams(schema):
    if schema in pagination_query_cache:
        return paginated_schema_cache[schema]

    combined_fields = dict(PaginationSchema().fields)
    combined_fields.update(schema().fields)

    # Dynamically create a new class with the combined fields
    PaginatedSchema = type(
        f"Paginated{schema.__class__.__name__}",
        (ma.Schema,),
        {"Meta": type("Meta", (), {"ordered": True}), **combined_fields},
    )

    pagination_query_cache[schema] = PaginatedSchema
    return PaginatedSchema
