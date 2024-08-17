import pytest

## https://docs.pytest.org/en/stable/


def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be less than 0")


def test_validate_age_valid_age():
    validate_age(10)


def test_validate_age_invalid_age():
    with pytest.raises(ValueError, match="Age cannot be less than 0"):
        validate_age(-1)
