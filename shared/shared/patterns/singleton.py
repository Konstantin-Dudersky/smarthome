"""Метакласс для создания одиночки.

Экземпляр класса можно создавать только один раз. При следующих попытках
создания будет возбуждено исключение.

В идеале, инициализация объекта должна быть в модуле точки входа.

Метакласс наследуется от Generic - не нашел удобного способа для подсказки
типов.

Использование:

class Singleton(object, metaclass=SingletonMeta["Singleton"]):
    pass

s1 = Singleton()
# code ...
s2 = Singleton.instance()
"""

from typing import Any, Final, Generic, Self, TypeVar

MSG_ALREADY_CREATED: Final[str] = "instance of class {cls} already created"
MSG_NOT_CREATED: Final[str] = "instance of class {cls} not created"

TSingleton = TypeVar("TSingleton")


class SingletonMeta(type, Generic[TSingleton]):
    """Метакласс для создания одиночки."""

    __instances: dict[Self, TSingleton] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> TSingleton:
        """Конструирование нового / возвращение существующего экземпляра."""
        if cls in cls.__instances:
            raise TypeError(MSG_ALREADY_CREATED.format(cls=cls))
        instance: TSingleton = super().__call__(*args, **kwargs)
        cls.__instances[cls] = instance
        return cls.instance()

    def instance(cls) -> TSingleton:
        """Экземпляр класса."""
        if cls not in cls.__instances:
            raise TypeError(MSG_NOT_CREATED.format(cls=cls))
        return cls.__instances[cls]
