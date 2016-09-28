from lista.prompt.key import Key
import pytest


def test_resolve():
    assert Key.resolve(100) == 100
    assert Key.resolve("\udc80kb") == "kb"
    assert Key.resolve("^H") == 0x08
    assert Key.resolve("Up") == "ku"
    assert Key.resolve("CR") == 0x0d
    assert Key.resolve("A") == ord("A")


def test_constructor():
    assert Key(100).code == 100
    assert Key(100).char == "d"
    assert Key("\udc80kb").code == "kb"
    assert Key("\udc80kb").char == ""
    assert Key("^H").code == 0x08
    assert Key("^H").char == "\x08"
    assert Key("Up").code == "ku"
    assert Key("Up").char == ""
    assert Key("CR").code == 0x0d
    assert Key("CR").char == "\r"
    assert Key("A").code == ord("A")
    assert Key("A").char == "A"


def test_singleton():
    keyA1 = Key('A')
    keyA2 = Key('A')
    keyB1 = Key('B')
    keyB2 = Key('B')

    assert keyA1 is keyA2
    assert keyB1 is keyB2
    assert keyA1 is not keyB1
    assert keyA1 != keyB1
