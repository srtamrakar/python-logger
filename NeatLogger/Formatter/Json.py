from datetime import datetime, timezone

from pythonjsonlogger import jsonlogger

from . import configs


def merge_record_extra(record, target, reserved):
    """To override Json.add_fields"""
    for key, value in record.__dict__.items():
        # this allows to have numeric keys
        if key not in reserved and not (
            hasattr(key, "startswith") and key.startswith("_")
        ):
            target[key] = value
    return target


class Json(jsonlogger.JsonFormatter):
    def __init__(self, *args, **kwargs):
        self.use_utc = kwargs.pop("use_utc", False)
        self.ignore_log_attribute_list = kwargs.pop("ignore_log_attribute_list", None)
        self.timezone = (
            timezone.utc if self.use_utc is True else datetime.now().astimezone().tzinfo
        )

        if self.ignore_log_attribute_list is None:
            self.ignore_log_attribute_list = configs.DEFAULT_IGNORE_ATTRIBUTE_LIST
        self.ignore_log_attribute_list.append("msg")

        super().__init__(
            json_ensure_ascii=False,
            reserved_attrs=self.ignore_log_attribute_list,
            timestamp=True,
        )

    def add_fields(self, log_record, record, message_dict):
        """Override: jsonlogger.JsonFormatter.add_fields"""
        for field in self._required_fields:
            log_record[field] = record.__dict__.get(field)
        log_record.update(message_dict)
        merge_record_extra(record, log_record, reserved=self._skip_fields)

        if self.timestamp:
            key = self.timestamp if type(self.timestamp) == str else "timestamp"
            log_record[key] = datetime.fromtimestamp(record.created, tz=self.timezone)
