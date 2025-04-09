import pandas as pd

from util import diff_minutes


class RecordManager:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path, index_col=False, dtype=str)

    def get_last_row(self):
        return self.df.iloc[-1] if not self.df.empty else None

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

        last_idx = self.df.index[-1]
        self.df.at[last_idx, "duration"] = diff_minutes(prev["time"], new_row["time"])

        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)

    def undo(self):
        if not self.df.empty:
            self.df = self.df.iloc[:-1]

    def save(self):
        self.df.to_csv(self.csv_path, index=False)

    def to_string(self):
        return self.df.to_csv(sep="\t", index=False)
