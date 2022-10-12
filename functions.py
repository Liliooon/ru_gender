from typing import Optional
from pymorphy2 import MorphAnalyzer
from constants import name_parts_kind_map


def get_one_name_part_gender(name_part: str, name_part_kind: str, morph: MorphAnalyzer) -> Optional[str]:
    name_part_kind = name_parts_kind_map[name_part_kind]
    try:
        parse_res = [p for p in morph.parse(name_part) if p.tag.case == "nomn"]
        parse_res_with_name_part_kind = [p for p in parse_res if name_part_kind in p.tag]
        if parse_res_with_name_part_kind:
            return parse_res_with_name_part_kind[0].tag.gender
        return None
    except IndexError:
        return None


def get_name_parts_gender(name_parts: dict, morph: MorphAnalyzer) -> list:
    name_parts_gender = [
        get_one_name_part_gender(name_part, name_part_kind, morph)
        for name_part_kind, name_part in name_parts.items()
    ]
    name_parts_gender = [gender for gender in name_parts_gender if gender]
    return name_parts_gender
