from __future__ import annotations
from typing import Any, ClassVar

SingletonMetaType = type["SingletonMeta"]


class SingletonMeta(type):
    _instances: ClassVar[dict[type, SingletonMetaType]] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> SingletonMetaType:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
