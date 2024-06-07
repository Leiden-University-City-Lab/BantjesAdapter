def relation_type_validator(v):
    if not str(v).isdigit():
        raise ValueError("Relation type can not be Null.")
    return v
