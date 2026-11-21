from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Базовая схема для HTTP API."""
    model_config = ConfigDict(
        from_attributes=True,      # Можно создавать из ORM/dataclass
        use_enum_values=True,      # Enum → строка в JSON
        str_strip_whitespace=True, # Убираем пробелы по краям строк
    )