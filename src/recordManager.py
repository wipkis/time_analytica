import pandas as pd

from util import diff_minutes


class RecordManager:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.records = pd.read_csv(csv_path, index_col=False, dtype=str)

    def get_last_row(self):
        return self.records.iloc[-1] if not self.records.empty else None

    def add_row(self, fields: list[str]):
        prev = self.get_last_row()
        if prev is None:
            raise ValueError("기존 데이터가 없습니다.")

        new_row = {
            "date": prev["date"],
            "time": fields[0],
            "duration": 0,
            "act": fields[1],
            **({"category_1": fields[2]} if len(fields) > 2 else {}),
            **({"category_2": fields[3]} if len(fields) > 3 else {}),
        }

        last_idx = self.records.index[-1]
        self.records.at[last_idx, "duration"] = diff_minutes(
            prev["time"], new_row["time"]
        )

        self.records = pd.concat(
            [self.records, pd.DataFrame([new_row])], ignore_index=True
        )

    def undo(self):
        if not self.records.empty:
            self.records = self.records.iloc[:-1]

    def save(self):
        self.records.to_csv(self.csv_path, index=False)

    def to_string(self):
        return self.records.to_csv(sep="\t", index=False)
