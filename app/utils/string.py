def snake_to_camel_case(name: str) -> str:
    parts = iter(name.split("_"))
    return next(parts) + "".join(i.title() for i in parts)
