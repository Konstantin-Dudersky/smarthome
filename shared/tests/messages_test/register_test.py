from shared.messages import register_message


def test_tegister():
    register_message.messages_dict.clear()

    @register_message.register_message
    class Class1:
        ...

    @register_message.register_message
    class Class2:
        ...

    assert Class1.__name__ in register_message.messages_dict
    assert register_message.messages_dict[Class1.__name__] == Class1
    assert Class2.__name__ in register_message.messages_dict
    assert register_message.messages_dict[Class2.__name__] == Class2


def test_tegister_duplicate():
    register_message.messages_dict.clear()

    @register_message.register_message
    class Class1:  # type: ignore
        ...

    try:

        @register_message.register_message
        class Class1:  # type: ignore
            ...

    except TypeError:
        return
    assert False
