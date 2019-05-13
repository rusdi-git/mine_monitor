def generate_simple_summary(queryset,field):
    model=queryset.model
    choices=model._meta.get_field(field).choices
    data=list(queryset)
    if choices:
        for item in data:
            for choice in choices:
                if item[field]==choice[0]:
                    item[field]=choice[1]
    return data