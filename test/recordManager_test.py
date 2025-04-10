from datetime import datetime
from unittest.mock import patch

import pytest

from recordManager import RecordManager


@patch("recordManager.datetime")
def test_today(mock_datetime):
    fixed_today = datetime(2025, 4, 10)
    mock_datetime.today.return_value = fixed_today
    mock_datetime.strptime = datetime.strptime


@pytest.fixture
def manager():
    return RecordManager(csv_path="./test/res/test.csv")


def test_get_last_row(manager):
    last_row = manager.get_last_row()

    assert last_row["act"] == "식사"


def test_add_row(manager):
    prev_last_row = manager.records.loc[manager.records.index[-1]]
    manager.add_row(["1000", "act"])
    new_last_row = manager.get_last_row()

    assert prev_last_row["time"] == "0900"
    assert prev_last_row["duration"] == 60
    assert new_last_row["time"] == "1000"
    assert new_last_row["act"] == "act"


def test_undo(manager):
    record_num = manager.records.index[-1]
    manager.undo()
    last_row = manager.get_last_row()

    assert record_num == manager.records.index[-1] + 1
    assert last_row["act"] == "수면"


def test_add_row_after_undo(manager):
    record_num = manager.records.index[-1]
    manager.add_row(["1000", "act"])
    manager.undo()
    last_row = manager.get_last_row()

    assert record_num == manager.records.index[-1]
    assert last_row["time"] == "0900"
    assert last_row["duration"] == 60

    manager.add_row(["0910", "act2"])
    prev_last_row = manager.records.loc[manager.records.index[-2]]
    last_row = manager.get_last_row()
    assert prev_last_row["time"] == "0900"
    assert prev_last_row["duration"] == 10
    assert last_row["time"] == "0910"
    assert last_row["act"] == "act2"


def test_handling_prev_and_get_date(manager):
    # prev가 있는 경우
    # 날자변경 없음
    date = manager.handling_prev_and_get_date("0900")

    last_row = manager.get_last_row()
    assert date == "2025-04-01"
    assert last_row["time"] == "0900"
    assert last_row["duration"] == 0

    date = manager.handling_prev_and_get_date("0930")

    last_row = manager.get_last_row()
    assert date == "2025-04-01"
    assert last_row["time"] == "0900"
    assert last_row["duration"] == 30

    # 날자변경 있음
    date = manager.handling_prev_and_get_date("0859")

    last_row = manager.get_last_row()
    assert date == "2025-04-02"
    assert last_row["time"] == "0900"
    assert last_row["duration"] == 1439

    # prev가 없는 경우
    manager.undo()
    manager.undo()

    date = manager.handling_prev_and_get_date("0859")

    last_row = manager.get_last_row()
    assert last_row is None
    assert date == datetime.today().strftime("%Y-%m-%d")
