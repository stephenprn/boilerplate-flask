from dataclasses import dataclass


@dataclass
class FilterText:
    text: str
    ignore_case: bool
    partial_match: bool


@dataclass
class FilterInt:
    min_value: int
    max_value: int
    min_strict: bool
    max_strict: bool
