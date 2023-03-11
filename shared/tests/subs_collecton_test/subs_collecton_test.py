from shared.redis_subscriber import SubsCollection
from shared.messages import BaseMessage


def test_no_subs():
    collection = SubsCollection()
    try:
        collection["not_existent_subs"]
    except KeyError:
        assert True
    assert False


def test_several_subs():
    collection = SubsCollection()
    collection.add_subs("subs_1", "entity_1")
    collection.add_subs("subs_2", None)
    assert collection["subs_1"]
    assert collection["subs_2"]


def test_several_subs_same_name():
    collection = SubsCollection()
    collection.add_subs("subs_1", "entity_1")
    try:
        collection.add_subs("subs_1", None)
    except KeyError:
        return
    assert False


def test_new_msg() -> None:
    msg = BaseMessage.construct()
    collection = SubsCollection()
    collection.add_subs("subs_1", "entity_1")
    collection.add_subs("subs_2", None)
    collection.new_message("entity_1", msg)
    assert msg == collection["subs_1"].pop()
    assert msg == collection["subs_2"].pop()
