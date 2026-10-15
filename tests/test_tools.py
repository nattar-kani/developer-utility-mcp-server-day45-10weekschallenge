
import json

import pytest

from server import (
    calculate,
    count_words,
    convert_temperature,
    format_json,
    get_timestamp,
)


# Tool 1: Calculator
def test_calculate_addition():
    assert calculate("10 + 5") == "15"


def test_calculate_expression():
    assert calculate("3 * 45 + 2 * 10") == "155"


def test_calculate_rejects_unsupported_expression():
    with pytest.raises(ValueError, match="Unsupported"):
        calculate("2 ** 3")


def test_calculate_rejects_long_expression():
    with pytest.raises(ValueError, match="too long"):
        calculate("1" * 101)


# Tool 2: Word counter
def test_count_words():
    result = count_words("Hello world. How are you?")

    assert result["word_count"] == 5
    assert result["character_count"] == 25
    assert result["sentence_count"] == 2


def test_count_words_empty_text():
    result = count_words("")

    assert result["word_count"] == 0
    assert result["character_count"] == 0
    assert result["sentence_count"] == 0


# Tool 3: Temperature converter
def test_celsius_to_fahrenheit():
    result = convert_temperature(100, "C", "F")

    assert result["converted_value"] == 212.0


def test_fahrenheit_to_celsius():
    result = convert_temperature(32, "F", "C")

    assert result["converted_value"] == 0.0


def test_kelvin_to_celsius():
    result = convert_temperature(273.15, "K", "C")

    assert result["converted_value"] == 0.0


def test_temperature_rejects_invalid_unit():
    with pytest.raises(ValueError, match="Units must be"):
        convert_temperature(100, "X", "C")


def test_temperature_rejects_below_absolute_zero():
    with pytest.raises(ValueError, match="absolute zero"):
        convert_temperature(-300, "C", "K")


# Tool 4: JSON formatter
def test_format_json():
    result = format_json('{"name":"Maya","age":25}')

    parsed = json.loads(result)

    assert parsed == {"name": "Maya", "age": 25}
    assert "\n" in result


def test_format_json_rejects_invalid_json():
    with pytest.raises(ValueError, match="Invalid JSON"):
        format_json('{"name": "Maya",}')


# Tool 5: Timestamp
def test_get_timestamp():
    result = get_timestamp()

    assert result["utc_timestamp"].endswith("+00:00")
    assert isinstance(result["unix_timestamp"], float)
    assert result["unix_timestamp"] > 0
