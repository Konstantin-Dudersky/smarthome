from collections import defaultdict
from typing import TypeAlias

from ..simple_deque import SimpleDeque
from ..messages import BaseMessage

TSimpleDeque: TypeAlias = SimpleDeque[BaseMessage]


class SubsCollection(object):
    def __init__(self) -> None:
        self.__by_subs_name: dict[str, TSimpleDeque] = {}
        self.__by_entity_id: dict[str, list[TSimpleDeque]] = defaultdict(list)

    def __getitem__(self, subs_name: str) -> TSimpleDeque:
        return self.__by_subs_name[subs_name]

    def add_subs(self, subs_name: str, entity_id: str | None) -> None:
        if subs_name in self.__by_subs_name:
            raise KeyError(
                "Подписка с названием {0} уже существует".format(subs_name),
            )
        deque: TSimpleDeque = SimpleDeque[BaseMessage]()
        self.__by_subs_name[subs_name] = deque
        entity_key: str = entity_id if entity_id is not None else "__all__"
        self.__by_entity_id[entity_key].append(deque)

    def new_message(self, entity_id: str, message: BaseMessage) -> None:
        deque_list: list[TSimpleDeque] = self.__by_entity_id[entity_id]
        for deque in deque_list:
            deque.append(message)
        for deque in self.__by_entity_id["__all__"]:
            deque.append(message)
