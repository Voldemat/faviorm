import enum

import pytest

import faviorm


@pytest.mark.mypy_testing
def test_timestamp_default() -> None:
    faviorm.Column(  # E:  Cannot infer type argument 1 of "Column"  [misc]
        "exp_at", faviorm.TIMESTAMP(), True, "NON"
    )


class PepperType(enum.Enum):
    CAROLINAREAPER = "CAROLINAREAPER"
    JALAPENO = "JALAPENO"


class BearType(enum.Enum):
    STOUT = "STOUT"
    GOSE = "GOSE"


@pytest.mark.mypy_testing
def test_enum_default_type() -> None:
    faviorm.Column(  # E:  Cannot infer type argument 1 of "Column"  [misc]
        "content_type", faviorm.ENUM(BearType), False, PepperType.JALAPENO
    )


@pytest.mark.mypy_testing
def test_numeric_type() -> None:
    faviorm.Column(  # E:  Cannot infer type argument 1 of "Column"  [misc]
        "num_col", faviorm.NUMERIC(2, 3), False, "12"
    )


@pytest.mark.mypy_testing
def test_interval_type() -> None:
    faviorm.Column(  # E:  Cannot infer type argument 1 of "Column"  [misc]
        "col", faviorm.INTERVAL(2), False, "12"
    )


@pytest.mark.mypy_testing
def test_money_type() -> None:
    faviorm.Column(  # E:  Cannot infer type argument 1 of "Column"  [misc]
        "col", faviorm.MONEY(2), False, bool
    )


@pytest.mark.mypy_testing
def test_float_type() -> None:
    faviorm.Column(  # E:  Cannot infer type argument 1 of "Column"  [misc]
        "col", faviorm.FLOAT(2), False, "FFF"
    )


@pytest.mark.mypy_testing
def test_smallint_type() -> None:
    faviorm.Column(  # E:  Cannot infer type argument 1 of "Column"  [misc]
        "num_col", faviorm.SMALLINT(), False, 2.14
    )


@pytest.mark.mypy_testing
def test_bigint_type() -> None:
    faviorm.Column(  # E:  Cannot infer type argument 1 of "Column"  [misc]
        "col", faviorm.BIGINT(), False, 2.14
    )


@pytest.mark.mypy_testing
def test_json_type() -> None:
    faviorm.Column(  # E:  Cannot infer type argument 1 of "Column"  [misc]
        "col", faviorm.JSON(), False, {PepperType: BearType}
    )


@pytest.mark.mypy_testing
def test_timetz_type() -> None:
    faviorm.Column(  # E:  Cannot infer type argument 1 of "Column"  [misc]
        "col", faviorm.TIMETZ(), False, "infinity"
    )


@pytest.mark.mypy_testing
def test_timestamptz_type() -> None:
    faviorm.Column(  # E:  Cannot infer type argument 1 of "Column"  [misc]
        "col", faviorm.TIMESTAMPTZ(), False, "allballs"
    )
