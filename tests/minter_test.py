import re

import pytest

import noid_minter.minter as nm
from noid_minter.minter import Minter, MintOrder


def test_minimal_configuration():
    with pytest.raises(nm.MissingConfigurationException):
        minter = Minter()
    with pytest.raises(nm.MissingConfigurationException):
        minter = Minter({})
    try:
        minter = Minter({"template": ".sd"})
    except Exception as message:
        pytest.fail(f"Unexpected exception raised: {message}")


def test_naan():
    minter = Minter({"template": ".sd"})
    assert minter.naan is None
    minter = Minter({"template": ".sd", "naan": "16417"})
    assert minter.naan == "16417"


def test_template_specifies_mint_order():
    minter = Minter({"template": ".rd"})
    assert minter.order == MintOrder.RANDOM
    minter = Minter({"template": ".sd"})
    assert minter.order == MintOrder.SEQUENTIAL
    minter = Minter({"template": ".zd"})
    assert minter.order == MintOrder.GROWING


def test_first_sequential_identifier_is_zero():
    minter = Minter({"template": ".sdd"})
    response = minter.mint()
    assert response.ark == "00"


def test_sequential_minter_mints_sequentially():
    minter = Minter({"template": ".sd"})
    assert minter.mint().ark == "0"
    assert minter.mint().ark == "1"
    assert minter.mint().ark == "2"
    assert minter.mint().ark == "3"


def test_sequential_minter_mints_digit_strings_and_exhausts():
    minter = Minter({"template": ".sddd"})
    for i in range(1000):
        response = minter.mint()
        assert re.match(r"^\d\d\d$", response.ark)
    assert minter.is_exhausted()


def test_growing_minter_extends_ark_length():
    minter = Minter({"template": ".zddd"})
    for i in range(1000):
        response = minter.mint()
        assert re.match(r"^\d\d\d$", response.ark)
    assert not minter.is_exhausted()
    response = minter.mint()
    assert response.ark == "1000"


def test_minter_uses_betanumeric_if_provided_in_template():
    minter = Minter({"template": ".se"})
    arks = []
    for i in range(29):
        response = minter.mint()
        arks.append(response.ark)
    assert "".join(arks) == "0123456789bcdfghjkmnpqrstvwxz"


def test_multibase_representation_works():
    minter = Minter({"template": ".sede"})
    minter.counter = 5678
    assert minter.mint().ark == "n5s"


def test_random_minter_preserves_noid_mint_order():
    minter = Minter({"template": ".reeedeeed"})
    assert minter.mint().ark == "4xg9f4v1"
    assert minter.mint().ark == "15d8nck7"
    assert minter.mint().ark == "wdb7vn02"
    assert minter.mint().ark == "rn872vq8"
    assert minter.mint().ark == "mw6693g4"
    assert minter.mint().ark == "h445hb70"
    assert minter.mint().ark == "cc24qjz6"
    assert minter.mint().ark == "7pv6b2x5"
    assert minter.mint().ark == "3xs5j9p1"
    assert minter.mint().ark == "05q4rjd7"
