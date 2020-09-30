from colorama import Fore, Style
from typing import Dict, Tuple, List, Optional


def get_log_format(
    attr_config_dict: Dict[str, Tuple[Optional[str], Optional[str], int]],
    ignore_attr_list: List[str],
) -> str:

    format_list = list()
    for (attr, (attr_name, str_format, color),) in attr_config_dict.items():

        if attr in ["message", "msg"] or attr in ignore_attr_list:
            continue

        attr_name = attr if attr_name is None else attr_name
        str_format = "s" if str_format is None else str_format

        format_list.append(
            f"[{Fore.LIGHTBLACK_EX}{attr_name}{Style.RESET_ALL} "
            + f"{color}%({attr}){str_format}{Style.RESET_ALL}]"
        )

    format_list.append("%(message)s")

    return " ".join(format_list)
