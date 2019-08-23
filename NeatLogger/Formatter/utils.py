from typing import Dict, List, Optional, Tuple

from colorama import Fore, Style


def get_apache_log_format(
    attr_config_dict: Dict[str, Tuple[Optional[str], Optional[str], int]],
    ignore_attr_list: List[str],
    add_colors: bool = False,
) -> str:

    format_list = list()
    for attr, (attr_name, str_format, color) in attr_config_dict.items():

        if attr in ["message", "msg"] or attr in ignore_attr_list:
            continue

        attr_name = attr if attr_name is None else attr_name
        str_format = "s" if str_format is None else str_format

        if add_colors is True:
            format_list.append(
                f"[{Fore.LIGHTBLACK_EX}{attr_name}{Style.RESET_ALL} "
                + f"{color}%({attr}){str_format}{Style.RESET_ALL}]"
            )
        else:
            format_list.append(f"[{attr_name} %({attr}){str_format}]")

    format_list.append("%(message)s")

    return " ".join(format_list)
