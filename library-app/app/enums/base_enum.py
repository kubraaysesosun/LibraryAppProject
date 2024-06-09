from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def __get_validators__(cls):
        cls.lookup = {v: k.value for v, k in cls.__members__.items()}
        cls.keys = [*cls.lookup]
        yield cls.validate

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="str", enum=cls.keys)

    @classmethod
    def validate(cls, v):
        if isinstance(v, Enum):
            return v
        try:
            if isinstance(v, str):
                return cls[v]
            elif isinstance(v, int):
                return cls(v)
        except (KeyError, ValueError):
            permitted = ", ".join(v for v in cls.keys)
            raise ValueError(
                f"value is not a valid enumeration member; permitted: {permitted}"
            )

    def _generate_next_value_(name, start, count, last_values):
        return name.lower()
