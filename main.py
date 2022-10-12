from collections import Counter

from pymorphy2 import MorphAnalyzer

from constants import gender_map
from functions import get_name_parts_gender

morph = MorphAnalyzer()


def get_fullname_gender(first_name: str = "", middle_name: str = "", last_name: str = "") -> str:
    gender = None

    first_name = first_name.lower()
    middle_name = middle_name.lower()
    last_name = last_name.lower()

    fullname = {
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name
    }

    if not any(fullname.values()):
        gender = "?"

    if (middle_name.endswith("ич")
            or any(last_name.endswith(end) for end in ["ов", "ев", "ин", "ий", "ой", "ый", "ас"])
            or first_name.startswith("оглы")):
        gender = "М"
    elif middle_name.endswith("вна"):
        gender = "Ж"

    if not gender:
        name_parts = {}

        for name_part_kind, name_part in fullname.items():
            if "." not in name_part and name_part:
                name_parts[name_part_kind] = name_part

        name_parts_gender = get_name_parts_gender(name_parts, morph)

        gender_set_len = len(set(name_parts_gender))

        if gender_set_len == 1:
            gender = name_parts_gender[0]
        elif gender_set_len > 1:
            gender_counter = Counter(name_parts_gender).most_common()
            if len(set(count[1] for count in gender_counter)) == 1:
                gender = "М"
            else:
                gender = gender_counter[0][0]

    if gender:
        gender = gender_map.get(gender.lower(), gender)
    else:
        gender = "?"

    return gender
