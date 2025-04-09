import pytest

from recordManager import RecordManager


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
